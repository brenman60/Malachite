from datetime import datetime
from typing import Optional
import discord
from discord import Member
from discord.ext import commands
import asyncio

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", description="Displays user [username]'s server stats")
    async def stats(self, ctx, target: Optional[Member]):
        async with ctx.channel.typing():
            await asyncio.sleep(2)
        
        target = target or ctx.author

        embed = discord.Embed()
        embed.title = f"{target.name}'s Server Stats"
        embed.url = ""
        embed.color = discord.Color.blue()
        embed.timestamp = datetime.now()
        embed.set_thumbnail(url=target.avatar)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(User(bot))
