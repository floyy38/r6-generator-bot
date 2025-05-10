import discord
import time
from discord.ext import commands
from discord import app_commands
from utils.access import premium_users, save_premium
from utils.cooldowns import set_custom_cooldown
from datetime import datetime

DURATION_MAP = {
    "1 Day": 1,
    "3 Days": 3,
    "7 Days": 7,
    "30 Days": 30,
    "Lifetime": "lifetime"
}

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addaccess", description="Grant premium access to a user")
    @app_commands.describe(user="User to grant access to", duration="Premium access duration")
    @app_commands.choices(duration=[
        app_commands.Choice(name="1 Day", value="1 Day"),
        app_commands.Choice(name="3 Days", value="3 Days"),
        app_commands.Choice(name="7 Days", value="7 Days"),
        app_commands.Choice(name="30 Days", value="30 Days"),
        app_commands.Choice(name="Lifetime", value="Lifetime"),
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def addaccess(self, interaction: discord.Interaction, user: discord.User, duration: app_commands.Choice[str]):
        user_id = str(user.id)
        selected = duration.value

        if selected == "Lifetime":
            expiry = "lifetime"
        else:
            days = DURATION_MAP[selected]
            expiry = int(time.time() + days * 86400)

        premium_users[user_id] = expiry
        save_premium(premium_users)

        exp_display = "Never" if expiry == "lifetime" else f"<t:{int(expiry)}:R>"
        embed = discord.Embed(title="👑 Premium Access Granted", color=discord.Color.gold())
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Duration", value=selected, inline=True)
        embed.add_field(name="Expires", value=exp_display, inline=True)
        embed.add_field(name="Granted By", value=interaction.user.mention, inline=False)
        embed.set_footer(text="Floyy Premium Access Management")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="removeaccess", description="Remove premium access from a user")
    @app_commands.describe(user="User to remove premium from")
    @app_commands.checks.has_permissions(administrator=True)
    async def removeaccess(self, interaction: discord.Interaction, user: discord.User):
        user_id = str(user.id)
        if user_id in premium_users:
            del premium_users[user_id]
            save_premium(premium_users)
            msg = f"❌ **{user.mention}** has been removed from premium access."
        else:
            msg = f"ℹ️ **{user.mention}** was not found in the premium list."
        await interaction.response.send_message(msg)

    @app_commands.command(name="listaccess", description="View all users with premium access")
    @app_commands.checks.has_permissions(administrator=True)
    async def listaccess(self, interaction: discord.Interaction):
        if not premium_users:
            await interaction.response.send_message("❌ No users currently have premium access.")
            return

        lines = []
        for uid, expiry in premium_users.items():
            member = interaction.guild.get_member(int(uid))
            name = member.mention if member else f"User ID {uid}"
            if expiry == "lifetime":
                expires = "💎 Lifetime"
            else:
                try:
                    expires = f"<t:{int(expiry)}:R>"
                except:
                    expires = "⚠️ Invalid"
            lines.append(f"{name} — {expires}")

        msg = "\n".join(lines)
        embed = discord.Embed(title="📋 Premium Access List", description=msg, color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setcooldown", description="Set a custom cooldown time for a user")
    @app_commands.describe(user="User to modify", tier="Tier to modify (free or premium)", seconds="Cooldown in seconds")
    @app_commands.checks.has_permissions(administrator=True)
    async def setcooldown(self, interaction: discord.Interaction, user: discord.User, tier: str, seconds: int):
        tier = tier.lower()
        if tier not in ["free", "premium"]:
            await interaction.response.send_message("❌ Tier must be `free` or `premium`.", ephemeral=True)
            return

        set_custom_cooldown(user.id, tier, seconds)
        embed = discord.Embed(
            title="⏱️ Custom Cooldown Set",
            description=f"User: {user.mention}\nTier: **{tier.capitalize()}**\nCooldown: **{seconds} seconds**",
            color=discord.Color.orange()
        )
        embed.set_footer(text="User-specific cooldowns override defaults.")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
