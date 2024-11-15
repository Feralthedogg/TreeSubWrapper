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

@tree_sub.command(
    group="math",
    name="add",
    description="Adds two numbers"
)
async def add(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"The sum of {a} and {b} is {a + b}")

bot.run("TOKEN")
