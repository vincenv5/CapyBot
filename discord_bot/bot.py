import logging
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
comm_prefix = '!'

client = commands.Bot(command_prefix=comm_prefix, intents=intents, log_handler=handler, log_level=logging.DEBUG)

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


@client.command()
async def weather(ctx, msg):
    await ctx.send(f"weather {msg}")


if __name__ == "__main__":
    client.run(token)