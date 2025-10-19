import datetime
import discord
import config
from discord.ext import commands

# for running the bot as a web
from keep_alive import keep_alive
keep_alive()

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True
intents.members = True

# Getting the data from the config.py
USER_ID = config.USER_ID
BOT_TOKEN = config.BOT_TOKEN
countdown_dict = config.countdown_dict
TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"

def get_prefix(bot, message):
    return config.prefix

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

@bot.event
# when the bot starts
async def on_ready():
    #loading the command script
    await bot.load_extension("bot_commands")

    # prints a message in console when ready
    print(f"✅Logged in as: {bot.user}")


@bot.event
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == bot.user:
        return

    # processing the commands
    await bot.process_commands(message)


@bot.event
async def on_presence_update(before, after):
    starting_time_channel_id = config.starting_time_channel_id
    countdown_channel_id = config.countdown_channel_id
    
    # defining the timezone
    offset = datetime.timedelta(hours=6)

    # getting the current time
    now = datetime.datetime.now(datetime.timezone(offset, name="GMT +6")).strftime(TIME_FORMAT)
    counter = 0

    # getting the channel id
    log_channel = bot.get_channel(starting_time_channel_id)
    countdown_channel = bot.get_channel(countdown_channel_id)
    
    # checking if it's the user or other members
    if after.id == USER_ID:
        old_status = str(before.status)
        new_status = str(after.status)

        # if the user comes online
        if old_status == "offline" and new_status != "offline":
            try:
                # getting the session id from the channel message history
                async for message in log_channel.history(limit=4):
                    session_id = message.content.replace("Session #", "")
                    
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
                last_msg_date = str(message.created_at + datetime.timedelta(hours=6)).split(' ')[0]

            # if the last countdown reminder wasn't sent on a date
            if last_msg_date != today:
                countdown_counter = 0
                
                # sends a message for each countdowns
                for key in countdown_dict.keys():
                    countdown_counter += 1
                    time_left = time_difference(today, countdown_dict[key])
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
    # if starting contains time too
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
bot.run(BOT_TOKEN)
