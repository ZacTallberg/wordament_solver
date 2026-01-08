import time
import asyncio
import pyautogui
import wordament_solver
import read_text

# Set PyAutoGUI pause to 0 to avoid blocking delays between actions
pyautogui.PAUSE = 0.0

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

                # Type the word and press Enter
                pyautogui.write(word)
                pyautogui.press('enter')

                print(word)

                # Yield control to the event loop to ensure the script remains responsive
                # and doesn't block itself
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
            # We are already in a loop context?
            # If called from KeyboardInterrupt (outside loop), we can run_until_complete.
            # If called from inside main (exception), loop is running.
            # But quitPendingTasks in original code used loop.run_until_complete.
            # This implies it's intended to be called from outside the loop or when loop is stopping?
            # Original code: tasks = loop.run_until_complete(asyncio.gather(*pending_tasks))
            # If called from inside main, this would fail (loop already running).
            # The original code called quitPendingTasks inside `except Exception` in `main`.
            # This would raise "RuntimeError: This event loop is already running".
            # So the original code was buggy in that regard.

            # I will fix this by checking if loop is running.
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
