# example.py

import discord
from discord.ext import commands
from TreeSubWrapper import tree_sub, BotNotInitializedError

INTENTS = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=INTENTS)
tree_sub.set_bot(bot)
tree_sub.set_initial_settings(debug=True, version="1.0.0")

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    await bot.tree.sync()
    print("Commands have been globally synced.")

# Single Group Example
@tree_sub.command(
    groups="math",
    name="add",
    description="Adds two numbers"
)
async def add(interaction: discord.Interaction, a: int, b: int):
    if tree_sub.initial_settings.get("debug"):
        print(f"Debug: add command called with a={a}, b={b}")
    await interaction.response.send_message(f"The sum of {a} and {b} is {a + b}")

# Multiple Groups Example
@tree_sub.command(
    groups=["math", "advanced"],
    name="power",
    description="Calculates the power of a number"
)
async def power(interaction: discord.Interaction, base: int, exponent: int):
    if tree_sub.initial_settings.get("debug"):
        print(f"Debug: power command called with base={base}, exponent={exponent}")
    result = base ** exponent
    await interaction.response.send_message(f"{base} raised to the power of {exponent} is {result}")

# Command Example with Error Handling
@tree_sub.command(
    groups="admin",
    name="shutdown",
    description="Shuts down the bot (admin only)"
)
@commands.has_permissions(administrator=True)
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message("Shutting down the bot...")
    await bot.close()

# Command Example Using Initial Settings
@tree_sub.command(
    groups="info",
    name="version",
    description="Shows the bot version"
)
async def version(interaction: discord.Interaction):
    bot_version = tree_sub.initial_settings.get("version", "Unknown")
    await interaction.response.send_message(f"The bot version is {bot_version}")

try:
    bot.run("TOKEN")
except BotNotInitializedError as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Bot has been terminated.")
    bot.close()
