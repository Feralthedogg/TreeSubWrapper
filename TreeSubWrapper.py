import discord
from discord.ext.commands import Bot
from discord import app_commands
import weakref

class TreeSubWrapper:
    def __init__(self):
        self._bot_ref = None
        self.commands = {}

    @property
    def bot(self):
        if self._bot_ref is None or self._bot_ref() is None:
            raise RuntimeError("Bot object is not initialized. Please use TreeSubBot or TreeSubClient.")
        return self._bot_ref()

    def set_bot(self, bot: discord.Client):
        self._bot_ref = weakref.ref(bot)

    def command(self, *, group: str = "default", **kwargs):
        def decorator(func):
            if self.bot is None:
                raise RuntimeError("Bot object is not initialized. Please initialize with discord.Client or Bot.")

            if group not in self.commands:
                self.commands[group] = app_commands.Group(
                    name=group,
                    description=f"{group} command group"
                )
                self.bot.tree.add_command(self.commands[group])

            command = app_commands.Command(
                name=kwargs.pop("name", func.__name__),
                callback=func,
                **kwargs
            )
            self.commands[group].add_command(command)
            return func

        return decorator

tree_sub = TreeSubWrapper()

class TreeSubClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tree_sub.set_bot(self)

class TreeSubBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tree_sub.set_bot(self)
