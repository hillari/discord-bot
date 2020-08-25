import asyncio
import aiohttp
import random
import argparse
import traceback
from datetime import datetime, timedelta

import discord
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
        self.n_grams = {}
        self.starting_grams = []
        self.n_gram_order = 5

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
    async def markov(self, ctx, command, value, channel: discord.TextChannel = None, person : discord.Member = None):
        parser = argparse.ArgumentParser(prog="!markov")
        parser.add_argument("--load", help="load chat from the specified duration")
        parser.add_argument("--load_person", help="load messages from a specified person")
        parser.add_argument("--say", help="generate a random message based on the loaded chat")
        parser.add_argument("--set_degree", type=int, choices=range(1, 11), help="allows you set the order of n-grams for the Markov chain")
        try:
            args = parser.parse_args([command, value])
            if args.set_degree:
                self.n_gram_order = args.set_degree
                await ctx.send("N-gram degree set: {}".format(self.n_gram_order))

            elif args.load:
                possible_durations = ["1d", "1w", "1m"]
                duration = args.load
                if duration in possible_durations:

                    messages = []
                    if duration == "1d":
                        print("Loading messages for the past day...")
                        messages = await channel.history(limit=None, after=datetime.now()-timedelta(days=1)).flatten()
                        print("\tDONE")
                    if duration == "1w":
                        print("Loading messages from the past 7 days...")
                        messages = await channel.history(limit=None, after=datetime.now()-timedelta(days=7)).flatten()
                        print("\tDONE")
                    if duration == "1m":
                        print("Loading messages from the past 30 days...")
                        messages = await channel.history(limit=None, after=datetime.now()-timedelta(days=30)).flatten()
                        print("\tDONE")

                    if not messages:
                        await ctx.send("No messages within the time specified. Please choose a longer duration.")
                        return
                    self.n_grams = {}
                    self.starting_grams = []
                    for message in messages:
                        index = 0
                        content = message.content
                        while index + self.n_gram_order < len(content):
                            n_gram = content[index: (index + self.n_gram_order)]
                            n_gram_next = content[index + self.n_gram_order]
                            if n_gram in self.n_grams:
                                self.n_grams[n_gram].append(n_gram_next)
                            else:
                                self.n_grams[n_gram] = [n_gram_next]
                            if index == 0 or (n_gram[0].isupper() and n_gram[1].islower()):
                                self.starting_grams.append(n_gram)
                            index += 1
                    await ctx.send("Messages successfully loaded. Ready for chaos...")
                # error handling for malformed load arg
                else:
                    msg = """
                        ```
                        Error: --load must be supplied with a duration
                        currently valid loads = ["1h", "1d", "1w"]
                        example usage: !markov --load 1w
                        ```
                    """
                    await ctx.send(msg)
            elif args.load_person:
                num_messages = int(args.load_person)
                if num_messages > 1000:
                    await ctx.send("Please specify less than 1000 messages...")
                else:
                    messages = []
                    async for message in channel.history(limit=20000):
                        if message.author == person:
                            messages.append(message)
                            if len(messages) >= num_messages:
                                break
                    self.n_grams = {}
                    self.starting_grams = []
                    for message in messages:
                        index = 0
                        content = message.content
                        while index + self.n_gram_order < len(content):
                            n_gram = content[index: (index + self.n_gram_order)]
                            n_gram_next = content[index + self.n_gram_order]
                            if n_gram in self.n_grams:
                                self.n_grams[n_gram].append(n_gram_next)
                            else:
                                self.n_grams[n_gram] = [n_gram_next]
                            if index == 0 or (n_gram[0].isupper() and n_gram[1].islower()):
                                self.starting_grams.append(n_gram)
                            index += 1
                    message = 'Loaded '
                    message = message + str(len(messages)) + " messages from user: " + str(person) + " successfully!"
                    await ctx.send(message)

            elif args.say:
                length = int(args.say)
                if length < 1000:
                    current_gram = random.choice(self.starting_grams)
                    result = current_gram
                    for i in range(length):
                        try:
                            possibilities = self.n_grams[current_gram]
                            next = random.choice(possibilities)
                            result += next
                            current_gram = result[len(result) - self.n_gram_order : len(result)]
                        except KeyError:
                            result += ". "
                            current_gram = random.choice(self.starting_grams)
                            result += current_gram
                    print("Final result:", result)
                    await ctx.send(result)
                    return
                else:
                    msg = """
                        ```
                        Error: --say must have a length less than 1000 characters
                        example usage: !markov --say 350
                        ```
                    """
                    await ctx.send(msg)

            else:
                await self.markov_help(ctx)

        except Exception as e:
            print("Error:", e)
            traceback.print_exc(e)
            await self.markov_help(ctx)

        except SystemExit as e:
            await ctx.send("You damn near killed me...")
            await self.markov_help(ctx)


    async def markov_help(self, ctx):
        msg = """
```
Command                   Description
-------                   -----------
--load {time}             Loads chat through the duration specified.
--say {length}            Generates a random message up to a maximum length specified.
--set-degree {order}      Sets the n-gram order for Markov chain computation.
```
        """
        await ctx.send(msg)



def setup(bot):
    bot.add_cog(Games(bot))
