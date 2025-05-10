import discord
from discord.ext import commands
from discord import app_commands
from utils.file_io import count_accounts

class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stock", description="Check current account stock")
    async def stock(self, interaction: discord.Interaction):
        free_count = count_accounts("data/free.txt")
        premium_count = count_accounts("data/premium.txt")

        embed = discord.Embed(title="📦 Account Stock", color=discord.Color.blue())
        embed.add_field(name="🆓 Free", value=f"**{free_count}**", inline=False)
        embed.add_field(name="💎 Premium", value=f"**{premium_count}**", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stock(bot))
