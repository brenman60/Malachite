import discord
from discord.ext import commands
import os
import config

# Creates Discord bot with set parameters.
def init():
    intents = discord.Intents.all()
    intents.members = True
    return commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# Connects all cogs to the bot. Allows better file organization.
async def run(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Grabs the current prefix configuration from the config.json file and uses it as the current server's prefix.
def get_prefix(bot, message):
    prefix = config.get_config(message.guild.id, "prefix")
    if prefix == "":
        prefix = "!"

    return prefix
