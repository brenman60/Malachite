import discord
from discord.ext import commands

def init():
    intents = discord.Intents.all()
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.run('MTMxODkzMjU5Njg1NTQwNjYyMw.G0TaIb.0jmK-thJQLe7ujzOzsRHsM1CjAx_Boip4HZkmY')

    return bot
