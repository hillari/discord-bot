import asyncio
import random
import os
import discord
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
    async def joined(self, ctx, member: discord.Member = None):
        """When member joined the server. e.g. joined <optional: @user>"""
        if member is None:
            await ctx.send('{0.name} joined in {0.joined_at}'.format(ctx.message.author))
        else:
            await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command()
    async def hello(self, ctx):
        """Greets you"""
        await ctx.send('Hello, {0.author.mention} , I see you!'.format(ctx))

    @commands.command()
    async def membercount(self, ctx):
        """Displays Total Number of Users in the Server"""
        id = self.bot.get_guild(ctx.message.guild.id)
        await ctx.message.delete()
        await ctx.send(f"""{id.member_count}""" + " members in the server")

    @commands.command()
    # @commands.has_role('Grader People')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def say(self, ctx, *, arg):
        """Says what you want it to e.g. say <text>"""
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    #@commands.has_role("Grader People")
    async def setstatus(self, ctx, *, status):
        """Sets Bot Status e.g. setstatus <status>"""
        game = discord.Game(status)
        await ctx.message.delete()
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot):
    bot.add_cog(Responses(bot))
