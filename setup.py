import discord
from discord.ext import commands
import os

# Creates Discord bot with set parameters.
def init():
    intents = discord.Intents.all()
    intents.members = True
    return commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Connects all cogs to the bot. Allows better file organization.
async def run(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')