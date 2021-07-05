# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import os
import sys

from . import bot, config, const
from .logging import logger


async def main():
    """Entrypoint"""
    logger.info("Loading config file")
    cfg = config.Config()
    try:
        cfg.load(const.CONFIG_FILE)
    except:
        logger.warning("Config file does not exist. Creating")
        cfg.save(const.CONFIG_FILE)

    if len(sys.argv) > 1 and sys.argv[1] == "-add":
        name = ""
        while name == "":
            name = input("Enter session name: ").strip()

        try:
            os.mkdir("data/")
        except:
            pass
        _bot = bot.Bot(os.path.join(const.DATA_FOLDER, name), cfg)
        await _bot.start(login_only=True)
        sys.exit(0)

    for session in filter(
        lambda x: len(x) > 8 and x[-8:] == ".session", os.listdir(const.DATA_FOLDER)
    ):
        logger.info('Initializing bot "%s"', session)
        _bot = bot.Bot(os.path.join(const.DATA_FOLDER, session[:-8]), cfg)

        logger.info("Loading local modules")
        base_folder = os.path.join(
            const.ROOT_DIRECTORY, __package__, const.MODULES_FOLDER
        )
        for file in [
            "core.py",
            *filter(
                lambda x: len(x) > 3
                and x[-3:] == ".py"
                and x[0] != "_"
                and x != "core.py",
                os.listdir(base_folder),
            ),  # pasted from ftg
        ]:
            path = os.path.join(base_folder, file)
            logger.info('Loading module "%s"', path)
            try:
                mod = _bot.load_module(path)
                if file == "core.py":
                    mod.bot = _bot
                logger.info('Successfully loaded module "%s"', mod.name)
            except Exception as ex:
                logger.exception('Cannot load module "%s": %s', path, ex)

        logger.info("Loading remote modules")
        for url in [
            *map(
                const.MODULES_URL.format,
                const.MODULES_DEFAULT + _bot.storage.dict.get("modules_from_repo", []),
            ),
            *_bot.storage.dict.get("modules", []),
        ]:
            logger.info('Loading module from "%s"', url)
            try:
                mod = _bot.load_module_from_url(url)
                logger.info('Successfully loaded remote module "%s"', mod.name)
            except Exception as ex:
                logger.exception('Cannot load module from "%s": %s', url, ex)

        logger.info("Starting bot")
        await _bot.start()
