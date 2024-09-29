import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API = os.getenv("GEMINI")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

genai.configure(api_key = GEMINI_API)

@bot.command()
async def prompt(ctx, *, msg):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(msg + " Ensure that your response is less than 1000 characters in length.")
        await ctx.channel.send(response.text)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(DISCORD_API)
# client.run(DISCORD_API)