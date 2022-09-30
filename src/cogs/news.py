import os.path
import discord

from discord import ForumChannel
from discord.ext import commands

from ..message import Message


class News(commands.Cog):
    def __init__(self, bot):
        """Miscellaneous simple commands."""
        self.bot = bot
        self.ctx = Message(bot)
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE_NAME = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../../misc/spoiler_threads/threads.txt"
        ))

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


async def setup(bot):
    await bot.add_cog(News(bot))
