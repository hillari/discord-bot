import os
from dotenv import load_dotenv
from discord.ext import commands
from helpers import is_owner

load_dotenv()  # dotenv is so we can read the following configs from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')
prefix = os.getenv('prefix')

bot = commands.Bot(command_prefix=prefix)  # creates the actual bot and assigns it a prefix


@bot.command()
async def ping(ctx):
    """Returns response time"""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def creload(ctx):
    """Bot developer Use ONLY"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.reload_extension(f"cogs.{filename[:-3]}")
            print("Reloaded: " + filename)
    # owner = os.getenv('owner')
    # if file.endswith(".py"):
    #     print("owner verified")
    #     bot.unload_extension(f"cogs.{file[:-3]}")
    #     bot.load_extension(f"cogs.{file[:-3]}")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == 'CodingGroup':
            break
    print(
        f'{bot.user} is connected to the following servers:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # commented out for brevity when testing
    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

@commands.command(name="help")
async def help(self, ctx):
    helptext = "```"
    for command in self.bot.commands:
        helptext += f"{command}\n"
    helptext += "```"
    await ctx.send(helptext)

@bot.event
async def on_message(message):
    """If the bot sees the word rude in a message, it will react with custom emoji"""
    if message.author == bot.user:
        return

    if 'rude' in message.content:
        id = 644004926296555549
        emoji = bot.get_emoji(id)
        await message.add_reaction(emoji)
    await bot.process_commands(message)  # We have to do this in order to use events and commands together


# loads all of the cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print("Loaded module: " + filename)

bot.run(TOKEN)
