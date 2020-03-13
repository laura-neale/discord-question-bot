import os
from datetime import datetime
from time import sleep

import discord
from dotenv import load_dotenv

from questiondb import insert_question, select_question

load_dotenv() #loads the .env file environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_CHANNEL = os.getenv('DISCORD_CHANNEL')

client = discord.Client() #represents a connection to discord
channel = client.get_channel(687940638314070057)


@client.event
async def on_ready():  # when a connection to discord is established
    print(f'{client.user} has connected to Discord!')


# TODO this doesn't work multi-threaded
async def run_scheduled_questions():
    await client.wait_until_ready()
    print(f'starting schedule on channel {channel}')
    while True:
        print("checking scheduling")
        hour = datetime.now().hour
        if hour == 9 or hour == 16 or hour == 12:
            print("messaging on schedule")
            await(send_question(channel))
        sleep(600)


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


# client.loop.create_task(run_scheduled_questions())
client.run(TOKEN)  # runs the bot with the token
