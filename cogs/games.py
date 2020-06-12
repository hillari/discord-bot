import asyncio
import aiohttp
import random
import argparse
from discord.ext import commands


try:
    answer_list = []
    with open("./files/8ball_answers.txt", "r") as answer:
        lines = answer.readlines()
        for line in lines:
            answer_list.append(line.rstrip())
except Exception:
    lines = []


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Chooses between strings. Use quotes for phrases"""
        input = choices
        """Chooses between multiple choices e.g. choose <choice> <choice>"""
        await ctx.send(random.choice(input))

    @commands.command()
    async def repeat(self, ctx, times: int, content='repeating...'):
        """Repeats a message multiple times e.g. repeat <number> <text>"""
        if times > 10:
            await ctx.send("{} times is too much. Please Limit to 10.".format(str(times)))
        else:
            for i in range(times):
                await ctx.send(content)

    @commands.command(name='8ball')
    async def eight_ball(self, ctx):
        """8 ball game"""
        print("8ball cmd received")
        await ctx.send(random.choice(answer_list) + ", " + ctx.message.author.mention)

#  Taken from: https://github.com/Der-Eddy/discord_bot/blob/master/cogs/fun.py
    @commands.command()
    async def countdown(self, ctx):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('**:ok:** DING DING DING')

    @commands.command()
    async def praise(self, ctx):
        '''Praise the Sun'''
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def hype(self, ctx):
        '''HYPE TRAIN CHOO CHOO'''
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)

    @commands.command()
    async def xkcd(self, ctx, *searchterm: str):
        ''' Random xkcd, made awesome by Sock '''

        apiUrl = 'https://xkcd.com/info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl) as resp:
                curr_json = await resp.json()
                max_num = curr_json['num']
            random_comic = random.randint(1, max_num)  # the first comic starts at 1
            comicUrl = 'https://xkcd.com/{}/'.format(random_comic)
            json_url = comicUrl + 'info.0.json'
            async with cs.get(json_url) as resp:
                new_comic = await resp.json()
                date = '{}.{}.{}'.format(new_comic['day'], new_comic['month'], new_comic['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(new_comic['safe_title'], new_comic['img'], new_comic['alt'],
                                                                                 comicUrl, date)
                
            await ctx.send(msg)


    @commands.command()
    async def markov(self, ctx, args):
        parser = argparse.ArgumentParser(prog="!markov")
        parser.add_argument("--load", help="load chat from the specified duration")
        parser.add_argument("--say", help="generate a random message based on the loaded chat")
        args = parser.parse_args(args)

        if args.load:
            duration = args.load
            # load the chat for the past duration
        elif args.say:
            length = args.say
        else:
            await self.markov_help(ctx)


    async def markov_help(self, ctx):
        msg = """
                ```
                Command                   Description
                -------                   -----------
                --load {time}            Loads chat through the duration specified.
                --say {length}           Generates a random message up to a maximum length specified.
                ```
              """
        await ctx.send(msg)



def setup(bot):
    bot.add_cog(Games(bot))
