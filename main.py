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

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

genai.configure(api_key = GEMINI_API)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(message.content[1:] + " Ensure that your response is less than 1000 characters in length.")
        await message.channel.send(response.text)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(DISCORD_API)
# client.run(DISCORD_API)