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

    # Returns bool based on whether given user is within the mods json.
    def is_user_mod(self, ctx, user: Member):
        mods = self.read_mods(ctx.guild.id)
        return (user.id in mods) or (user.id == ctx.guild.owner_id)

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
        mods = self.read_mods(ctx.guild.id)

        target_is_mod = target_id in mods
        user_is_mod = self.is_user_mod(ctx, ctx.author)

        if not target_is_mod and user_is_mod:
            mods.append(target_id)
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

        target_is_mod = target_id in mods
        user_is_mod = self.is_user_mod(ctx, ctx.author)

        if target_id == user_id:
            await ctx.send(f"You cannot unmod yourself!")
        elif target_is_mod and user_is_mod:
            mods.remove(target_id)
            self.write_mods(ctx.guild.id, mods)
            await ctx.send(f"{target.mention} as been unmodded.")
        elif not target_is_mod and user_is_mod:
            await ctx.send(f"{target.mention} is not a mod!")

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
        print(f"Banning: {target}")

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

    # Returns current mods list JSON object.
    def read_mods(self, id):
        try:
            with open(self.mods_filepath, "r") as file:
                data = json.load(file)
                return data[str(id)]
        except:
            return []

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
