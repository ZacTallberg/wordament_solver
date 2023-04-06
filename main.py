import os, sys
import time, random
from random import randrange
import pyautogui
import pytesseract
import cv2
import numpy as np
import asyncio
import mouse 
import win32api, win32con
from image_slicer import slice
import os 
import wordament_solver
import read_text
import time

screenWidth, screenWidth = pyautogui.size()


region=(300, 300, 1300, 700 )
time_between_keys = 0.1
all_squares = []


left = 0
top = 0
width = 110
height = 110

async def main(x, y):
    start = time.time()
    try:
        read_text.find_letters()
        wordament_solver.run_program()
        wordament_image_center = pyautogui.locateCenterOnScreen('test-wordament.png', confidence = 0.6)
        pyautogui.click(wordament_image_center)
        await asyncio.sleep(0.5)
        with open('solution_words.txt', 'r') as solution_words:
            for word in solution_words:
                ## stop program after a minute and a half
                if time.time() - start >= 90:
                    break
                pyautogui.write(word, interval=0.0001)
                print(word)


    except Exception as e:
        print('oh ' + str(e))
        quitPendingTasks()
        return False
    else:

        return True

def quitPendingTasks():
    pending_tasks = [
        task for task in asyncio.all_tasks() if not task.done()
    ]
    print(pending_tasks)
    tasks = loop.run_until_complete(asyncio.gather(*pending_tasks))
    tasks.exception()
    loop.stop()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(300,300))
except KeyboardInterrupt:
    print('caught KeyboardInterrupt')
    quitPendingTasks()
    quit()
except Exception as e:
    print('Exception, quitting!' + str(e))
    # quitPendingTasks()
    
