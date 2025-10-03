import discord
import datetime
import random
import os
import dotenv
import json
import sys

# keeps the bot alive
from keep_alive import keep_alive
keep_alive()

dotenv.load_dotenv(".env")

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

# Getting the data from the .env files
USER_ID = int(os.getenv("USER_ID"))
GENERAL_CHANNEL_ID = int(os.getenv("GENERAL_CHANNEL_ID"))
STARTING_TIME_CHANNEL_ID = int(os.getenv("STARTING_TIME_CHANNEL_ID"))
COUNTDOWN_CHANNEL_ID = int(os.getenv("COUNTDOWN_CHANNEL_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
initial = os.getenv("INITIAL")

TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"
QUOTES = ["quran.txt", "sunnah.txt", "quote.txt"]

# getting the countdown dictionary from the .env file
countdown_dict = json.loads(os.getenv("COUNTDOWN_DATES"))


@client.event
# when the bot starts 
async def on_ready():
    # prints a message in console when ready
    print(f"Logged in as: {client.user}")


@client.event
# when the user sends a message in server
async def on_message(message):
    global initial
    
    # prevents the bot from replying on its own messages
    if message.author == client.user:
        return
    
    # stores every simple reply simple_commands
    message_dict = {
        f"{initial}bonjour": f"Guten Tag, Chef. Ich hoffe, Sie haben einen fantastischen Tag. Ich wünsche Ihnen einen schönen Tag.",
        f"{initial}status": "Active."
    }

    help = f"""```Command list:
{initial}bonjour
{initial}status
{initial}del number_of_messages_to_delete
{initial}add NAME TIME(%Y-%m-%d)
{initial}rmv NAME
{initial}set VARIABLE VALUE
{initial}randomline quran/sunnah/quote```"""

    # adding the help section to the dict
    message_dict.update({f"{initial}help": help})

    # replies to user messages
    for msg in message_dict:
        if message.content.startswith(msg):
            await message.channel.send(message_dict[msg])

    # deletes previous messages as per user request
    if message.content.startswith(f"{initial}del"):
        try:
            # extracting the data from the use input
            parts = message.content.split(' ')
            amount = int(parts[1])

            # +1 to remove the command itself
            await message.channel.purge(limit=amount+1)
        except:
            await message.channel.send(f"Invalid command. Correct Syntax: `{initial}del number_of_messages_to_delete` ")

    # adds an item to the dictionary
    elif message.content.startswith(f"{initial}add"):
        try:
            # extracting the data from the messages
            parts = message.content.split(' ')
            name = parts[1]
            time = parts[2]

            # adding the countdown to the dictionary
            countdown_dict.update({name: time})
            
            # dumping the whole dictionary in string format
            updated = json.dumps(countdown_dict)
            
            # saving the dictionary to the .env file
            dotenv.set_key(".env", "COUNTDOWN_DATES", updated)

            await message.channel.send(f"Successfully added countdown. {name}: {time}")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}add NAME TIME(%Y-%m-%d)`")
    
    # removes an item from the dictionary
    elif message.content.startswith(f"{initial}rmv"):
        try:
            # extracting the data from the messages
            parts = message.content.split(' ')
            name = parts[1]

            # removing the countdown from the dictionary
            countdown_dict.pop(name)
            
            # dumping the whole dictionary in string format
            updated = json.dumps(countdown_dict)
            
            # saving the dictionary to the .env file
            dotenv.set_key(".env", "COUNTDOWN_DATES", updated)

            await message.channel.send(f"Successfully removed {name} countdown from storage.")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}rmv NAME`")

    # send a randomline as per user request
    elif message.content.startswith(f"{initial}randomline"):
        try:
            # extracting the data from user message
            parts = message.content.split(' ')
            item_name = parts[1]
            file_name = item_name + ".txt"

            if file_name in QUOTES:
                # since Bengali alphabet is in unicode, we need to open the file in unicode
                with open(file_name, 'r', encoding="utf-8") as file:
                    lines = file.readlines()
            
                    # sending a random line from the user's desired type
                    await message.channel.send(lines[random.randint(0, (len(lines)-1))])
            else:
                await message.channel.send(f"{item_name} not found. Available files are: {QUOTES}")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}randomline quran/sunnah/quote`")
    
    # changes bot settings
    elif message.content.startswith(f"{initial}set"):
        try:
            # extracting the data from the message
            parts = message.content.split(' ')
            variable = parts[1]
            value = parts[2]

            match variable:
                case "INITIAL":
                    initial = value
        
                    # updating the .env file
                    dotenv.set_key(".env", variable, value)
            
            await message.channel.send(f"Successful. {variable} set to {value}")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}set VARIABLE VALUE`")

    # replies with the list of available items as per user request
    elif message.content.startswith(f"{initial}list"):
        try:
            await message.channel.send(f"```Available Countdowns: \n{list(countdown_dict.keys())}```")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}list countdown`")
            

@client.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    # defining the timezone
    offset = datetime.timedelta(hours=6)

    # getting the current time for the desired timezone
    now = datetime.datetime.now(datetime.timezone(offset, name="GMT +6")).strftime(TIME_FORMAT)
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
                for key in countdown_dict.keys():
                    countdown_counter += 1
                    time_left = time_difference(now, countdown_dict[key])
                    await countdown_channel.send(f"Countdown-{countdown_counter} -> {key}: {time_left}")

        # if the user goes offline
        elif old_status != "offline" and new_status == "offline":     
            msg = None
            # getting the last message from desired channel; limit = number of channel
            async for message in log_channel.history(limit=1):
                msg = message
            
            # extracting the data from the message
            msg_parts = msg.content.split(' ')
            msg_time = msg_parts[-1]
            msg_date = msg_parts[-3]
            time = f"{msg_date} -> {msg_time}"
            
            active_time = time_difference(time, now)

            await log_channel.send(f"Closing Time: {now}")
            await log_channel.send(f"Was Active for: {active_time}")


def time_difference(starting, now):
    # if  starting contains time too
    if len(starting.split(' ')) == 3:
        # converting the time in datetime
        time1 = datetime.datetime.strptime(starting, TIME_FORMAT)
        time2 = datetime.datetime.strptime(now, TIME_FORMAT)
        duration = time2 - time1

        # making the time difference more readable
        duration = str(duration).split(':')
        active_time = f"{duration[0]} hours {duration[1]} minutes {duration[2]} seconds"
    else:
        # converting the time in datetime
        time1 = datetime.datetime.strptime(starting, "%Y-%m-%d")
        time2 = datetime.datetime.strptime(now.split(' ')[0], "%Y-%m-%d")
        duration = time2 - time1

        # writing only remaining days as time is unavailable
        active_time = str(duration.days) + " days"

    return active_time

# starts the bot
client.run(BOT_TOKEN)
