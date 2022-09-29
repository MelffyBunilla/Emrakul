import os.path
import discord
import random
import aiohttp

from discord import ForumChannel
from discord.ext import commands

from ..message import Message


class Misc(commands.Cog):
    def __init__(self, bot):
        """Miscellaneous simple commands."""
        self.bot = bot
        self.ctx = Message(bot)
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE_NAME = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../../misc/spoiler_threads/threads.txt"
        ))

    @commands.command()
    async def hello(self, ctx):
        """Only works if you are one of the chosen ones."""

        obey_dict = {
            # neosloth
            120767447681728512: "Hi neosloth.",
            # Average Dragon
            182268688559374336: "neosloth: Eat a dick, dragon.",
            # Garta
            217005730149040128: "neosloth: Welcome, Srammiest Man",
            # spitefiremase
            165971889351688192: "neosloth: Mase, you're cooler and smarter and stronger and funnier in real life",
            # Shaper
            115501385679634439: "neosloth: Shaped shape shaping shapes~",
            # Braden
            279686121149956096: "neosloth: Braden is definitely lame.",
            # Sickrobot
            98525939910078464: "neosloth: *sniffle* yea, sure",
            # Melffy Bunilla
            141131991218126848: "Hi cutie. <3",
            # Mori
            161511401322446848: ":sheep:"
        }

        if ctx.message.author.id in obey_dict.keys():
            await self.ctx.send(ctx, obey_dict[ctx.message.author.id])
        else:
            await self.ctx.send(ctx, "owo hi, ʰᵒʷ ʳ ᵘ")

    @commands.command()
    async def addme(self, ctx):
        """The link to add Emrakul to your Discord server."""
        await self.ctx.send(ctx, "https://discordapp.com/oauth2/authorize?"
                            "client_id=850633920012877874&scope=bot&permissions=262144")

    @commands.command()
    async def remove_news_channel(self, ctx):
        "!remove_news_channel: Remove news channel. (Manage Channels Permission required)"
        if ctx.message.author.guild_permissions.manage_channels:
            guild_id = ctx.message.guild.id
            with open(self.FILE_NAME) as file:
                lines = file.readlines()
                all_lines = ""
                for line in lines:
                    tmp_threads = line.rstrip().split(',')
                    if not int(tmp_threads[0]) == guild_id:
                        all_lines += line.rstrip() + '\n'
            threads_file = open(self.FILE_NAME, 'w')
            threads_file.write(all_lines)
            threads_file.close()
            await self.ctx.send(ctx, "News Channel removed from Emmy.")
        else:
            await self.ctx.send(ctx, "You don't have the permissions to use this command.")

    @commands.command()
    async def add_news_channel(self, ctx):
        "!add_news_channel {Channel ID} {optional: Tag}: Add news channel. (Right click a channel, then click 'Copy ID') (Manage Channels Permission required)"
        if ctx.message.author.guild_permissions.manage_channels:
            args = ctx.message.content.split()
            if len(args) > 1:
                try:
                    parent_id = int(args[1])
                    channel = ctx.message.guild.get_channel(parent_id)
                    if isinstance(channel, ForumChannel):
                        guild_id = ctx.message.guild.id
                        with open(self.FILE_NAME) as file:
                            lines = file.readlines()
                            threads = []
                            for line in lines:
                                tmp_threads = line.rstrip().split(',')
                                threads.append(int(tmp_threads[0]))
                        if not guild_id in threads:
                            threads_file = open(self.FILE_NAME, 'a+')
                            thread = {
                                "name": "Forum Channel added to News Command",
                                "content": "This is a test thread, you can delete it if you want."
                            }
                            thread_info = str(guild_id) + ',' + str(parent_id)
                            thread_tag_id = ""
                            if len(args) > 2:
                                for tag_id, tag in channel._available_tags.items():
                                    if tag.name == args[2]:
                                        thread_tag_id = ',' + str(tag.id)
                                        thread["applied_tags"] = [
                                            channel.get_tag(tag.id)]
                            try:
                                thread, message = await channel.create_thread(**thread)
                                try:
                                    await thread.edit(archived=True)
                                    threads_file.write(
                                        f"{thread_info}{thread_tag_id}\n")
                                except discord.errors.Forbidden as e:
                                    await thread.send("Missing channel permissions. (Emmy needs to manage posts)")
                            except discord.errors.Forbidden as e:
                                await self.ctx.send(ctx, "Missing channel permissions. (Emmy needs to create and manage posts)")
                        else:
                            await self.ctx.send(ctx, "You already added a News Channel to this Server.")
                    else:
                        await self.ctx.send(ctx, "The provided channel id is not a forum channel.")
                except ValueError as e:
                    await self.ctx.send(ctx, "Please provide a forum channel id. (Right click a channel, then click 'Copy ID')")
            else:
                await self.ctx.send(ctx, "Please provide a forum channel id. (Right click a channel, then click 'Copy ID')")
        else:
            await self.ctx.send(ctx, "You don't have the permissions to use this command.")

    @commands.command()
    async def updates(self, ctx):
        "Get the current updates on the Emrakul bot."
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE_NAME = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../../misc/updates/Emrakul-updates.txt"
        ))
        await self.ctx.send(ctx, file=discord.File(self.FILE_NAME))

    @commands.command()
    async def flirt(self, ctx):
        "Return the image of a given card."
        cute_choice = random.choices(["../../misc/emrablush.jpg",
                                      "../../misc/emrashy.png",
                                      ])
        flirt_line = random.choices(["Did it hurt when you broke through the plane's crust ascending from the underworld?",
                                     "Did it hurt when you broke through time and space to feed on reality itself?",
                                     "I'm learning about important dates in history. Wanna be one of them?",
                                     "Do you have a map? I keep getting lost in your eyes.",
                                     "You're so beautiful that you made me forget my pickup line.",
                                     "I was wondering if you had an extra heart. Mine was just stolen.",
                                     "Are you extraterrestrial? Because you just abducted my heart.",
                                     "You know what you would look really beautiful in? My tentacles.",
                                     "The spark in your soul is so bright, Heliod must be jealous.",
                                     "One night I looked up at the stars and thought, 'Wow, so many planes to consume.' But now that I'm looking at you, that all seems so pointless.",
                                     "If beauty were time, you'd be eternity.",
                                     "I love you to your plane and back.",
                                     "Hey cutie, you must be an eldritch horror because I find you maddening.",
                                     "You make me lose my mind!",
                                     "I can't wait for it to be full moon, so I can see you again.",
                                     "Three words. Fourteen letters. Say it and I'm all yours.\n\nBanding with you.",
                                     "Three words. Fourteen letters. Say it and I'm all yours.\n\nPartner with you.",
                                     "Two words. Fourteen letters.\n\nFriends Forever!",
                                     "I hope each night to become eternal, so I can be with you forever.",
                                     "You are the only Treasure I wouldn't sacrifice, not even for value.",
                                     ])
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE_NAME = os.path.realpath(os.path.join(
            self.ROOT_DIR, cute_choice[0]
        ))
        await self.ctx.send(ctx, flirt_line[0])
        await self.ctx.send(ctx, file=discord.File(self.FILE_NAME))

    @commands.command()
    async def scryfall_extension(self, ctx):
        "Download a simple Chrome extension that restores the Magiccards.info function to auto-focus the search bar."
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE_NAME = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../../misc/scryfall_search_bar_ext.zip"
        ))
        install_guide = "1. Save this to a place you don't accidentally delete\n"
        install_guide += "2. Go to chrome://extensions/\n"
        install_guide += "3. Click in the top right on 'Developer mode'\n"
        install_guide += "4. Click 'Load unpacked'\n"
        install_guide += "5. Choose this .zip file, or folder if you unpacked it"
        await self.ctx.send(ctx, install_guide)
        await self.ctx.send(ctx, file=discord.File(self.FILE_NAME))

    @commands.command()
    async def asmor(self, ctx):
        "Asmoranomardicadaistinaculdacar"
        await self.ctx.send(ctx, "Asmoranomardicadaistinaculdacar")

    @commands.command()
    async def roll(self, ctx):
        "Roll any dice."
        args = ctx.message.content.split()
        table = random.choices([0, 1], [10, 1])
        people = random.randrange(1, 9999)
        if len(args) > 1:
            amount = 1
            result_amount = ""
            if "d" in args[1]:
                dice_arr = args[1].split("d")
                number = dice_arr[1]
                if not dice_arr[0] == "":
                    try:
                        amount = int(dice_arr[0])
                    except ValueError as e:
                        await self.ctx.send(ctx, "ö̴̲̳̼̯́̿͒ĥ̵͎̺̔̇̃̀͑̕ ̶̻̞̹̺͍̩̇͊̏̒̄͐͛͐̌̓n̷͖̪͌̀̄̑̓́̊̏͝o̴̡̲̺̭͙̖͉̝͎̪̎̂̈̍̓̈́ ̴̩͖̂̋͝w̴̱̭͖̲͍̓̿͌̓̀͋ͅh̸͍̣̣͒̔̂͛̊̽͝ȃ̷̡̨͎̖͍̞̪̣̪͑̌̄͊͌͛̀̚͝t̷͖͌ ̵̢͇̮̪͈̘͐́͑̆h̶͎̹̟̺̮̮̩̉̔͆̋̐͜͠ą̶͔̬̱̤̭̦͌̐͆̿̃̍͜͜ͅv̸̻̟͈̗̦̳̬̰̩́̄e̵̺͚̻͔̯̎͒̾ ̶̢̧̥̳̗̮̪̬̻̉͗͋̋̓͗͑̎̎ͅỳ̶͚̹͇̙̣̪̪͓͐̌̈́̽͑͝ő̴̧̟̜͔̘̥̠͋̀͐̀̆̎̾̇̏ú̸̡̡̫̟̻̼̰̺͙̐͋̐̚͠ ̵̢̳̣͈̾̈́͑̾͒̚͝d̷̤̥̱͉̒̌͌ọ̸̬̼͒̓̈̐̌̃̃̎̋͠-̷͓̀͊-̷̩̲̯͈̤̠̫̜͛̽͂̐͒͑͌͛͑-̶̧̞͖̼͔̙͓̗͔̥͆̊̅ ")
            else:
                number = args[1]
            if not number == "2":
                result_amount = "a"
                if amount > 1:
                    result_amount = "{}".format(amount)
                await self.ctx.send(ctx, "*Emrakul rolls {} massive interdimensional d{}, {} Innistrad people are crushed under the weight*".format(result_amount, number, people))
            if table[0] > 0:
                await self.ctx.send(ctx, "It fell off the plane **uwu**")
            else:
                try:
                    if int(amount) > 20:
                        await self.ctx.send(ctx, "....oh god they spilled all over I can't count all these....where's my favorite dice??? **>.<**")
                    elif int(number) < 2:
                        if amount > 1:
                            result_amount = " {} times".format(amount)
                        await self.ctx.send(ctx, "The dice landed on {}{}....what did you expect".format(number, amount))
                    elif int(number) == 2:
                        await self.ctx.send(ctx, "Emrakul: (╯°□°）╯︵ ┻━┻")
                        await self.flip(ctx)
                    else:
                        random_num = ""
                        for x in range(0, amount):
                            random_num = "{}{},".format(
                                random_num, random.randrange(1, int(number)))
                        if amount > 1:
                            result_txt = "Your results are {}".format(
                                random_num[:-1])
                        else:
                            result_txt = "Your result is {}".format(
                                random_num[:-1])
                        await self.ctx.send(ctx, result_txt)
                except ValueError as e:
                    await self.ctx.send(ctx, "ö̴̲̳̼̯́̿͒ĥ̵͎̺̔̇̃̀͑̕ ̶̻̞̹̺͍̩̇͊̏̒̄͐͛͐̌̓n̷͖̪͌̀̄̑̓́̊̏͝o̴̡̲̺̭͙̖͉̝͎̪̎̂̈̍̓̈́ ̴̩͖̂̋͝w̴̱̭͖̲͍̓̿͌̓̀͋ͅh̸͍̣̣͒̔̂͛̊̽͝ȃ̷̡̨͎̖͍̞̪̣̪͑̌̄͊͌͛̀̚͝t̷͖͌ ̵̢͇̮̪͈̘͐́͑̆h̶͎̹̟̺̮̮̩̉̔͆̋̐͜͠ą̶͔̬̱̤̭̦͌̐͆̿̃̍͜͜ͅv̸̻̟͈̗̦̳̬̰̩́̄e̵̺͚̻͔̯̎͒̾ ̶̢̧̥̳̗̮̪̬̻̉͗͋̋̓͗͑̎̎ͅỳ̶͚̹͇̙̣̪̪͓͐̌̈́̽͑͝ő̴̧̟̜͔̘̥̠͋̀͐̀̆̎̾̇̏ú̸̡̡̫̟̻̼̰̺͙̐͋̐̚͠ ̵̢̳̣͈̾̈́͑̾͒̚͝d̷̤̥̱͉̒̌͌ọ̸̬̼͒̓̈̐̌̃̃̎̋͠-̷͓̀͊-̷̩̲̯͈̤̠̫̜͛̽͂̐͒͑͌͛͑-̶̧̞͖̼͔̙͓̗͔̥͆̊̅ ")
        else:
            dice = random.choices([4, 6, 8, 10, 12, 20])
            await self.ctx.send(ctx, "*Emrakul rolls a massive interdimensional d{}, {} Innistrad townspeople are crushed by this dice*".format(dice[0], people))
            if table[0] > 0:
                await self.ctx.send(ctx, "It fell off the table uwu")
            else:
                await self.ctx.send(ctx, random.randrange(1, dice[0]))

    @commands.command()
    async def flip(self, ctx):
        "Flip a coin."
        side = random.choices([0, 1], [6000, 1])
        cat = random.choices([0, 1], [500, 1])
        people = random.randrange(1, 9999)
        await self.ctx.send(ctx, "*Emrakul throws a coin on an interdimensional scale, {} Innistrad townspeople are crushed when the coin lands*".format(people))
        if side[0] > 0:
            await self.ctx.send(ctx, "The coin landed on its side (a 1:6000 chance)")
        else:
            if cat[0] > 0:
                await self.ctx.send(ctx, "Alms Collector stole your coin, you drew a card instead")
            else:
                start = random.choices([0, 1])
                if start[0] > 0:
                    odds = [51, 49]
                else:
                    odds = [49, 51]
                coin = random.choices(["heads", "tails"], odds)
                await self.ctx.send(ctx, "The coin landed on {}".format(coin[0]))

    @commands.command()
    async def advice(self, ctx):
        "Emrakul gives advice."
        args = ctx.message.content.split()
        people = random.randrange(1, 9999)
        advice = random.choices(["It is certain.",
                                 "It is decidedly so.",
                                 "Without a doubt.",
                                 "Yes definitely.",
                                 "You may rely on it.",
                                 "As I see it, yes.",
                                 "Most likely.",
                                 "Outlook good.",
                                 "Yes.",
                                 "Signs point to yes.",
                                 "Reply hazy, try again.",
                                 "Ask again later.",
                                 "Better not tell you now.",
                                 "Cannot predict now.",
                                 "Concentrate and ask again.",
                                 "Don't count on it.",
                                 "My reply is no.",
                                 "My sources say no.",
                                 "Outlook not so good.",
                                 "Very doubtful.",
                                 "You did great today.",
                                 "I'm proud of you.",
                                 "You look stunning today.",
                                 "OMG I just saw a gif of a cute puppy.",
                                 "Did you hydrate today?",
                                 "You probably need to get some food.",
                                 "Someone in here needs to go to bed.",
                                 "You're valid.",
                                 ])
        await self.ctx.send(ctx, "*Emrakul wants to help you, but while starting to think she started to lean on the Innistrad plane, {} Innistrad townspeople were crushed due to that*".format(people))
        await self.ctx.send(ctx, advice[0])

    @commands.command()
    async def powerlevel(self, ctx):
        "What's the power level?!"
        seven = random.choices(["seven",
                                "سَبْعَة",
                                "sete",
                                "七",
                                "sedam",
                                "sedm",
                                "syv",
                                "zeven",
                                "siete",
                                "seitsemän",
                                "sept",
                                "sieben",
                                "επτά",
                                "sette",
                                "七",
                                "7",
                                "sju",
                                "siedem",
                                "sete",
                                "șapte",
                                "семь",
                                "siete",
                                "sju",
                                "семь",
                                "เจ็ด",
                                "yedi",
                                "сім",
                                "bảy", ])
        await self.ctx.send(ctx, "The deck has a power level of {} (7) out of 10.".format(seven[0]))

    @commands.command()
    async def cut(self, ctx):
        "Ask emmy for cut."
        land = random.choices(
            ["a plains", "an island", "a swamp", "a mountain", "a forest"])
        await self.ctx.send(ctx, "You should cut {}.".format(land[0]))

    @commands.command()
    async def git(self, ctx):
        """Repo link."""
        await self.ctx.send(ctx, "https://github.com/MelffyBunilla/Emrakul")

    @commands.command()
    async def stats(self, ctx):
        """Return the number of users and servers served."""
        users_count = 0
        for guild in self.bot.guilds:
            users_count+=guild.member_count

        await self.ctx.send(ctx, "Fetching cards for {} servers and {} users".format(
            len(self.bot.guilds),
            users_count
        ))

    @commands.command()
    async def video(self, ctx):
        """Create a new jitsi videocall with everyone mentioned."""
        # Random 10 digit number
        call_id = str(random())[2:12]
        url = "https://meet.jit.si/{}".format(call_id)

        # Simply send out the url if no one was mentioned
        if not ctx.message.mentions:
            await self.ctx.send(ctx, url)

        invite_message = "{} is inviting you to a videocall.\n{}".format(
            ctx.author.name,
            url
        )

        await self.ctx.send(ctx.author, invite_message)

        for mention in ctx.message.mentions:
            await self.ctx.send(mention, invite_message)


async def setup(bot):
    await bot.add_cog(Misc(bot))
