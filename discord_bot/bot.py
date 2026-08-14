import logging
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from joke import get_full_joke


# setting up global constants, file, intents, and environment variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord_bot\\bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
comm_prefix = '!'


# This establishes the bot with the command prefix, intents, log, and logging level
client = commands.Bot(command_prefix=comm_prefix, intents=intents, log_handler=handler, log_level=logging.DEBUG)


"""The client.events are what the bot will look out for."""
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await client.process_commands(message)


"""The commands will run once it detects when the user sends a message that includes the command prefix
   followed by the command phrase (i.e the name of the functions that are described below)"""
@client.command()
async def joke(ctx):
    await ctx.send(get_full_joke())


@client.command()
async def guide(ctx):
    return 0


if __name__ == "__main__":
    client.run(token)