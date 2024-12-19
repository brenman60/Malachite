import setup
import asyncio

bot = setup.init()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready!")

@bot.event
async def on_command_error(ctx, error):
    print(f"Error occurred: {error}")
    await ctx.send(f"An error occurred running the command... ({error})")

async def main():
    await setup.run(bot)
    
    async with bot:
        await bot.start('MTMxODkzMjU5Njg1NTQwNjYyMw.G0TaIb.0jmK-thJQLe7ujzOzsRHsM1CjAx_Boip4HZkmY')

if __name__ == "__main__":
    asyncio.run(main())

# apparently can host on Replit, Heroku, or Railway
# ideas: (~ = haven't started, % = in progress, {} = completed, <> = notes, -= =- = description)
# ~ !resume
# ~ !skills
# % !help
# {} !linkedin
# {} !github
# % !stats [username]
# % !server
# ~ !project [project name]
# ~ !project [help]
# ~ !gamble <rename needed> -= small game revolving around money or something. money stored in JSON file probably for each person... unless Discord has specific userdata or something =-
# ~ !generateName -= makes random type of name like those websites =-
