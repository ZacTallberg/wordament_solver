import cv2
import numpy as np
import pytesseract
import re
import image_slicer
import pyautogui
import os
import string
from PIL import Image
import math

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, convert to HSV format, define lower/upper ranges, and perform
# color segmentation to create a binary mask

def iterate_single_letter_images(image_name):
    
    image = cv2.imread('./wordament_found/splits/' + image_name)
    image = cv2.bitwise_not(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 179])
    upper = np.array([179, 17, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Create horizontal kernel and dilate to connect text characters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    dilate = cv2.dilate(mask, kernel, iterations=2)
    data = None
    
    # Find contours and filter using aspect ratio
    # Remove non-text contours by filling in the contour
    def test_value(dilate, mask):
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for index, c in enumerate(cnts):
            
            x,y,w,h = cv2.boundingRect(c)

            ## This section needs work, .15 is just an arbitrary value I chose that works well enough
            ## any lower and it starts forgetting what "I" looks like
            ## any higher and it forgets how to english
            ar = w / float(h)
            if ar < .15:
                cv2.drawContours(dilate, [c], -1, (0,0,0), -1)
            # Bitwise dilated image with mask, invert, then OCR
        result = 255 - cv2.bitwise_and(dilate, mask)
        
        data = pytesseract.image_to_string(result, lang='eng',config='--psm 10')
        return result, data

    return_value, data = test_value(dilate, mask)

    ## THIS IS GROSS, BUT I HAVEN'T OPTIMIZED MY LETTER SEARCH YET
    if '|' in data:
        data = data.replace('|', 'I')
    if 'a' in data:
        data = data.replace('a', 'I')
    
    data = re.sub(r'\W+', '', data)
    cv2.imwrite('./wordament_found/dilate/' + image_name, dilate)
    return(return_value, data)

def find_letters():
    try:
        ## removes any lowercase characters, since I haven't optimized my code and we have a lot of weird characters to deal with
        table = str.maketrans('', '', string.ascii_lowercase)
        wordament_screenshot = pyautogui.locateOnScreen('test-wordament.png', confidence = 0.6)
        if not wordament_screenshot:
            raise Exception ("NO SCREENSHOT")
        else:
            pyautogui.screenshot('./wordament_found/main_image.png', region=wordament_screenshot)

            letters = image_slicer.slice('./wordament_found/main_image.png', 16, save=False)
            
            image_slicer.save_tiles(letters, directory='./wordament_found/splits', prefix='letter', format='png')
            full_characters = []

            for filename in os.listdir('./wordament_found/splits'):
                file_path = './wordament_found/splits/' + filename
                split_image = Image.open(file_path)
                left = 0
                top = 0 + 32
                right = split_image.size[0]
                bottom = split_image.size[1]

                cropped_image = split_image.crop((left,top,right,bottom))
                cropped_image.save(file_path)

                return_value, letters = iterate_single_letter_images(filename)
                if len(letters) > 1:
                    letters = letters.translate(table)
                full_characters.append(letters)

            new_strings = ['','','','']

            for index, character in enumerate(full_characters):
                count = math.floor(index/4)
                if index == 0 or (index+4)/(count+1) == 4:
                    space = ''
                else:
                    space = ' '
                
                return_carriage = '\n' if (index+1)%4 == 0 else ''

                new_strings[count] = new_strings[count] + space + character + return_carriage
            
            with open('./array.txt', 'w') as array_file:
                array_file.writelines(new_strings)
                array_file.close()

    except Exception as e:
        print(e)
