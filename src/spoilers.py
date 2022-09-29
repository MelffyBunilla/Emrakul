import aiohttp
import os.path
import urllib.parse
import pytz
import discord
import html

from discord.ext import commands, tasks
from datetime import datetime, timedelta
from io import BytesIO

from .message import Message


class Spoilers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.THREADS = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../misc/spoiler_threads/threads.txt"
        ))
        self.SPOILER_DT = os.path.realpath(os.path.join(
            self.ROOT_DIR, "../misc/spoiler_threads/spoiler_dt.txt"
        ))
        self.ctx = Message(bot)

    @tasks.loop(minutes=5)
    async def news_cycle(self):
        await self.bot.wait_until_ready()
        dt = datetime.now()
        newspaper = await self.get_news()
        with open(self.THREADS) as file:
            lines = file.readlines()
            threads = []
            for line in lines:
                tmp_threads = line.rstrip().split(',')
                tmp_thread = {}
                tmp_thread['guild_id'] = int(tmp_threads[0])
                tmp_thread['parent_id'] = int(tmp_threads[1])
                if len(tmp_threads) > 2:
                    tmp_thread['tag_id'] = int(tmp_threads[2])
                threads.append(tmp_thread)
        for thread in threads:
            await self.close_threads(thread['guild_id'], thread['parent_id'])
            await self.post_news(thread, newspaper)

    async def close_threads(self, guild_id, parent_id):
        guild = self.bot.get_guild(guild_id)
        guild_threads = await guild.active_threads()
        for thread in guild_threads:
            if thread.parent_id == parent_id:
                dt = datetime.now().replace(tzinfo=pytz.UTC)

                msg_dt = thread.created_at
                if thread.last_message:
                    message = thread.fetch_message(thread.last_message_id)
                    msg_dt = message.edited_at
                msg_dt = msg_dt + \
                    timedelta(minutes=thread.auto_archive_duration)

                if not thread.flags.pinned and dt > msg_dt:
                    await thread.edit(archived=True)

    async def get_news(self):
        dt = datetime.now()
        dt_now = str(dt.timestamp())[:10]
        with open(self.SPOILER_DT) as file:
            dt_previous = file.read()
        api_url = f"https://api.pushshift.io/reddit/search/submission/?subreddit=magictcg&sort=asc&sort_type=created_utc&after={dt_previous}&before={dt_now}&size=1000"
        newspaper = []
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                res = await response.json()
        if session is not None:
            await session.close()
        if res:
            for value in res['data']:
                if value['link_flair_text'] == "Spoiler" and not "[deleted]" in value['selftext']:
                    curr_news_headlines = [d['name'] for d in newspaper]
                    dt_previous = value['created_utc']
                    if not value['title'][:100] in curr_news_headlines:
                        tmp_news = {
                            "name": value['title'][:100],
                            "content": f"{urllib.parse.unquote(value['selftext'])}\n\n{value['full_link']}"[:2000],
                        }
                        if "preview" in value:
                            session = aiohttp.ClientSession()
                            async with session.get(html.unescape(value['url'])) as response:
                                img = await response.content.read()
                            if session is not None:
                                await session.close()
                            img_name = value['id'] + ".jpg"
                            tmp_news['file'] = discord.File(
                                fp=BytesIO(img), filename=img_name)
                        if "gallery_data" in value:
                            tmp_dict = []
                            i = 1
                            for item in value['gallery_data']['items']:
                                if item['media_id'] in value['media_metadata'] and i <= 10:
                                    if value['media_metadata'][item['media_id']]['status'] == 'valid':
                                        img_url = html.unescape(
                                            value['media_metadata'][item['media_id']]['s']['u'])
                                        session = aiohttp.ClientSession()
                                        async with session.get(img_url) as response:
                                            img = await response.content.read()
                                        if session is not None:
                                            await session.close()
                                        img_name = item['media_id'] + ".jpg"
                                        tmp_dict.append(discord.File(
                                            fp=BytesIO(img), filename=img_name))
                                        i += 1
                            if len(tmp_dict) > 0:
                                tmp_news['files'] = tmp_dict
                        newspaper.append(tmp_news)
        f = open(self.SPOILER_DT, "w")
        f.write(str(dt_previous))
        f.close()
        return newspaper

    async def post_news(self, thread, newspaper):
        """Get spoiler posts from reddit."""
        guild = self.bot.get_guild(thread['guild_id'])
        channel = guild.get_channel(thread['parent_id'])
        tag = None
        if "tag_id" in thread:
            tag = [channel.get_tag(thread['tag_id'])]
        for news in newspaper:
            if tag:
                news["applied_tags"] = tag
            await channel.create_thread(**news)


async def setup(bot):
    await bot.add_cog(Spoilers(bot))