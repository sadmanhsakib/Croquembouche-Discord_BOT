import discord
import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv("const.env")

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

# Getting the CONST from the .env files
USER_ID = int(os.getenv("USER_ID"))
PERSONAL_SERVER_ID = int(os.getenv("PERSONAL_SERVER_ID"))
GENERAL_CHANNEL_ID = int(os.getenv("GENERAL_CHANNEL_ID"))
STARTING_TIME_CHANNEL_ID = int(os.getenv("STARTING_TIME_CHANNEL_ID"))
DARK_HUMOR_ID = int(os.getenv("DARK_HUMOR_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
QURAN_FILE = "quran.txt"
SUNNAH_FILE = "sunnah.txt"
QUOTES_FILE = "quote.txt"
QUOTE_LIST = [QURAN_FILE, SUNNAH_FILE, QUOTES_FILE]

@client.event
# when the bot starts 
async def on_ready():
    # prints a message in console to 
    print(f"Logged in as: {client.user}")


@client.event
# when the user sends a message in server
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == client.user:
        return
    
    # command for personal server
    if message.content.startswith("-bonjour") and message.guild.id == PERSONAL_SERVER_ID:
        await message.channel.send("Guten Tag, Chef. Ich hoffe, Sie haben einen fantastischen Tag. Ich wünsche Ihnen einen schönen Tag.")

    # stores every simple reply simple_commands
    message_dict = {
        "-hello": f"Good day, {message.author.mention}. Hope you are having a wonderful day. Have a nice day. ",
        "-status": "Active."
    }

    help = "Command list:\n"
    # stores all the simple_commands name to help
    for k in message_dict.keys():
        help += f"{k}\n"
    # stores all the complex_commands name to help
    help += "-delete\n-quran\n-quote\n-sunnah"
    # adding the help section to the dict
    message_dict.update({"-help": f"{help}"})

    # replies to user messages
    for msg in message_dict:
        if message.content.startswith(msg):
            await message.channel.send(message_dict[msg])

    # deletes the necessary lines as per user request
    if message.content.startswith("-delete"):
        amount = message.content.replace("-delete ", "")
        amount = int(amount)
        # +1 to remove the command itself
        await message.channel.purge(limit=amount+1)

    if message.content.startswith("-"):
        # replying with quotes
        for x in QUOTE_LIST:
            # parsing the strings into user command style for comparing
            y = x.replace(f".txt", "")
            y = "-" + y

            if message.content == y:
                # since Bangla alpha is in unicode, we need to open the file in unicode
                with open(x, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    
                    # sending a random line from the user's desired type
                    await message.channel.send(lines[random.randint(0, (len(lines)-1))])


@client.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    counter = 0

    # getting the channel id
    general_channel = client.get_channel(GENERAL_CHANNEL_ID)
    log_channel = client.get_channel(STARTING_TIME_CHANNEL_ID)
    dark_humor_channel = client.get_channel(DARK_HUMOR_ID)
    
    # for my personal server
    if after.id == USER_ID and after.guild.id == PERSONAL_SERVER_ID:
        old_status = str(before.status)
        new_status = str(after.status)
        now = datetime.datetime.now().strftime("%Y-%m-%d -> %H:%M:%S")

        # if the user comes online
        if old_status == "offline" and new_status != "offline":
            # sends a greeting message
            await general_channel.send(f"Willkommen zurück, {after.name}.\nIch wünsche Ihnen einen schönen Tag.")

            # getting the session id from the channel message history
            async for message in log_channel.history(limit=4):
                session_id = message.content

            try:
                session_id = session_id.replace("Session #", "")
                counter = int(session_id)
                counter += 1
            # if there are no previous messages, then set counter as 1
            except UnboundLocalError:
                counter = 1

            # acquires the channel id, then sends the message
            await log_channel.send(f"Session #{counter}")
            await log_channel.send(f"Opening Time: {now}")

        # if the user goes offline
        elif old_status != "offline" and new_status == "offline":     
            msg = None
            # getting the last message from desired channel; limit = number of channel
            async for message in log_channel.history(limit=1):
                msg = message
                break
            
            active_time = ActiveTime(msg, now)
            await log_channel.send(f"Closing Time: {now}")
            await log_channel.send(f"Was Active for: {active_time}")
    # for other servers
    else:
        if old_status == "offline" and new_status != "offline":
            await dark_humor_channel.send(f"Welcome back, {after.name}.")
        elif old_status != "offline" and new_status == "offline":
            await dark_humor_channel.send(f"Bye, {after.name}.\nSee you soon! ")


def ActiveTime(msg, now):
    # getting only time from the total value
    msg = msg.content.replace(f"{msg.content[0:28]}", "")
    now = now.replace(f"{now[0:14]}", "")

    # creating a list of time by removing the ':'  
    starting_parts = msg.split(":")
    now_parts = now.split(":")

    # converting string lists to int lists
    starting_parts = list(map(int, starting_parts))
    now_parts = list(map(int, now_parts))

    duration = [0, 0, 0]

    for i in range(3):
        duration[i] = now_parts[i] - starting_parts[i]

    # parsing the duration in a string
    active_time = str(duration[0]) + " hours " + str(duration[1]) + " minutes " + str(duration[2]) + " seconds"

    return active_time

# starts the bot
client.run(BOT_TOKEN)