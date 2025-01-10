from datetime import datetime
from typing import Optional
import discord
from discord import Member
from discord.ext import commands
import asyncio
import json
import os

class Server(commands.Cog):
    stats_filepath = os.path.join(os.path.dirname(__file__), "../data/server_stats.json")
    leveling_factor = 10

    def __init__(self, bot):
        self.bot = bot

    # Sends message containing information about the current Discord server.
    @commands.command(name="server", description="Displays current server's stats")
    async def server(self, ctx):
        async with ctx.channel.typing():
            await asyncio.sleep(0.5)
        
        icon = ctx.guild.icon.url if ctx.guild.icon != None else "https://cdn-icons-png.flaticon.com/512/25/25400.png"

        stats = self.read_stats(ctx.guild.id)
        exp_requirement = stats["lvl"] * self.leveling_factor

        embed = discord.Embed()
        embed.title = f"{ctx.guild.name} Stats"
        embed.url = ""
        embed.color = discord.Color.blue()
        embed.timestamp = datetime.now()
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Members:", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Level:", value=stats["lvl"], inline=True)
        embed.add_field(name="Level Up Progress", value=f"{round((stats["exp"] / exp_requirement) * 100)}%")

        await ctx.send(embed=embed)

    # Listens for user messages in order to input them into the server leveling system.
    @commands.Cog.listener()
    async def on_message(self, message):
        stats = self.read_stats(message.guild.id)
        exp_requirement = stats["lvl"] * self.leveling_factor
        stats["exp"] += len(message.clean_content)
        
        while stats["exp"] >= exp_requirement:
            stats["exp"] -= exp_requirement
            stats["lvl"] += 1
            exp_requirement = stats["lvl"] * 10

        self.write_stats(message.guild.id, stats)

    # Returns current stats list JSON object.
    def read_stats(self, id):
        try:
            with open(self.stats_filepath, "r") as file:
                data = json.load(file)
                return data[str(id)]
        except:
            return {"lvl": 0, "exp": 0}

    # Writes over the stats list JSON file with new data. Contains extra checks for make sure stats file exists before writing to it.
    def write_stats(self, id, data):
        id = str(id)

        current_stats = ""
        os.makedirs(os.path.dirname(self.stats_filepath), exist_ok=True)

        if not os.path.exists(self.stats_filepath):
            with open(self.stats_filepath, "w") as file:
                json.dump({}, file, indent=4)

        with open(self.stats_filepath, "r") as file:
                current_stats = json.load(file)

        current_stats[id] = data
        with open(self.stats_filepath, "w") as file:
            json.dump(current_stats, file, indent=4)

    # Callback for when new users are added to the current Discord server.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome to {member.guild.name}, {member.mention}.')

async def setup(bot):
    await bot.add_cog(Server(bot))
