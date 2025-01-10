from datetime import datetime
from typing import Optional
import discord
from discord import Member
from discord.ext import commands
import asyncio
import json
import os

class User(commands.Cog):
    stats_filepath = os.path.join(os.path.dirname(__file__), "../data/user_stats.json")
    leveling_factor = 5

    def __init__(self, bot):
        self.bot = bot

    # Sends message displaying a user's stats within the Discord server. Users level up by interacting in the server.
    @commands.command(name="stats", description="Displays user [username]'s server stats")
    async def stats(self, ctx, user: Optional[Member]):
        async with ctx.channel.typing():
            await asyncio.sleep(0.5)
        
        user = user or ctx.author

        stats = self.read_stats(ctx.guild.id)
        player_stats = None
        if str(user.id) in stats:
            player_stats = stats[str(user.id)]
        else:
            player_stats = {"lvl": 0, "exp": 0}

        exp_requirement = player_stats["lvl"] * self.leveling_factor

        embed = discord.Embed()
        embed.title = f"{f"{user.display_name}'" if user.display_name[-1] == "s" else f"{user.display_name}'s"} Stats"
        embed.color = user.accent_color
        embed.timestamp = datetime.now()
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Level:", value=player_stats["lvl"], inline=True)
        embed.add_field(name="Level Up Progress", value=f"{round((player_stats["exp"] / exp_requirement) * 100)}%")

        await ctx.send(embed=embed)
    
    # Listens for user messages in order to input them into the leveling system.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user = message.author

        stats = self.read_stats(message.guild.id)
        player_stats = None
        if str(user.id) in stats:
            player_stats = stats[str(user.id)]
        else:
            player_stats = {"lvl": 0, "exp": 0}

        exp_requirement = player_stats["lvl"] * self.leveling_factor
        player_stats["exp"] += len(message.clean_content)
        
        player_did_levelup = False
        while player_stats["exp"] >= exp_requirement:
            player_stats["exp"] -= exp_requirement
            player_stats["lvl"] += 1
            exp_requirement = player_stats["lvl"] * self.leveling_factor
            player_did_levelup = True

        if player_did_levelup:
            await message.channel.send(f"{user.mention} is now level {player_stats["lvl"]}!")

        stats[str(user.id)] = player_stats

        self.write_stats(message.guild.id, stats)

    # Returns current stats list JSON object.
    def read_stats(self, id):
        try:
            with open(self.stats_filepath, "r") as file:
                data = json.load(file)
                return data[str(id)]
        except:
            return {}

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

    # Bans a user from the current Discord server. User can only join back once unbanned.
    @commands.command(name="ban", description="Bans user [username]")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, target: Member, reason: Optional[str]):
        if target is ctx.author:
            await ctx.send(f"You cannot ban yourself!")
            return
        
        if reason is None:
            reason = "None provided"

        await target.ban(reason = reason)

    # Bans a user from the current Discord server. User can only join back once unbanned.
    @commands.command(name="unban", description="Unbans user [username]")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, target: Member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = target.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
            
    # Kicks a user from the current Discord server.
    @commands.command(name="kick", description="Kicks user [username]")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, target: Member, reason: Optional[str]):
        if target is ctx.author:
            await ctx.send(f"You cannot kick yourself!")
            return

        if reason is None:
            reason = "None provided"

        await target.kick(reason=reason)

async def setup(bot):
    await bot.add_cog(User(bot))
