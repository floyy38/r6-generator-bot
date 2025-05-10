import os
import time
import discord
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

async def log_generation(interaction: discord.Interaction, tier: str, account: str):
    try:
        user = interaction.user
        channel = await interaction.client.fetch_channel(LOG_CHANNEL_ID)

        embed = discord.Embed(
            title="✅ New Account Generated",
            color=discord.Color.green()
        )
        embed.add_field(name="👤 User", value=f"```{user.mention}```", inline=False)
        embed.add_field(name="🏷️ Tier", value=f"```{tier.upper()}```", inline=True)
        embed.add_field(name="🔑 Account", value=f"```{account}```", inline=False)
        embed.set_footer(text=f"🕓 Generated at {time.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        await channel.send(embed=embed)
    except Exception as e:
        print(f"⚠️ Logging failed: {e}")
