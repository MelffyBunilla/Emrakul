import os.path
from discord.ext import commands


class ReadMe(commands.Cog):
    def __init__(self, bot):
        """Simple Discord Message Rewrite."""
        self.bot = bot
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.EMRA_UPDATES = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../misc/updates/Emrakul-updates.txt"
        ))
        self.EMRA_README = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../README.md"
        ))


    async def write_readme(self):
        guilds_count = len(self.bot.guilds)
        users_count = 0

        for guild in self.bot.guilds:
            users_count += guild.member_count

        emrakul_addme = "https://discordapp.com/oauth2/authorize?client_id=850633920012877874&scope=bot&permissions=262144"

        with open(self.EMRA_UPDATES) as f:
            emrakul_update = f.read()
        emrakul_help = ""
        emrakul_commands = {}
        command_name_len = 0

        for cog_name in self.bot.cogs:
            if len(self.bot.cogs[cog_name].get_commands()) > 0:
                emrakul_commands[cog_name] = []
                for command in self.bot.cogs[cog_name].get_commands():
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

        f = open(self.EMRA_README, "w")

        f.write(txt)
        f.close()


async def setup(bot):
    await bot.add_cog(ReadMe(bot))
