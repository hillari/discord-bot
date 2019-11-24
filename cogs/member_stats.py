import discord
from helpers import *
from discord.ext import commands

class Member_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def add_reputation(self, member, guild, reputation: int):
        connection = db_connect()
        member_info = get_member(member, guild)
        mycursor = connection.cursor()

        new_reputation = member_info[6] + reputation
        sql = "UPDATE members SET reputation=%s WHERE discord_id=%s"
        mycursor.execute(sql, (new_reputation, member.id))
        connection.commit()
        try:
            print("[*] Updated user %s reputation points from %s to "
                  "%s." % (member.name, member_info[6], new_reputation))
        except Exception as e:
            print("[-] Error updating reputation for %s; %s" % (member.id, e))

    @commands.command()
    async def checkrep(self, ctx, member: discord.Member):
        member_info = get_member(member, ctx.message.guild)

        embedded = discord.Embed()
        embedded.set_footer(text="CS bot made by Hillari")
        icon_str = str(member.avatar_url)
        icon_addr = icon_str.split('.w', 1)
        author_icon_str = str(self.bot.user.avatar_url)
        author_icon = author_icon_str.split('.w', 1)
        embedded.set_author(name="Reputation stats for: " + member.display_name, icon_url=author_icon[0])
        embedded.set_thumbnail(url=icon_addr[0])
        embedded.add_field(name="Rep", value=member_info[6], inline=True)
        await ctx.send(embed=embedded)

    @commands.command()
    async def takerep(self, ctx, member: discord.Member):
        member_info = get_member(member, ctx.message.guild)
        reputation = member_info[6]
        if ctx.message.author.id == member.id:
            await ctx.send("You can't take reputation points from yourself, fool!")
            return
        if reputation <= 0:
            await ctx.send(str(member.display_name) + " doesn't have any rep points to take!")
            reputaion = 0
        else:
            self.add_reputation(member, ctx.message.guild, -1)
            await ctx.send("Took a reputation point from " + str(member.display_name) + " !")

    @commands.command()
    async def giverep(self, ctx, member: discord.Member):
        """Gives Rep to a specified user e.g. giverep <@user>. Cannot be yourself."""
        if ctx.message.author.id == member.id:
            await ctx.send("You can't give yourself reputation points, fool!")
            return
        await ctx.send("Gave " + "<@!" + str(member.id) + ">" + " 1 reputation point!")
        self.add_reputation(member, ctx.message.guild, 1)


def setup(bot):
    bot.add_cog(Member_stats(bot))
