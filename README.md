## What is it?

A chat bot reminding us to talk to each other during the quarantine

It posts randomly selected questions on a schedule, and in response to user messages 

## running it

It runs against a devserver-hosted database of questions, and 'randomly' selects one, preferring user-submitted submitted questions to non-user-submitted ones, and questions that haven't been asked recently over questions that were.

It uses a .env file with, and needs the properties "DISCORD_CHANNEL" and "DISCORD_TOKEN"

## how to use it

**get a question**: type 'hey bot'

**change the schedule**: type `set schedule: ` followed by a comma-separated list of the hours it should post at, e.g. `set schedule: 10, 15, 18` (e.g. for 10 am, 3 pm and 6 pm)'

**submit a question**: dm the bot with your question. Note: anything you dm the bot with will be considered a question.
