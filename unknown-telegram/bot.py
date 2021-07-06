# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

from telethon import TelegramClient, events

from . import command, config, const, loader, sdk, storage
from .logging import logger


class Bot:
    """Works with Telegram account"""

    def __init__(self, name: str, cfg: config.Config):
        self.modules = loader.Modules()
        self.storage = storage.Storage(name + ".storage")
        self.client = TelegramClient(
            name,
            api_id=cfg.id,
            api_hash=cfg.hash,
            app_version=cfg.app_version,
            device_model=cfg.device_model,
            system_version=cfg.system_version,
        )
        self.client.parse_mode = "html"

    def load_module(self, path: str) -> loader.Module:
        """Load module from given path"""
        logger.info('Loading module "%s"', path)
        spec = self.modules.load_spec(path)
        mod = self.modules.load_module_from_spec(spec)
        mod.storage = self.storage.dict.setdefault(mod.__module__, {})
        self.modules.register_module(mod)
        return mod

    def load_module_from_url(self, url: str) -> loader.Module:
        """Load module from given URL"""
        logger.info('Loading module from "%s"', url)
        mod = self.modules.load_module_from_url(url)
        mod.storage = self.storage.dict.setdefault(mod.__module__, {})
        self.modules.register_module(mod)
        return mod

    async def incoming_handler(self, event):
        """Handler for incoming messages"""
        for handler in self.modules.incoming:
            try:
                await handler(event)
            except Exception as ex:
                logger.exception(ex)
            self.storage.sync()

    async def outgoing_handler(self, event):
        """Handler for outgoing messages"""
        cmd = command.Command(event.message.raw_text)
        if cmd.text == "":
            return

        if cmd.cmd in self.modules.commands:
            try:
                await self.modules.commands[cmd.cmd](event, cmd)
            except Exception as ex:
                logger.exception(ex)
                await sdk.send(
                    event.message,
                    const.MESSAGE_ERROR,
                )
            self.storage.sync()

    async def start(self, login_only=False):
        """Start the bot"""
        await self.client.start(lambda: input("Enter your phone: "))
        if await self.client.is_bot():
            await self.client.log_out()
            raise Exception("Bots are not supported")
        if login_only:
            return

        start_message = self.storage.dict.get("start_message", None)
        if start_message is not None:
            try:
                await self.client.edit_message(
                    start_message["entity"], start_message["id"], start_message["text"]
                )
            except:
                pass
            del self.storage.dict["start_message"]
            self.storage.sync()

        self.client.add_event_handler(
            self.incoming_handler, events.NewMessage(incoming=True)
        )
        self.client.add_event_handler(
            self.outgoing_handler, events.NewMessage(outgoing=True, forwards=False)
        )
