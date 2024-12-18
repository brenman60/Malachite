import discord
from discord.ext import commands

# Create a bot instance
intents = discord.Intents.all()
intents.members = True  # This enables member updates
bot = commands.Bot(command_prefix='!', intents=intents)

# Event when the bot has successfully connected
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')  # This will print when the bot starts

# A simple command
@bot.command()
async def hello(ctx):
    await ctx.send("dassssssssssssssssssssssssssssssss")

@bot.event
async def on_message(message):
    # Don't allow the bot to respond to its own messages
    if message.author == bot.user:
        print("Replying to self")
        return
    
    # Process commands as usual
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print(f"Error occurred: {error}")
    await ctx.send("Sorry, there was an error with the command!")

# Run the bot with your token
bot.run('MTMxODkzMjU5Njg1NTQwNjYyMw.G0TaIb.0jmK-thJQLe7ujzOzsRHsM1CjAx_Boip4HZkmY')  # Replace 'YOUR_BOT_TOKEN' with your actual token

# ideas: 
# - machine learning swear filter