import time
import asyncio
import pyautogui
import random
import wordament_solver
import read_text

# Set PyAutoGUI pause to 0 to avoid blocking delays between actions
pyautogui.PAUSE = 0.0

async def type_human_like(word):
    """
    Types the word with random small delays between characters
    to simulate superhuman but natural input.
    """
    for char in word:
        pyautogui.write(char)
        # Random delay between keystrokes: 0.01 to 0.04 seconds
        # This corresponds to roughly 1500-6000 CPM, which is superhuman
        # but the variance makes it look less like a buffer dump.
        delay = random.uniform(0.01, 0.04)
        await asyncio.sleep(delay)

async def main():
    start = time.time()
    try:
        read_text.find_letters()
        wordament_solver.run_program()

        # Locate the game area
        wordament_image_center = pyautogui.locateCenterOnScreen('test-wordament.png', confidence=0.6)
        if wordament_image_center:
            pyautogui.click(wordament_image_center)

        await asyncio.sleep(0.5)

        with open('solution_words.txt', 'r') as solution_words:
            for line in solution_words:
                word = line.strip()
                if not word:
                    continue

                # Stop program after 90 seconds
                if time.time() - start >= 90:
                    break

                # Type the word with human-like variance and press Enter
                await type_human_like(word)
                pyautogui.press('enter')

                print(word)

                # Yield control is partially handled by type_human_like's asyncio.sleep
                # but we keep this for safety and inter-word timing
                await asyncio.sleep(0)

    except Exception as e:
        print('Error: ' + str(e))
        quitPendingTasks()
        return False
    else:
        return True

def quitPendingTasks():
    try:
        pending_tasks = [
            task for task in asyncio.all_tasks() if not task.done()
        ]
        if pending_tasks:
            if loop.is_running():
                for task in pending_tasks:
                    task.cancel()
            else:
                loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
    except Exception as e:
        print(f"Error cleaning up tasks: {e}")
    finally:
        loop.stop()

if __name__ == "__main__":
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt')
        quitPendingTasks()
    except Exception as e:
        print('Exception, quitting! ' + str(e))
        quitPendingTasks()
