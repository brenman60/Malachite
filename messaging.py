import setup

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

bot = setup.init()

# ideas: 
# - machine learning swear filter
# - christmas countdown
# - blocked website checker
# - 