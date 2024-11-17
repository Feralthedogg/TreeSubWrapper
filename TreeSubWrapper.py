# TreeSubWrapper.py

import discord
from discord.ext.commands import Bot
from discord import app_commands
import weakref
import asyncio

class BotNotInitializedError(Exception):
    pass

class TreeSubWrapper:
    def __init__(self):
        self._bot_ref = None
        self.groups = {}
        self._commands_to_sync = []
        self.sync_guilds = None
        self.initial_settings = {}

    async def __aenter__(self):
        if self._bot_ref is None or self._bot_ref() is None:
            raise BotNotInitializedError(
                "Bot object is not initialized. Please set the bot before using the context manager."
            )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.bot.wait_until_ready()
        if self.sync_guilds:
            for guild in self.sync_guilds:
                await self.bot.tree.sync(guild=guild)
        else:
            await self.bot.tree.sync()
        self.groups.clear()
        self._commands_to_sync.clear()

    @property
    def bot(self):
        if self._bot_ref is None or self._bot_ref() is None:
            raise BotNotInitializedError(
                "Bot object is not initialized. Please use TreeSubBot or TreeSubClient."
            )
        return self._bot_ref()

    def set_bot(self, bot: discord.Client):
        self._bot_ref = weakref.ref(bot)

    def set_sync_guilds(self, guilds):
        self.sync_guilds = guilds

    def set_initial_settings(self, **settings):
        self.initial_settings.update(settings)

    def command(self, *, groups=None, name: str, description: str):
        def decorator(func):
            if self.bot is None:
                raise BotNotInitializedError(
                    "Bot object is not initialized. Please initialize with discord.Client or Bot."
                )

            parent = self.bot.tree

            if isinstance(groups, str):
                groups_list = [groups]
            elif isinstance(groups, list):
                groups_list = groups
            else:
                groups_list = []

            for group_name in groups_list:
                if group_name not in self.groups:
                    existing_command = parent.get_command(group_name)
                    if existing_command:
                        parent.remove_command(group_name)
                    new_group = app_commands.Group(
                        name=group_name,
                        description=f"{group_name} command group"
                    )
                    self.groups[group_name] = new_group
                    parent.add_command(new_group)
                parent = self.groups[group_name]

            existing_command = parent.get_command(name)
            if existing_command:
                parent.remove_command(name)

            command = app_commands.Command(
                name=name,
                callback=func,
                description=description
            )
            parent.add_command(command)
            self._commands_to_sync.append(command)

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
