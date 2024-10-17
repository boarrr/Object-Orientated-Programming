import subprocess
import pytesseract
import pyperclip
from dotenv import load_dotenv
from pynput import keyboard
from openai import OpenAI
import os

# Variable to store the extracted text
extracted_text = ""

load_dotenv()

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

def on_activate():

    # Prompt to take a screenshot of a selected region
    screenshot_path = 'temp_screenshot.png'
    subprocess.call(['screencapture', '-i', screenshot_path])

    # Perform OCR on the screenshot
    if os.path.exists(screenshot_path):
        try:
            text = pytesseract.image_to_string(screenshot_path)
            global extracted_text
            extracted_text = text

            response = client.chat.completions.create(
                messages=[
                    { "role": "system", "content": "You are an assistant in completing quizzes in a timely manner.\
                            The content you are given will contain a lot of information, pleae only isolate and focus on actual questions in the text.\
                            Any questions that are not provided with a multiple choice answer, please return a paragraph answer to the question\
                            Please just return the correct option which is the answer to the question and that is all, please escape char any quotes such as \""},
                    { "role": "user", "content": extracted_text}
        
                ],
                model="gpt-4o",
            )

            # Notify the user with a push notification
            notification_title = "ChatGPT:"
            notification_text = response.choices[0].message.content

            subprocess.call([
                'osascript', '-e',
                f'display notification "{notification_text}" with title "{notification_title}"'
            ])

            pyperclip.copy(notification_text)
            

        except Exception as e:
            print(f"An error occurred during OCR: {e}")
        finally:
            # Clean up the temporary screenshot file
            os.remove(screenshot_path)
    else:
        print("No screenshot was taken.")


def on_exit():
    listener.stop()

# Set up the global hotkey listener
with keyboard.GlobalHotKeys({
        '<ctrl>+s': on_activate,
        '<ctrl>+q': on_exit
    }) as listener:
    listener.join()
