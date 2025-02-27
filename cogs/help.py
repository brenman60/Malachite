import discord
from discord.ext import commands
import config

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sends message displaying all registered bot commands and their descriptions.
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

    # Allows user to set, get, or recieve information about this bot's configurations.
    @commands.command(name="config", description="Gets, sets, or displays help information about this bot's config", aliases=["cf"])
    @commands.has_permissions(administrator = True)
    async def config(self, ctx, action, key = None, value = None):
        actions = ["get", "set" , "list", "help"]
        if action not in actions:
            return await ctx.send(f"Unrecognized action '{action}'.")
        
        match action:
            case "get":
                config_value = config.get_config(ctx.guild.id, key)
                if config_value == "":
                    await ctx.send(f"Not config [{key}] found.")
                else:
                    await ctx.send(f"[{key}]: {config.get_config(ctx.guild.id, key)}")
            case "set":
                changed = config.set_config(ctx.guild.id, key, value)
                if changed:
                    await ctx.send(f"Successfully changed [{key}].")
                else:
                    await ctx.send(f"Config option [{key}] not found.")
            case "list":
                configs = config.get_configs()
                if configs != "":
                    embed = discord.Embed(
                        title="Configurations",
                        description="Displays all available configs",
                        color=discord.Color.blue()
                    )

                    for config_ in configs:
                        embed.add_field(name=(configs.index(config_) + 1), value=config_, inline=True)

                    # Change to create embed of all configs
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Couldn't return config list.")
            case "help":
                await ctx.send(f"[{key}] - {config.config_help[key]}")
            case _:
                return Exception

async def setup(bot):
    await bot.add_cog(Help(bot))
