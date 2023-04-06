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

screenWidth, screenWidth = pyautogui.size()


region=(300, 300, 1300, 700 )
time_between_keys = 0.1
all_squares = []


left = 0
top = 0
width = 110
height = 110

async def main(x, y):
    screenshot = pyautogui.screenshot('./view.png')
    screenshot.save('./view.png')
    try:
        wordament_solver.run_program()
        await asyncio.sleep(0.5)
        print('yes')
        with open('solution_words.txt', 'r') as solution_words:
            for word in solution_words:
                pyautogui.write(word, interval=0.1)
                print(word)
        # last_square = None
        # for target in pyautogui.locateAllOnScreen('./test-wordament.png', confidence = 0.6):
        #     if not last_square:
        #         last_square = target
        #         all_squares.append(target)
        #         continue
        #     else:
        #         if target.left - last_square.left >= 100 or target.top - last_square.top >= 100:
        #             all_squares.append(target)                        
        #             last_square = target
        #             print(target)
        #         else:
        #             continue
                    
        # for index, square in enumerate(all_squares):
        #     pyautogui.screenshot('./test-photos/split_into.png', region=square)

        #     print(square)
        #     left = square.left
        #     top = square.top
        
        # if len(all_squares) == 1:
        #     square = all_squares[0]
        #     slice('./test-photos/split_into.png', 16)
        
        # top_left = (4, 36)
        # bottom_right = (106, 80)

        # top_left_num = (4, 16)
        # bottom_right_num = (32, 34)




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
    
