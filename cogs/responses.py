import asyncio
import random
import os

import aiohttp
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()


class Responses(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx):
        """Returns the current prefix"""
        prefix = os.getenv('prefix')
        await ctx.send("The current prefix is: " + prefix)

    @commands.command()
    async def hello(self, ctx):
        """Greets you"""
        await ctx.send('Hello, {0.author.mention} , I see you!'.format(ctx))





def setup(bot):
    bot.add_cog(Responses(bot))
