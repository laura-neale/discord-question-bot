import _thread
import os
import random
import asyncio

import discord
import psycopg2 as psycopg2
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

from psycopg2 import sql

load_dotenv() #loads the .env file environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_CHANNEL = os.getenv('DISCORD_CHANNEL')

client = discord.Client() #represents a connection to discord

def get_a_question():
    conn = psycopg2.connect(host="doris.devserver0.btn1.bwcom.net", database="brandwatch-crawler.db",  user="brandwatch")
    cur = conn.cursor()
    cur.execute("SELECT question FROM discord_chatbot_questions ORDER BY last_asked DESC, user_submitted DESC, question")
    qs = cur.fetchone()
    question = qs[0]
    cur.execute("UPDATE discord_chatbot_questions SET last_asked = now() WHERE question = %s", (question,))
    conn.commit()
    cur.close
    return question


questions = get_a_question()

@client.event
async def on_ready(): #when a connection to discord is established
    print(f'{client.user} has connected to Discord!')

    #currently doesnt' work
    # await run_scheduled_questions()


async def run_scheduled_questions():
    await client.wait_until_ready()
    channel = client.get_channel(687940638314070057)
    print(f'starting schedule on channel {channel}')
    while True:
    #while not client.is_closed:
        print("checking scheduling")
        hour = datetime.now().hour
        if hour == 9 or hour == 16 or hour == 12:
            print("messaging on schedule")
            await(send_message(channel))
        sleep(600)


@client.event
async def on_message(message):
    if message.author != client.user and message.content.lower() == "hey bot":
        print("message received")
        await(send_message(message.channel))


async def send_message(channel):
    print("sending message")
    response = get_a_question()
    await(channel.send(response))


client.loop.create_task(run_scheduled_questions())
client.run(TOKEN) #runs the bot with the token
