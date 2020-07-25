import discord
from helpers import *
from discord.ext import commands


class Member_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def add_reputation(self, member, guild, reputation: int):
        """Gives specified user reputation point"""
        connection = db_connect()
        member_info = get_member(member, guild)
        mycursor = connection.cursor()

        new_reputation = member_info[5] + reputation
        sql = "UPDATE members SET reputation=%s WHERE discord_id=%s"
        mycursor.execute(sql, (new_reputation, member.id))
        connection.commit()
        try:
            print("[*] Updated user %s reputation points from %s to "
                  "%s." % (member.name, member_info[5], new_reputation))
        except Exception as e:
            print("[-] Error updating reputation for %s; %s" % (member.id, e))

    # @commands.Command()
    # async def rank(self, ctx, member: discord.Member = None):
    #     if member is None:
    #         member = ctx.message.author
    #     else:

    @commands.command()
    async def checkranks(self, ctx):
        msg = "Top 5 ranked members:\n"
        replist = get_ranks()
        # replist.sort()
        # final = replist[-5:]
        # mem = ctx.message.guild.get_member(replist[0][0])
        # print(get_member(ctx.message.guild, replist[0][0]))
        final_list = []
        for i in range(5):
            mem = ctx.message.guild.get_member(replist[i][0])
            final_list.append(str(mem.display_name))
            final_list.append(replist[i][1])
        # await ctx.send(msg + str(replist) + str(mem.display_name))
        await ctx.send(msg + str(final_list))


    @commands.command()
    async def checkrep(self, ctx, member: discord.Member = None):
        """Checks the reputation of specified user"""
        if member is None:  # return stats for author
            member = ctx.message.author
        else:
            member = member
        member_info = get_member(member, ctx.message.guild)
        embedded = discord.Embed()
        embedded.set_footer(text="Congrats on your meaningless internet points")
        icon_str = str(member.avatar_url)
        icon_addr = icon_str.split('.w', 1)
        author_icon_str = str(self.bot.user.avatar_url)
        author_icon = author_icon_str.split('.w', 1)

        embedded.set_author(name="Reputation stats for: " + member.display_name, icon_url=author_icon[0])
        embedded.set_thumbnail(url=icon_addr[0])
        embedded.add_field(name="Rep", value=member_info[5], inline=True)
        await ctx.send(embed=embedded)

    @commands.command()
    async def takerep(self, ctx, member: discord.Member):
        """Takes Rep from user. takerep <@user>. Cannot be yourself."""
        member_info = get_member(member, ctx.message.guild)
        reputation = member_info[5]
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
        """Gives Rep to user. giverep <@user>. Cannot be yourself."""
        if ctx.message.author.id == member.id:
            await ctx.send("You can't give yourself reputation points, fool!")
            return
        await ctx.send("Gave " + str(member.display_name) + " 1 reputation point!")
        self.add_reputation(member, ctx.message.guild, 1)


def setup(bot):
    bot.add_cog(Member_stats(bot))
