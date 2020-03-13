import asyncio
import os
from datetime import datetime

import discord
from dotenv import load_dotenv

from questiondb import insert_question, select_question

# load the .env file, and the variables in it
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL'))

client = discord.Client()  # represents a connection to discord

schedule_hours = [9, 16]  # hours of the day, 0 to 23
schedule_days = [1, 2, 3, 4, 5]  # ISO week days


@client.event
async def on_ready():  # when a connection to discord is established
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(run_scheduled_questions())


async def run_scheduled_questions():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    print(f'starting schedule on channel {channel}')
    while not client.is_closed():
        now = datetime.now()
        if now.minute == 5 and now.hour in schedule_hours and now.isoweekday() in schedule_days:
            print("messaging on schedule")
            await(send_question(channel))
        await(asyncio.sleep(60))


@client.event
async def on_message(message): # when a message is sent, in any channel or a dm to the bot
    text = message.content.lower()
    if message.author == client.user:
        # it's from a bot, don't react
        return
    elif text == "hey bot":
        print("message received")
        await(send_question(message.channel))
    elif text.startswith("set schedule:"):
        await set_schedule(message)
    elif isinstance(message.channel, discord.DMChannel):
        await process_dm(message)


async def process_dm(message):
    print("DM received")
    if "?" in message.content:
        insert_question(message.content)
        await(message.channel.send("Ok, I've added that to my list"))
    else:
        await(message.channel.send("I don't understand that. If you want to add a question to the list, include a ? in it"))


async def set_schedule(message):
    global schedule_hours

    hours_as_string = message.content.split(":")[1]
    schedule_hours = [int(h.strip()) for h in hours_as_string.split(",")]

    print(f'setting schedule to: {schedule_hours}')
    await message.channel.send(f"got it, I'll run at {schedule_hours}")


async def send_question(channel):
    print("sending message")
    response = select_question()
    await(channel.send(response))


client.run(TOKEN)  # runs the bot with the token
