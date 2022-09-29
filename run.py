import os
import logging
import asyncio

from discord import Game, ActivityType, Intents
from discord.ext import commands
from secret import EMRAKUL_SECRET_TOKEN, DEV_ONLY
from datetime import datetime, timedelta

from src.spoilers import Spoilers

logging.basicConfig(level=logging.INFO)
token = EMRAKUL_SECRET_TOKEN

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="A magic the gathering card fetcher bot",
    pm_help=True,
    intents=intents)

bot.dev_mode = DEV_ONLY
news_start = datetime.now()
news_started = False


@bot.event
async def on_ready():
    global news_start, news_started
    game = Game("!help // !updates")
    await bot.change_presence(status=ActivityType.playing,
                              activity=game)

    await write_readme()

    # dt = datetime.now()
    # ts = news_start + timedelta(seconds=5)
    # spoilers = Spoilers(bot)

    # if not news_started:
    #     news_started = True
    #     spoilers.news_cycle.start()

    # if news_started and ts < dt:
    #     news_start = ts
    #     spoilers.news_cycle.restart()


async def load_extensions():
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"src.cogs.{filename[:-3]}")


async def main(token):
    async with bot:
        await load_extensions()
        await bot.start(token)


async def write_readme():
    guilds_count = len(bot.guilds)
    users_count = 0

    for guild in bot.guilds:
        users_count += guild.member_count

    emrakul_addme = "https://discordapp.com/oauth2/authorize?client_id=850633920012877874&scope=bot&permissions=262144"

    with open("misc/updates/Emrakul-updates.txt") as f:
        emrakul_update = f.read()
    emrakul_help = ""
    emrakul_commands = {}
    command_name_len = 0

    for cog_name in bot.cogs:
        if len(bot.cogs[cog_name].get_commands()) > 0:
            emrakul_commands[cog_name] = []
            for command in bot.cogs[cog_name].get_commands():
                if len(command.qualified_name) > command_name_len:
                    command_name_len = len(command.qualified_name)
                emrakul_commands[cog_name].append(
                    [command.qualified_name, command.help])

    command_name_len += 2
    for cog_name, commands in emrakul_commands.items():
        emrakul_help += f"\n{cog_name}:"
        for command in commands:
            spaces = " " * (command_name_len - len(command[0]))
            emrakul_help += f"\n  {command[0]}{spaces}{command[1]}"

    txt = f'''[![Stats](https://img.shields.io/badge/discord-{guilds_count}%20servers%20{users_count}%20users-blue.svg)]({emrakul_addme})


# Emrakul

[https://github.com/MelffyBunilla/Emrakul](https://github.com/MelffyBunilla/Emrakul)


Emrakul is a mtg card-fetcher discord bot that is heavily inspired by [Bolas](https://github.com/theneosloth/Bolas).

The docstring for each one of the plugins are all concatenated together and can be displayed with the hardcoded !help command. 

## List of commands

``` {emrakul_help}
```

## How to run

Execute run.py.

## Add Emrakul to your Discord server

[Click here]({emrakul_addme})

## Updates

``` 
{emrakul_update}
```'''

    f = open("README.md", "w")

    f.write(txt)
    f.close()

asyncio.run(main(token))
