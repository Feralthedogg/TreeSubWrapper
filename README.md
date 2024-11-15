# TreeSubWrapper

TreeSubWrapper is a Python utility designed to simplify the creation of subcommands for Discord bots using the `discord.py` library. It extends the functionality of `app_commands` by enabling nested groups and intuitive command organization. This library integrates seamlessly with both `discord.Client` and `discord.ext.commands.Bot` objects.

---

## Features

- Simple subcommand creation using the `@tree_sub.command` decorator.
- Support for nested groups to mimic hierarchical command structures.
- Compatible with `discord.py`'s `app_commands` API.
- Works with both `discord.Client` and `commands.Bot`.

---

## Installation

Copy the `TreeSubWrapper` class into your project and use it directly.

---

## Quick Start

### Import and Initialization

To use `TreeSubWrapper`, import the `tree_sub` instance and initialize it with your bot.

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

#### Single Group Command

Define subcommands within a single group:

```python
@tree_sub.command(
    groups="example",
    name="say",
    description="Repeats the text you provide"
)
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"You said: {text}")
```

#### Nested Group Command

Use multiple groups to create a nested command structure:

```python
@tree_sub.command(
    groups=["example", "nested"],
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
    groups="test",
    name="hello",
    description="Sends a greeting"
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")

bot.run("TOKEN")
```

---

## API Reference

### `TreeSubWrapper`

- **Purpose**: Handles subcommand grouping and registration.
- **Methods**:
  - `set_bot(bot: discord.Client)`: Connects the `TreeSubWrapper` to a bot instance.
  - `command(groups=None, name: str, description: str)`: Decorator for defining subcommands.

---

## Example Commands

### Command with Single Group
```python
@tree_sub.command(
    groups="utilities",
    name="ping",
    description="Check the bot's latency"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")
```

### Command with Nested Groups
```python
@tree_sub.command(
    groups=["admin", "tools"],
    name="restart",
    description="Restarts the bot"
)
async def restart(interaction: discord.Interaction):
    await interaction.response.send_message("Restarting...")
    # Add restart logic here
```

---

## Error Handling

### Common Errors

1. **"Bot object is not initialized"**:
   - Ensure you use `TreeSubWrapper.set_bot(bot)` before defining commands.

2. **Command not working**:
   - Ensure `await bot.tree.sync()` is called in the `on_ready` event.

---

## Contributing

If you encounter issues or have ideas for new features, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
