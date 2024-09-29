import discord
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

genai.configure(api_key = os.getenv("GEMINI"))

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

client.run(os.getenv('DISCORD_BOT_TOKEN'))