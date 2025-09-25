import discord
import datetime
import random
import os
import dotenv
import json

# keeps the bot alive
from keep_alive import keep_alive
keep_alive()

dotenv.load_dotenv(".env")
# config stores all the values inside the .env file
config = dotenv.dotenv_values(".env")

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

# Getting the CONST from the .env files
USER_ID = int(os.getenv("USER_ID"))
GENERAL_CHANNEL_ID = int(os.getenv("GENERAL_CHANNEL_ID"))
STARTING_TIME_CHANNEL_ID = int(os.getenv("STARTING_TIME_CHANNEL_ID"))
COUNTDOWN_CHANNEL_ID = int(os.getenv("COUNTDOWN_CHANNEL_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"
QURAN_FILE = "quran.txt"
SUNNAH_FILE = "sunnah.txt"
QUOTES_FILE = "quote.txt"
QUOTE_LIST = [QURAN_FILE, SUNNAH_FILE, QUOTES_FILE]

# getting the countdown dictionary from the .env file
COUNTDOWN_DATES = config.get("COUNTDOWN_DATES")
countdown = json.loads(COUNTDOWN_DATES)


@client.event
# when the bot starts 
async def on_ready():
    # prints a message in console when ready
    print(f"Logged in as: {client.user}")


@client.event
# when the user sends a message in server
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == client.user:
        return
    
    # stores every simple reply simple_commands
    message_dict = {
        "-bonjour": f"Guten Tag, Chef. Ich hoffe, Sie haben einen fantastischen Tag. Ich wünsche Ihnen einen schönen Tag.",
        "-status": "Active."
    }

    help = "Command list:\n"
    # stores all the simple_commands name in help
    for k in message_dict.keys():
        help += f"{k}\n"
    # stores all the complex_commands name in help
    help += "-del\n-quran\n-quote\n-sunnah"
    # adding the help section to the dict
    message_dict.update({"-help": f"{help}"})

    # replies to user messages
    for msg in message_dict:
        if message.content.startswith(msg):
            await message.channel.send(message_dict[msg])

    # deletes the necessary lines as per user request
    if message.content.startswith("-del"):
        try:
            amount = message.content.replace("-del ", "")
            amount = int(amount)

            # +1 to remove the command itself
            await message.channel.purge(limit=amount+1)
        except Exception as error:
            await message.channel.send("Invalid Argument!\nCorrent syntax: -del<space>[Number of Messages to Remove].")

    if message.content.startswith("-"):
        # replying with quotes
        for x in QUOTE_LIST:
            # parsing the strings into user command style for comparing
            y = x.replace(f".txt", "")
            y = "-" + y

            if message.content == y:
                # since Bengali alphabet is in unicode, we need to open the file in unicode
                with open(x, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    
                    # sending a random line from the user's desired type
                    await message.channel.send(lines[random.randint(0, (len(lines)-1))])


@client.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    now = datetime.datetime.now().strftime(TIME_FORMAT)
    counter = 0

    # getting the channel id
    general_channel = client.get_channel(GENERAL_CHANNEL_ID)
    log_channel = client.get_channel(STARTING_TIME_CHANNEL_ID)
    countdown_channel = client.get_channel(COUNTDOWN_CHANNEL_ID)
    
    # checking if it's the user or other members
    if after.id == USER_ID:
        old_status = str(before.status)
        new_status = str(after.status)

        # if the user comes online
        if old_status == "offline" and new_status != "offline":
            # sends a greeting message
            await general_channel.send(f"Willkommen zurück, {after.name}.\nIch wünsche Ihnen einen schönen Tag.")
            
            try:
                # getting the session id from the channel message history
                async for message in log_channel.history(limit=4):
                    session_id = message.content
                session_id = session_id.replace("Session #", "")
                counter = int(session_id)
                counter += 1
            # if there are no previous messages, then set counter as 1
            except UnboundLocalError:
                counter = 1
            
            # acquires the channel id, then sends the message
            await log_channel.send(f"Session #{counter}")
            await log_channel.send(f"Opening Time: {now}")

            last_msg_date = ""
            today = now.split(' ')[0]
            # getting the last time when a message was send in countdown channel
            async for message in countdown_channel.history(limit=1): 
                # getting the date from the message creation time
                last_msg_date = str(message.created_at).split(' ')[0]

            # if the last countdown reminder wasn't sent on a date
            if last_msg_date != today:
                countdown_counter = 0
                # reminds the user about the countdown's
                for key in countdown.keys():
                    counter += 1
                    time_left = time_difference(now, countdown[key])
                    await countdown_channel.send(f"Countdown-{countdown_counter} -> {key}: {time_left}")

        # if the user goes offline
        elif old_status != "offline" and new_status == "offline":     
            msg = None
            # getting the last message from desired channel; limit = number of channel
            async for message in log_channel.history(limit=1):
                msg = message
                break
            
            # getting the duration
            msg_parts = msg.content.split(' ')
            msg_time = msg_parts[-1]
            msg_date = msg_parts[-3]
            time = f"{msg_date} -> {msg_time}"
            active_time = time_difference(time, now)

            await log_channel.send(f"Closing Time: {now}")
            await log_channel.send(f"Was Active for: {active_time}")


def time_difference(starting, now):
    # converting the time in datetime
    time1 = datetime.datetime.strptime(starting, TIME_FORMAT)
    time2 = datetime.datetime.strptime(now, TIME_FORMAT)
    duration = time2 - time1

    # making the time difference more readable
    duration = str(duration).split(':')
    active_time = f"{duration[0]} hours {duration[1]} minutes {duration[2]} seconds"

    return active_time


# starts the bot
client.run(BOT_TOKEN)