# TreeSubWrapper

TreeSubWrapper is a Python utility that simplifies the creation of subcommands for Discord bots using the `discord.py` library. It extends the functionality of `app_commands` to organize commands into intuitive groups. This library is designed to work seamlessly with both `discord.Client` and `discord.ext.commands.Bot` objects.

## Features

- Simple subcommand creation using the `@tree_sub.command` decorator.
- Automatically organizes commands into logical structures.
- Fully compatible with `discord.py`'s `app_commands` API.
- Works with both `discord.Client` and `commands.Bot`.

---

## Installation

Copy the `TreeSubWrapper` class and its dependencies into your project, or package it as a module if needed.

---

## Quick Start

### Import and Initialization

To use `TreeSubWrapper`, simply import the `tree_sub` instance and initialize it.

```python
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
```

---

### Creating Subcommands

Define subcommands using the `@tree_sub.command` decorator. Grouping is handled by specifying the `group` argument.

```python
@tree_sub.command(
    group="example",
    name="say",
    description="Repeats the text you provide"
)
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"You said: {text}")

@tree_sub.command(
    group="example",
    name="shout",
    description="Shouts the text in uppercase"
)
async def shout(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"{text.upper()}!")
```

---

### Using with `commands.Bot`

If you're using `commands.Bot`, manually initialize the `tree_sub` instance.

```python
import discord
from discord.ext.commands import Bot
from TreeSubWrapper import tree_sub

INTENTS = discord.Intents.all()
bot = Bot(command_prefix="!", intents=INTENTS)
tree_sub.set_bot(bot)

@tree_sub.command(
    group="test",
    name="hello",
    description="Sends a greeting"
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")

bot.run("TOKEN")
```

---

## Classes

### `TreeSubWrapper`

- **Purpose**: Handles subcommand grouping and registration.
- **Methods**:
  - `set_bot(bot: discord.Client)`: Connects the `TreeSubWrapper` to a bot instance.
  - `command(group: str = "default", **kwargs)`: Decorator for defining subcommands.

### `TreeSubBot`

- **Extends**: `commands.Bot`
- Automatically initializes `tree_sub` with the bot instance.

### `TreeSubClient`

- **Extends**: `discord.Client`
- Automatically initializes `tree_sub` with the client instance.

---

## Example Project

```python
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
```

---

## Error Handling

### Common Errors

1. **"Bot object is not initialized"**:
   - Ensure you use `TreeSubBot`, `TreeSubClient`, or call `tree_sub.set_bot(bot)` before using `@tree_sub.command`.

2. **Command not working**:
   - Check if `await bot.tree.sync()` is called in the `on_ready` event.

---

## Contributing

Feel free to submit issues or pull requests to enhance the library!

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

