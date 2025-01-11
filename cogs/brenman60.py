import discord
from discord.ext import commands
from urllib.request import urlretrieve
import os
import json
import asyncio

class brenman60(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sends message containing information for the LinkedIn page.
    @commands.command(name="linkedin", description="Displays LinkedIn page", aliases=["li"])
    async def linkedin(self, ctx):
        embed = discord.Embed()
        embed.title = "LinkedIn Page"
        embed.url = "https://www.linkedin.com/in/brennan-kunicki-55a83a30a"
        embed.color = discord.Color.blue()
        embed.set_thumbnail(url="https://cdn-icons-png.freepik.com/256/3991/3991775.png?semt=ais_hybrid")
        await ctx.send(embed=embed)

    # Sends message containing information for the GitHub page.
    @commands.command(name="github", description="Displays GitHub page", aliases=["gh"])
    async def github(self, ctx):
        embed = discord.Embed()
        embed.title = "GitHub Page"
        embed.url = "https://github.com/brenman60"
        embed.color = discord.Color.blue()
        embed.set_thumbnail(url="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png")
        await ctx.send(embed=embed)

    # Sends message containing information for the portfolio page.
    @commands.command(name="portfolio", description="Displays Portfolio page", aliases=["resume", "pf"])
    async def portfolio(self, ctx):
        embed = discord.Embed()
        embed.title = "Portfolio Page"
        embed.url = "https://brenman60.github.io/portfolio/"
        embed.color = discord.Color.blue()
        embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/2354888042055965527/751F2CC84C8EF889315DD53385E52CAB2593A744/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false")
        await ctx.send(embed=embed)

    # Sends an embed with information about the certification. 
    @commands.command(name="certification", description="Displays information about one of my certifications", aliases=["cert"])
    async def certification(self, ctx, *, name):
        if ctx.author == self.bot.user:
            return
        
        async with ctx.channel.typing():
            url = (
                "https://raw.githubusercontent.com/brenman60/portfolio/"
                "refs/heads/main/public/data/certifications.json"
            )
            filename = "downloaded/certifications.json"

            if not os.path.exists("downloaded/"):
                os.mkdir("downloaded/")

            path, headers = urlretrieve(url, filename)
            with open(path, "r") as file:
                cert_data = json.load(file)
                
                cert_found = False
                for company, company_certs in cert_data.items():
                    for cert_key, cert in company_certs.items():
                        if name == cert["name"]:
                            cert_found = True

                            embed = discord.Embed()
                            embed.title = name
                            embed.color = discord.Color.blue()
                            embed.url = cert["link"]
                            embed.add_field(name="Id:", value=cert["id"], inline=True)
                            embed.add_field(name="Issued:", value=cert["issued"], inline=True)

                            await ctx.send(embed=embed)
                            break
                    if cert_found:
                        break
                
                if not cert_found:
                    await ctx.send("Certificate not found.")                     

async def setup(bot):
    await bot.add_cog(brenman60(bot))
