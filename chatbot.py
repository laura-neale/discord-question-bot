import os
from datetime import datetime
from time import sleep

import discord
from dotenv import load_dotenv
import asyncio

from questiondb import insert_question, select_question

load_dotenv() #loads the .env file environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL'))

client = discord.Client() #represents a connection to discord

schedule_hours = [9, 16]

@client.event
async def on_ready():  # when a connection to discord is established
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(run_scheduled_questions())


# TODO this doesn't work multi-threaded
async def run_scheduled_questions():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    print(f'starting schedule on channel {channel}')
    while not client.is_closed():
        now = datetime.now()
        if now.minute == 5 and now.hour in schedule_hours:
                print("messaging on schedule")
                await(send_question(channel))
        await(asyncio.sleep(60))


@client.event
async def on_message(message):
    text = message.content.lower()
    if message.author == client.user:
        # it's from a bot, don't react
        return
    elif text == "hey bot":
        print("message received")
        await(send_question(message.channel))
    elif text.startswith("set schedule:"):
        hours_as_string = text.split(":")[1]
        global schedule_hours
        schedule_hours = [int(h.strip()) for h in hours_as_string.split(",")]
        print(f'setting schedule to: {schedule_hours}')
        await message.channel.send(f"got it, I'll run at {schedule_hours}")
    elif isinstance(message.channel, discord.DMChannel):
        print("DM received")
        if "?" in text:
            insert_question(message.content)
            await(message.channel.send("Ok, I've added that to my list"))
        else:
            await(message.channel.send("I don't understand that. If you want to add a question to the list, include a ? in it"))


async def send_question(channel):
    print("sending message")
    response = select_question()
    await(channel.send(response))

client.run(TOKEN)  # runs the bot with the token
