import json
import discord, dotenv
import config
from discord.ext import commands

countdown_dict = config.countdown_dict

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = config.prefix

    @commands.command(name="bonjour")
    async def hello(self, ctx):
        await ctx.send(f"Guten Tag, Chef. Ich hoffe, Sie haben einen fantastischen Tag. Ich wünsche Ihnen einen schönen Tag.")

    @commands.command(name="status")
    async def status(self, ctx):
        await ctx.send(f"Ich bin online. ")

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Ping: {round(self.bot.latency * 1000)} ms. ")

    @commands.command(name="list")
    async def list_countdown(self, ctx):
        await ctx.send(f"List of countdowns: {list(countdown_dict.keys())}")

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🤖 Bot Help Menu",
            description="Here are all available commands:",
            color=0x00ff00
        )

        # adding the general commands
        embed.add_field(
            name="\n📝 General Commands: ",
            value=f"`{self.prefix}bonjour` - Greets the user.\n"
            f"`{self.prefix}status` - Returns the status of the bot.\n"
            f"`{self.prefix}ping` - Returns the latency of the BOT in milliseconds.\n"
            f"`{self.prefix}list` - Returns the list of countdown names.\n",
            inline=False,
        )

        # adding the complex commands
        embed.add_field(
            name="\n🧩 Complex Commands (Takes Arguments): ",
            value=f"`{self.prefix}del number_of_messages_to_delete` - Deletes the number of messages given.\n"
            f"`{self.prefix}add countdown NAME DATE(%Y-%m-%d)` - Adds a countdown for daily pinging.\n"
            f"`{self.prefix}rmv countdown NAME` - Removes a countdown.\n"
            f"`{self.prefix}set VARIABLE VALUE` - Sets the value of the BOT config variable to the given value.\n",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="del")
    async def delete_messages(self, ctx, *, message: str=''):
        try:
            if message == '':
                raise Exception

            # extracting the data from the message
            amount = int(message)
            # +1 to remove the command itself
            await ctx.channel.purge(limit=amount+1)
        except:
            await ctx.send(f"Invalid command. Correct Syntax: `{self.prefix}del number_of_messages_to_delete` ")

    @commands.command(name="add")
    async def add(self, ctx, *, message: str=''):
        try:
            if message == '':
                raise Exception

            # extracting the data from the messages
            parts = message.split(' ')
            name = parts[1]
            date = parts[2]

            # adding the countdown to the dictionary
            countdown_dict.update({name: date})

            # dumping the whole dictionary in string format
            updated = json.dumps(countdown_dict)

            # saving the dictionary to the .env file
            dotenv.set_key(".env", "COUNTDOWN_DATES", updated)

            await ctx.send(f"Successfully added countdown. {name}: {date}")
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{self.prefix}add countdown NAME DATE(%Y-%m-%d)`")

    @commands.command(name="rmv")
    async def remove(self, ctx, *, message: str=''):
        try:
            if message == '':
                raise Exception

            # extracting the data from the messages
            parts = message.split(' ')
            name = parts[1]

            # removing the countdown from the dictionary
            countdown_dict.pop(name)

            # dumping the whole dictionary in string format
            updated = json.dumps(countdown_dict)

            # saving the dictionary to the .env file
            dotenv.set_key(".env", "COUNTDOWN_DATES", updated)

            await ctx.send(f"Successfully removed {name} countdown from storage.")
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{self.prefix}rmv countdown NAME`")

    @commands.command(name="set")
    async def set(self, ctx, *, message: str=''):
        try:
            if message == '':
                raise Exception

            # extracting the data from the messages
            parts = message.split(' ')
            variable = parts[0].upper()
            value = parts[1]

            shouldUpdate = False

            match variable:
                case "PREFIX":
                    config.prefix = value
                    shouldUpdate = True
                case "STARTING_TIME_CHANNEL_ID":
                    config.starting_time_channel_id = int(value)
                    shouldUpdate = True
                case "COUNTDOWN_CHANNEL_ID":
                    config.starting_time_channel_id = int(value)
                    shouldUpdate = True

            if shouldUpdate:
                # updating the .env file
                dotenv.set_key(".env", variable, value)
                await ctx.send(f"Successful. {variable} set to {value}")
            else:
                await ctx.send(
                    f"Variable not found. Available variables are: PREFIX, STARTING_TIME_CHANNEL_ID, COUNTDOWN_CHANNEL_ID"
                )
        except:
            await ctx.send(
                f"Invalid. Correct Syntax: `{self.prefix}set VARIABLE VALUE`"
            )

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
