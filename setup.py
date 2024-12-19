import discord
from discord.ext import commands
import os

def init():
    intents = discord.Intents.all()
    intents.members = True
    return commands.Bot(command_prefix='!', intents=intents, help_command=None)

async def run(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')