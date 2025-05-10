import discord, time, os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils.file_io import get_account
from utils.logger import log_generation
from utils.cooldowns import check_cooldown, update_cooldown
from utils.access import has_active_premium

load_dotenv()
FREE_CHANNEL_ID = int(os.getenv("FREE_CHANNEL_ID"))
PREMIUM_CHANNEL_ID = int(os.getenv("PREMIUM_CHANNEL_ID"))

class Gen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gen", description="Generate a free or premium R6 account")
    @app_commands.describe(tier="Choose either free or premium")
    async def gen(self, interaction: discord.Interaction, tier: str):
        user_id = str(interaction.user.id)
        tier = tier.lower()
        channel_id = interaction.channel.id

        if tier not in ["free", "premium"]:
            await interaction.response.send_message("🚫 Invalid tier. Use `free` or `premium`.", ephemeral=True)
            return

        if tier == "free" and channel_id != FREE_CHANNEL_ID:
            await interaction.response.send_message("❌ Please use this command in the **#🤖│free-gen** channel.", ephemeral=True)
            return

        if tier == "premium" and channel_id != PREMIUM_CHANNEL_ID:
            await interaction.response.send_message("❌ Please use this command in the **#🤖│prem-gen** channel.", ephemeral=True)
            return

        if not check_cooldown(user_id, tier):
            await interaction.response.send_message("⏳ You are on cooldown. Please wait.", ephemeral=True)
            return

        if tier == "premium" and not has_active_premium(user_id):
            await interaction.response.send_message("🔒 You don’t have active premium access.", ephemeral=True)
            return

        filename = f"data/{tier}.txt"
        account = get_account(filename)

        if not account:
            await interaction.response.send_message(f"❌ No {tier} accounts left.", ephemeral=True)
            return

        email, password = account.split(":")
        embed = discord.Embed(title="🎁 R6 Account Generated", color=discord.Color.blurple())
        embed.add_field(name="📧 Email", value=f"```{email}```", inline=True)
        embed.add_field(name="🔑 Password", value=f"```{password}```", inline=True)

        try:
            await interaction.user.send(embed=embed)
            update_cooldown(user_id, tier)

            confirm = discord.Embed(
                title="✅ Account Sent",
                description="We've delivered your account to your **DMs**! Check your inbox.",
                color=discord.Color.green()
            )
            confirm.set_footer(text="Enjoy your account! If it doesn’t work, open a ticket.")
            await interaction.response.send_message(embed=confirm, ephemeral=False)
            await log_generation(interaction, tier, account)


        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I couldn't send you a DM. Please enable DMs from server members.", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Gen(bot))
