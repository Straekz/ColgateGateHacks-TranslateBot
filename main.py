import logging
import discord
from discord import app_commands
from discord.ext import tasks, commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyautogui
import pyttsx3

load_dotenv()

DISCORD_API = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API = os.getenv("GEMINI")

bot = commands.Bot(command_prefix = '@@', intents = discord.Intents.default())

genai.configure(api_key = GEMINI_API)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='genai.log', level=logging.INFO)

engine = pyttsx3.init()

@tasks.loop(seconds = 8.0)
async def commentary():
    screenshot = pyautogui.screenshot("screenshot.png")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        genai.upload_file("screenshot.png"),
        "\n\n",
        "You are my gaming coach. Tell me what you see in only 1 sentence, then tell me how I can improve in my current situation in only 1 sentence."
    ])

    engine.say(response.text)
    engine.runAndWait()

@bot.event
async def on_ready():
    logger.info("Ready!")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as error:
        logger.error(error)
    commentary.start()

@bot.tree.command(name = "prompt")
@app_commands.describe(content = "Prompt to send to Gemini")
async def prompt(interaction : discord.Interaction, content : str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"Translate the following content to Japanese: {content}"
    )
    await interaction.response.send_message(response.text, ephemeral=True)

bot.run(DISCORD_API)