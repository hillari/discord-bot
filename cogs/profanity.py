import discord
from discord.ext import commands
from helpers import *


class Profanity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Profanity(bot))