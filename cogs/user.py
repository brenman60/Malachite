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

    # Sends message displaying a user's stats within the Discord server. Users level up by interacting in the server.
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

    # Promotes a user to moderator status. Allows heightened actions from them.
    @commands.command(name="mod", description="Mods user [username]")
    async def mod(self, ctx, target: Optional[Member]):
        if target is None:
            return

        target_id = str(target.id)
        user_id = str(ctx.author.id)
        mods = self.read_mods(ctx.guild.id)
        print(mods)

        target_is_mod = target_id in mods and mods[target_id] == "mod"
        user_is_owner = user_id == str(ctx.guild.owner_id)
        user_is_mod = (user_id in mods and mods[user_id] == "mod") or user_is_owner

        if not target_is_mod and user_is_mod:
            mods[target_id] = "mod"
            self.write_mods(ctx.guild.id, mods)
            await ctx.send(f"{target.mention} has been added as a mod.")
        elif target_is_mod and user_is_mod:
            await ctx.send(f"{target.mention} is already modded.")
        
    # Demotes a user from moderator status. Turns them back into a normal user.
    @commands.command(name="unmod", description="Unmods user [username]")
    async def unmod(self, ctx, target: Optional[Member]):
        if target is None:
            return
        
        target_id = str(target.id)
        user_id = str(ctx.author.id)
        mods = self.read_mods(ctx.guild.id)

        target_is_mod = target_id in mods and mods[target_id] == "mod"
        user_is_owner = user_id == str(ctx.guild.owner_id)
        user_is_mod = (user_id in mods and mods[user_id] == "mod") or user_is_owner

        if target_is_mod and user_is_mod:
            del mods[target_id]
            self.write_mods(ctx.guild.id, mods)
            await ctx.send(f"{target.mention} as been unmodded.")
        elif not target_is_mod and user_is_mod:
            await ctx.send(f"{target.mention} is not a mod!")
        elif target_id == user_id:
            await ctx.send(f"You cannot unmod yourself!")

    # Bans a user from the current Discord server. User can only join back once unbanned.
    @commands.command(name="unmod", description="Unmods user [username]")
    async def ban(self, ctx, target: Optional[Member]):
        if target is None:
            return
        
        

    # Returns current mods list JSON object.
    def read_mods(self, id):
        try:
            with open(self.mods_filepath, "r") as file:
                data = json.load(file)
                return data[str(id)]
        except:
            return {}

    # Writes over the mods list JSON file with new data. Contains extra checks for make sure mods file exists before writing to it.
    def write_mods(self, id, data):
        id = str(id)

        current_mods = ""
        os.makedirs(os.path.dirname(self.mods_filepath), exist_ok=True)

        if not os.path.exists(self.mods_filepath):
            with open(self.mods_filepath, "w") as file:
                json.dump({}, file, indent=4)

        with open(self.mods_filepath, "r") as file:
                current_mods = json.load(file)

        current_mods[id] = data
        with open(self.mods_filepath, "w") as file:
            json.dump(current_mods, file, indent=4)

async def setup(bot):
    await bot.add_cog(User(bot))
