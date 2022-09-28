from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        """Simple Discord Message Rewrite."""
        self.bot = bot

    async def send(self, ctx, content=None, embed=None, file=None, delete_after=None):
        context = {}
        if content:
            context['content'] = content
        if embed:
            context['embed'] = embed
        if file:
            context['file'] = file
        if delete_after:
            context['delete_after'] = delete_after
        if not self.bot.dev_mode or ctx.message.author.id == 141131991218126848:
            await ctx.send(**context)


async def setup(bot):
    await bot.add_cog(Message(bot))
