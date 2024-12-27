import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="Displays command information")
    async def help(self, ctx):
        commands_list = [command for command in self.bot.commands]

        embed = discord.Embed(
            title="Help",
            description="Displays all commands",
            color=discord.Color.blue()
        )

        for command in commands_list:
            embed.add_field(name=command.name, value=command.description, inline=False)

        await ctx.send(embed=embed)

    async def config(self, ctx, action, key, value = None):
        actions = ["get", "set", "help"]
        if action not in actions:
            return await ctx.send(f"Unrecognized action '{action}'")
        
        match action:
            case "get":
                return ""
            case "set":
                return ""
            case "help":
                return ""
            case _:
                return ""

async def setup(bot):
    await bot.add_cog(Help(bot))
