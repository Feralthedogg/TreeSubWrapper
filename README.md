# TreeSubWrapper

**TreeSubWrapper** is a Python utility designed to simplify the creation of subcommands for Discord bots using the `discord.py` library. It extends the functionality of `app_commands` by enabling nested groups and intuitive command organization. This library integrates seamlessly with both `discord.Client` and `discord.ext.commands.Bot` objects.

---

## Features

- **Easy Subcommand Creation**: Use the `@tree_sub.command` decorator to define commands effortlessly.
- **Nested Group Support**: Create hierarchical command structures with nested groups.
- **Context Manager Integration**: Utilize `async with` for automatic command synchronization.
- **Custom Error Handling**: Provides clear exceptions like `BotNotInitializedError` for better debugging.
- **Initial Settings Configuration**: Set initial settings for global access within commands.
- **Guild-specific Synchronization**: Optionally sync commands to specific guilds (servers).
- **Compatibility**: Works with both `discord.Client` and `commands.Bot`.

---

## Installation

Simply copy the `TreeSubWrapper` class into your project and import the `tree_sub` instance.

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

# Optional: Set initial settings
tree_sub.set_initial_settings(debug=True, version="1.0.0")

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    await bot.tree.sync()
    print("Commands have been globally synced.")
```

---

### Creating Subcommands

#### Single Group Command

Define a command within a single group:

```python
# Single Group Example
@tree_sub.command(
    groups="utilities",
    name="echo",
    description="Echoes the message you provide"
)
async def echo(interaction: discord.Interaction, message: str):
    if tree_sub.initial_settings.get("debug"):
        print(f"Debug: echo command called with message='{message}'")
    await interaction.response.send_message(f"You said: {message}")
```

#### Nested Group Command

Use multiple groups to create a nested command structure:

```python
# Multiple Groups Example
@tree_sub.command(
    groups=["admin", "tools"],
    name="broadcast",
    description="Broadcasts a message to all channels"
)
@commands.has_permissions(administrator=True)
async def broadcast(interaction: discord.Interaction, message: str):
    if tree_sub.initial_settings.get("debug"):
        print(f"Debug: broadcast command called with message='{message}'")
    for channel in interaction.guild.text_channels:
        await channel.send(message)
    await interaction.response.send_message("Broadcast completed.")
```

---

### Using with `commands.Bot`

If you're using `commands.Bot`, you can initialize the `tree_sub` instance as shown above. The library integrates seamlessly with both `discord.Client` and `commands.Bot`.

---

## Context Manager Usage

`TreeSubWrapper` supports the use of an asynchronous context manager for automatic command synchronization and cleanup.

```python
async with tree_sub:
    # Define your commands here
    @tree_sub.command(
        groups="fun",
        name="joke",
        description="Tells a random joke"
    )
    async def joke(interaction: discord.Interaction):
        await interaction.response.send_message("Why did the programmer quit his job? Because he didn't get arrays!")
```

- Upon exiting the `async with` block, `__aexit__` will automatically sync the commands and perform cleanup.
- This approach is optional and can be used when you prefer automatic management.

---

## API Reference

### `TreeSubWrapper`

- **Purpose**: Handles subcommand grouping, registration, and synchronization.
- **Methods**:
  - `set_bot(bot: discord.Client)`: Connects the `TreeSubWrapper` to a bot instance.
  - `set_sync_guilds(guilds)`: Specifies guilds for command synchronization.
  - `set_initial_settings(**settings)`: Stores initial settings accessible within commands.
  - `command(groups=None, name: str, description: str)`: Decorator for defining subcommands.
- **Properties**:
  - `bot`: Returns the bot instance. Raises `BotNotInitializedError` if not set.
  - `initial_settings`: A dictionary storing initial settings.

### Custom Exceptions

- **`BotNotInitializedError`**: Raised when the bot instance is not set before command registration.

---

## Example Commands

### Command with Error Handling

```python
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
```

### Command Using Initial Settings

```python
# Command Example Using Initial Settings
@tree_sub.command(
    groups="info",
    name="version",
    description="Shows the bot version"
)
async def version(interaction: discord.Interaction):
    bot_version = tree_sub.initial_settings.get("version", "Unknown")
    await interaction.response.send_message(f"The bot version is {bot_version}")
```

---

## Error Handling

### Common Errors

1. **"Bot object is not initialized"**:
   - **Cause**: The bot instance was not set before defining commands.
   - **Solution**: Ensure you call `tree_sub.set_bot(bot)` before registering commands.

2. **Command not working or not appearing**:
   - **Cause**: Commands were not synced with Discord.
   - **Solution**: Call `await bot.tree.sync()` in the `on_ready` event or use the context manager.

3. **Permission Errors**:
   - **Cause**: User lacks the required permissions to execute a command.
   - **Solution**: Use decorators like `@commands.has_permissions(administrator=True)` to manage access.

---

## Advanced Usage

### Synchronizing Commands to Specific Guilds

For faster command registration during development, you can sync commands to specific guilds:

```python
# Set guilds to sync commands with
GUILD_IDS = [123456789012345678]  # Replace with your guild IDs
GUILDS = [discord.Object(id=guild_id) for guild_id in GUILD_IDS]
tree_sub.set_sync_guilds(GUILDS)

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    for guild in tree_sub.sync_guilds:
        await bot.tree.sync(guild=guild)
    print(f"Commands have been synced to guilds: {GUILD_IDS}")
```

---

## Contributing

If you encounter issues or have suggestions for new features, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## Security Notice

**Important**: Never share your bot's token in your code or publicly. Always keep it secure by using environment variables or a separate configuration file not committed to version control.

---

## Disclaimer

This library is designed to assist in organizing Discord bot commands and is provided as-is. Please ensure you comply with Discord's Developer Terms of Service when using this library.

---

## Acknowledgements

Special thanks to the Discord.py community for their contributions and support.

---

## Full Example

Here's a full example combining all features:

```python
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
    groups="fun",
    name="echo",
    description="Echoes the message you provide"
)
async def echo(interaction: discord.Interaction, message: str):
    if tree_sub.initial_settings.get("debug"):
        print(f"Debug: echo command called with message='{message}'")
    await interaction.response.send_message(f"You said: {message}")

# Multiple Groups Example
@tree_sub.command(
    groups=["admin", "tools"],
    name="broadcast",
    description="Broadcasts a message to all channels"
)
@commands.has_permissions(administrator=True)
async def broadcast(interaction: discord.Interaction, message: str):
    if tree_sub.initial_settings.get("debug"):
        print(f"Debug: broadcast command called with message='{message}'")
    for channel in interaction.guild.text_channels:
        await channel.send(message)
    await interaction.response.send_message("Broadcast completed.")

# Command with Error Handling
@tree_sub.command(
    groups="admin",
    name="shutdown",
    description="Shuts down the bot (admin only)"
)
@commands.has_permissions(administrator=True)
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message("Shutting down the bot...")
    await bot.close()

# Command Using Initial Settings
@tree_sub.command(
    groups="info",
    name="version",
    description="Shows the bot version"
)
async def version(interaction: discord.Interaction):
    bot_version = tree_sub.initial_settings.get("version", "Unknown")
    await interaction.response.send_message(f"The bot version is {bot_version}")

try:
    bot.run("TOKEN")  # Replace with your actual bot token
except BotNotInitializedError as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Bot has been terminated.")
    bot.close()
```

---

**Note**: Replace `"YOUR_BOT_TOKEN"` with your actual bot token. However, never share your bot token publicly or commit it to version control.

---

## Getting Help

If you need assistance with `TreeSubWrapper`, feel free to reach out via the project's issue tracker or consult the [Discord.py documentation](https://discordpy.readthedocs.io/en/stable/).

---

## Frequently Asked Questions

### Q: Can I use `TreeSubWrapper` with cogs?

A: Yes, you can integrate `TreeSubWrapper` within cogs by setting the bot instance within the cog and registering commands accordingly.

### Q: How do I handle command permissions?

A: Use decorators from `discord.ext.commands`, such as `@commands.has_permissions()`, to manage permissions for commands.

### Q: Is `TreeSubWrapper` compatible with the latest version of `discord.py`?

A: `TreeSubWrapper` is designed to work with `discord.py` versions that support `app_commands`. Ensure you're using a compatible version.

---

## Support

If you find this utility helpful, consider giving it a star on GitHub or contributing to its development.

---

By using `TreeSubWrapper`, you can streamline your Discord bot development with organized and maintainable command structures.
