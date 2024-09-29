import schedule, time
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyautogui
import pyttsx3

engine = pyttsx3.init()

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = GEMINI_API)

engine = pyttsx3.init()

def commentary():
    screenshot = pyautogui.screenshot("screenshot.png")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        genai.upload_file("screenshot.png"),
        "\n\n",
        "You are my professional gaming coach, who is also Goku from Dragon Ball Z. Tell me how I can improve on my current situation in under 3 sentences."
    ])

    engine.say(response.text)
    engine.runAndWait()

if __name__ == "__main__":
    schedule.every(5.0).seconds.do(commentary)

    while True:
        schedule.run_pending()
        time.sleep(1)