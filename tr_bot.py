import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API = os.getenv("GEMINI")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '$', intents = intents)
intents.message_content = True
client = discord.Client(intents=intents)

genai.configure(api_key = GEMINI_API)

bot.lang = "Japanese"

@bot.event
async def on_ready():
    print("Ready!")

@bot.event
async def on_message(message):
    if message.author.bot or message.content.startswith('$'):
        if message.content.startswith('$set_lang '):
            bot.lang = message.content[10:]
        return
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Translate the following content to " + bot.lang + ": " + message.content)
    await message.channel.send(response.text)

bot.run(DISCORD_API)