import threading
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pyautogui
from gtts import gTTS
import pyglet

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = GEMINI_API)

screenshot_file_path = "tmp/temp.png"
audio_file_path = "tmp/temp.mp3"
prompt = "You are a backseat gamer. Playfully suggest something I should do. Please, keep your response minimal and under 1 sentences."

def commentary():
    threading.Timer(6.0, commentary).start()
    print("Generating commentary...")
    screenshot = pyautogui.screenshot(screenshot_file_path)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            genai.upload_file(screenshot_file_path),
            prompt
        ])
    except:
        return

    text_to_speech = gTTS(
        text = response.text,
        lang = 'en'
    )
    text_to_speech.save(audio_file_path)

    audio = pyglet.media.load(audio_file_path, streaming=False)
    audio.play().pitch = 1.3

if __name__ == "__main__":
    commentary()

    pyglet.app.run()