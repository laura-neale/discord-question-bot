import os
from datetime import datetime
from time import sleep

import discord
from dotenv import load_dotenv
import asyncio

from questiondb import insert_question, select_question

load_dotenv() #loads the .env file environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client() #represents a connection to discord
channel_id = os.getenv('DISCORD_CHANNEL')
DEFAULT_CHANNEL = client.get_channel(687940638314070057)

print(channel_id)
print(DEFAULT_CHANNEL)


@client.event
async def on_ready():  # when a connection to discord is established
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(run_scheduled_questions())


# TODO this doesn't work multi-threaded
async def run_scheduled_questions():
    await client.wait_until_ready()
    print(f'starting schedule on channel {DEFAULT_CHANNEL}')
    while not client.is_closed():
        print("checking scheduling")
        hour = datetime.now().hour
        if hour == 9 or hour == 16 or hour == 14:
            print("messaging on schedule")
            await(send_question(DEFAULT_CHANNEL))
        await(asyncio.sleep(60))


@client.event
async def on_message(message):
    if message.author == client.user:
        # it's from a bot, don't react
        return
    elif message.content.lower() == "hey bot":
        print("message received")
        await(send_question(message.channel))
    elif isinstance(message.channel, discord.DMChannel):
        print("DM received")
        insert_question(message.content)
        await(message.channel.send("Ok, I've added that to my list"))


async def send_question(channel):
    print("sending message")
    response = select_question()
    await(channel.send(response))


client.run(TOKEN)  # runs the bot with the token
