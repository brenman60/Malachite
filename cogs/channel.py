import discord
from discord.ext import commands

class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Removes a set amount of messages from the current Discord channel.
    @commands.command(name="purge", description="Clears messages with parameter [messages]")
    async def purge(self, ctx, messages: int):
        await ctx.channel.purge(limit=messages)

async def setup(bot):
    await bot.add_cog(Channel(bot))
