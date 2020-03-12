import asyncio
import datetime
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
    async def msgcount(self, ctx, channel: discord.TextChannel=None):
        """Total messages sent per channel. Channel arg is optional"""
        channel = channel or ctx.channel
        count = 0
        async for _ in channel.history(limit=None):
            count += 1
        await ctx.send("There have been {} messages in {}".format(count, channel.mention))

    @commands.command()
    async def umsgcount(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
        """Messages per channel per user. optional args: <member> <channel> """
        count = 0
        channel = channel or ctx.channel
        member = member or ctx.message.author
        if member is None:  # No user arg give 
            async for message in channel.history(limit=None):
                if message.author == ctx.message.author:
                    count += 1
            await ctx.send("You've sent {} messages in {}".format(count, channel))
        else:
            async for message in channel.history(limit=None):
                if message.author == member:
                    count += 1
            await ctx.send(member.display_name + " has sent {} messages in {}".format(count, channel.mention))

    @commands.command()
    async def prefix(self, ctx):
        """Returns the current prefix. Kinda useless"""
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
    # @commands.has_role('Bot Dev 🤖')
    @commands.cooldown(1, 10, commands.BucketType.user)  # Don't let normies spam our bot
    async def say(self, ctx, *, arg):
        """Make bot say something e.g. say <text>"""
        print(datetime.datetime.now(), "", ctx.message.author, "used say command in", ctx.message.channel,
              ".Output:\n  message: ", arg, file=open("command-logs.txt", "a"))
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    async def setstatus(self, ctx, *, status):
        """Sets Bot Status e.g. setstatus <status>"""
        game = discord.Game(status)
        print(datetime.datetime.now(), "", ctx.message.author, "used setstatus command in", ctx.message.channel,
              ".Output:\n  message: ", status, file=open("command-logs.txt", "a"))
        await ctx.message.delete()
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot):
    bot.add_cog(Responses(bot))
