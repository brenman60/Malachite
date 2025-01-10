import bot
import asyncio
import config
import os
from dotenv import load_dotenv

load_dotenv()

bot = bot.init()

# Signifies that the bot is active.
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready!")

    for guild in bot.guilds:
        config.init_config(guild.id)

# Adds the default bot configuration to the main config file when joining a new server.
@bot.event
async def on_guild_join(self, guild):
    config.init_config(guild.id)

# Catches all errors the bot encounters and relays them to the appropriate Discord channel.
@bot.event
async def on_command_error(ctx, error):
    print(f"Error occurred: {error}")
    await ctx.send(f"An error occurred running the command... ({error})")

# Sets up the bot using setup.py.
async def main():
    await bot.run(bot)
    
    async with bot:
        TOKEN = os.getenv("DISCORD_BOT_SECRET")
        await bot.start(str(TOKEN))

if __name__ == "__main__":
    asyncio.run(main())
