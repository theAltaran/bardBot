import discord
import bardapi
from discord.ext import commands
from dotenv import load_dotenv
import os
import re

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
token = os.getenv('BARDAPI_TOKEN')
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!bard'):
        # Process the command
        await bot.process_commands(message)

@bot.command()
async def bard(ctx, *, query):
    # Send an API request and get a response from BardAPI
    response = bardapi.core.Bard(token).get_answer(query)

    # Check if the response contains an image
    if 'images' in response and response['images']:
        image_url = response['images'].pop()
        await ctx.send(image_url)

    # Remove any [Image of ...] mention from the content
    content = response['content']
    content = re.sub(r'\[Image of [^\]]+\]', '', content)

    # Split the modified content into chunks of 2000 characters
    chunks = [content[i:i + 2000] for i in range(0, len(content), 2000)]

    # Send each chunk as a separate message
    for chunk in chunks:
        await ctx.send(chunk)

bot.run(bot_token)
