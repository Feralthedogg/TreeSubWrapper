import discord
from discord.ext import commands
from TreeSubWrapper import tree_sub

INTENTS = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=INTENTS)
tree_sub.set_bot(bot)

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    await bot.tree.sync()

# Single Group Example
@tree_sub.command(
    groups="math",
    name="add",
    description="Adds two numbers"
)
async def add(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"The sum of {a} and {b} is {a + b}")

# Multiple Groups Example
@tree_sub.command(
    groups=["math", "advanced"],
    name="power",
    description="Calculates the power of a number"
)
async def power(interaction: discord.Interaction, base: int, exponent: int):
    result = base ** exponent
    await interaction.response.send_message(f"{base} raised to the power of {exponent} is {result}")

bot.run("TOKEN")
