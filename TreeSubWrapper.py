import discord
from discord.ext.commands import Bot
from discord import app_commands
import weakref

class TreeSubWrapper:
    def __init__(self):
        self._bot_ref = None
        self.groups = {}

    @property
    def bot(self):
        if self._bot_ref is None or self._bot_ref() is None:
            raise RuntimeError("Bot object is not initialized. Please use TreeSubBot or TreeSubClient.")
        return self._bot_ref()

    def set_bot(self, bot: discord.Client):
        self._bot_ref = weakref.ref(bot)

    def command(self, *, groups=None, name: str, description: str):
        """
        Decorator to create commands with multiple groups to mimic a spaced structure.
        :param groups: Either a single group name (str) or a list of group names (list).
        :param name: Command name.
        :param description: Command description.
        """
        def decorator(func):
            if self.bot is None:
                raise RuntimeError("Bot object is not initialized. Please initialize with discord.Client or Bot.")

            parent = self.bot.tree

            if isinstance(groups, str):
                groups_list = [groups]
            elif isinstance(groups, list):
                groups_list = groups
            else:
                groups_list = []

            for group_name in groups_list:
                if group_name not in self.groups:
                    new_group = app_commands.Group(
                        name=group_name,
                        description=f"{group_name} command group"
                    )
                    self.groups[group_name] = new_group
                    parent.add_command(new_group)
                parent = self.groups[group_name]

            command = app_commands.Command(
                name=name,
                callback=func,
                description=description
            )
            parent.add_command(command)
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
