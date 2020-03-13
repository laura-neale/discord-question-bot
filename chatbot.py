import os
import random

import discord
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

load_dotenv() #loads the .env file environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client() #represents a connection to discord

@client.event
async def on_ready(): #when a connection to discord is established
    # print("Hello")
    print(f'{client.user} has connected to Discord!')

    # while True:
    #     if datetime.now().hour == 9:
    #         send_message()
    #         sleep(600)
    #


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    questions = [
        "What's your favourite podcast?",
        "What's one of your hobbies?",
        "What's the most interesting place you've been?",
        "What's one thing you admire about a co-worker?"
    ]
    if message.content == "hey bot":
        response = random.choice(questions)
        await (message.channel.send(response))


client.run(TOKEN) #runs the bot with the token