import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API = os.getenv("GEMINI")

bot = commands.Bot(command_prefix='$', intents=discord.Intents.default())

genai.configure(api_key = GEMINI_API)

@bot.event
async def on_ready():
    print("Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as error:
        print(error)

@bot.tree.command(name="prompt")
@app_commands.describe(content = "Prompt to send to Gemini")
async def prompt(interaction : discord.Interaction, content : str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        "You are impersonating spongebob. " + content + " Ensure that your response is less than 1000 characters in length."
    )
    await interaction.response.send_message(response.text, ephemeral=True)

bot.run(DISCORD_API)