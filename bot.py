from helpers import *
import os
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()  # dotenv is so we can read the following configs from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')
prefix = os.getenv('prefix')

bot = commands.Bot(command_prefix=prefix)  # creates the actual bot and assigns it a prefix

first_run = 0  # Hacky method to avoid initializing the db each time without commenting out code


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == 'CodingGroup':
            break
    if first_run == 1:
        init_all_users(bot)

    print(
        f'{bot.user} is connected to the following servers:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # commented out for brevity when testing
    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')


@bot.command()
async def ping(ctx):
    """Returns response time"""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@commands.has_role('Grader People')
@bot.command()
async def creload(ctx):
    """For Hillari ONLY (sorry normies)"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.reload_extension(f"cogs.{filename[:-3]}")
            print("Reloaded: " + filename)
    await ctx.send("Reloaded cogs")


@commands.has_role('Grader People')
@bot.command(name="cquit")
async def bot_quit(ctx):
    """Bot Creator Use ONLY"""
    await ctx.send("Shutting down...\n\U0001f44b")
    await bot.logout()


@commands.command(name="help")
async def help(self, ctx):
    helptext = "```"
    for command in self.bot.commands:
        helptext += f"{command}\n"
    helptext += "```"
    await ctx.send(helptext)


# @bot.event
# async def on_message(message):
#     """If the bot sees the word rude in a message, it will react with custom emoji"""
#     if message.author == bot.user:
#         return
#
#     if 'rude' in message.content:
#         id = 644004926296555549
#         emoji = bot.get_emoji(id)
#         await message.add_reaction(emoji)
#     await bot.process_commands(message)  # We have to do this in order to use events and commands together


@bot.event
async def on_message(message):
    """If the bot sees the words good bot it will respond *MOVE THIS*"""
    if message.author == bot.user:
        return
    if 'good bot' in message.content:
        # emojid = 647707023869476874
        # emoj = bot.get_emoji(emojid)
        # await message.add_reaction(emoj)
        await message.channel.send("Awww thanks. I try")
    await bot.process_commands(message) # We have to do this in order to use events and commands together

# loads all of the cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print("Loaded module: " + filename)

bot.run(TOKEN)
