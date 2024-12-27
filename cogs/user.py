from datetime import datetime
from typing import Optional
import discord
from discord import Member
from discord.ext import commands
import asyncio
import json
import os

class User(commands.Cog):
    mods_filepath = os.path.join(os.path.dirname(__file__), "../data/mods.json")

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

    @commands.command(name="mod", description="Mods user [username]")
    async def mod(self, ctx, target: Optional[Member]):
        if target is None:
            return

        mods = self.read_mods()

        if (str(target.id) in mods and mods[str(target.id)] != "mod") or (str(target.id) not in mods):
            mods[str(target.id)] = "mod"
            self.write_mods(mods)
            await ctx.send(f"{target.mention} has been added as a mod.")
        elif str(target.id) in mods and mods[str(target.id)] == "mod":
            await ctx.send(f"{target.mention} is already modded.")
        
    def read_mods(self):
        try:
            with open(self.mods_filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def write_mods(self, data):
        os.makedirs(os.path.dirname(self.mods_filepath), exist_ok=True)
        with open(self.mods_filepath, "w") as file:
            json.dump(data, file, indent=4)

async def setup(bot):
    await bot.add_cog(User(bot))
