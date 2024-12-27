from datetime import datetime
from typing import Optional
import discord
from discord import Member
from discord.ext import commands
import asyncio

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="server", description="Displays current server's stats")
    async def server(self, ctx):
        async with ctx.channel.typing():
            await asyncio.sleep(2)
        
        icon = ctx.guild.icon.url if ctx.guild.icon != None else "https://cdn-icons-png.flaticon.com/512/25/25400.png"

        embed = discord.Embed()
        embed.title = f"{ctx.guild.name} Stats"
        embed.url = ""
        embed.color = discord.Color.blue()
        embed.timestamp = datetime.now()
        embed.set_thumbnail(url=icon)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome to {member.guild.name}, {member.mention}.')

async def setup(bot):
    await bot.add_cog(Server(bot))
