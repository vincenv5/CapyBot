import logging
import os
import discord
import asyncio
from pathlib import Path
from json import load
from discord.ext import commands
from dotenv import load_dotenv
from .joke import get_full_joke
from .quote_scraper import get_quotes


# setting up global constants, file, intents, and environment variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord_bot\\bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
comm_prefix = '!'


# This establishes the bot with the command prefix, intents, log, and logging level
client = commands.Bot(command_prefix=comm_prefix, intents=intents, log_handler=handler, log_level=logging.DEBUG)


def run_bot():
    client.run(token)


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


#----------------------------------------Commands----------------------------------------#
# The commands will run once it detects when the user sends a message that includes the command prefix
# followed by the command phrase (i.e the name of the functions that are described below)

@client.command()
async def joke(ctx):
    """Command to get a joke. Will send a setup line, followed by
    a punchline a couple seconds later"""
    # Call to get a generator for the setup and punchline
    joke = get_full_joke()

    # First yield will get the setup, while the second yield will
    # get the punchline
    setup = next(joke)
    punchline = next(joke)

    # When te joke command is received, the bot will send the setup,
    # wait a couple seconds, and then send the punchline
    await ctx.send(setup)
    await asyncio.sleep(2)
    await ctx.send(punchline)


@client.command()
async def quote(ctx) -> None:
    """
    This command will allow the user to have the bot post a quote within a chat. 
    It does not return anything, but does create a json file 'quotes.json' inside the discord_bot
    folder that stores scraped quotes.
    """
    async def _print_quotes():
        """Helper function to open the 'quotes.json' file that contains JSON payloads of quotes,
        format the f-string for the quote, and send it to the msg section."""
        with open(Path('discord_bot\\quotes.json')) as file:
            quotes = load(file)
            for quote in quotes:
                formatted_quote = f"{quote["quote"]}\n"\
                                    f"\t-{quote["author"]}"

                await ctx.send(formatted_quote)

    try:
    # Opens 'quotes.json' and load quotes from JSON into Python dictionary form.
    # For every quote within the file, will format each
        await _print_quotes()

    except FileNotFoundError:
        # Calls the quote_scraper to scrape quotes from 'https://quotes.toscrape.com/'
        # from an asyncio event loop to not block the discord bot's event loop
        # and creates a 'quotes.json' file
        quote_loop = asyncio.get_event_loop()
        await quote_loop.run_in_executor(None, get_quotes)

        # Recalls '_print_quotes' 
        await _print_quotes()


__all__ = ["run_bot"]


if __name__ == "__main__":
    run_bot()