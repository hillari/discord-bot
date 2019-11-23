import discord
from discord.ext import commands
from helpers import *

bot = commands.Bot(command_prefix='.')


class User_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def new_user_dm(self, member):
        msg = "Welcome to our awesome server!"
        await member.send(msg)  # Will send a DM to the member

    @commands.Cog.listener()
    async def on_member_join(self, member):
        get_member(member, member.guild)  # This function also contains code to add the member
        await self.new_user_dm(member)


def setup(bot):
    bot.add_cog(User_manager(bot))