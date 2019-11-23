import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
owner = os.getenv('owner')


def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)
