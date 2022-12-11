# -*- coding: utf-8 -*-
# Coded by @altfoxie with power of Senko!

import os
import subprocess
import sys

from git import Repo

from .. import __main__, bot, const, sdk
from ..loader import AlreadyLoaded
from ..logging import logger


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "Core"
        self.bot: bot.Bot

    def restart(self):
        self.bot.storage.sync()  # sync storage before restart
        python = sys.executable
        os.execl(python, python, "-m", __main__.__package__)  # FUCK WINDOWS!

    async def help_cmd(self, event: sdk.Event, command: sdk.Command):
        help_dict = {}
        for key, val in self.bot.modules.commands.items():
            help_dict[val.__self__.name] = help_dict.get(val.__self__.name, []) + [key]

        help_str = "\n".join(
            [f'<b>• {k}:</b> <code>{", ".join(v)}</code>' for k, v in help_dict.items()]
        )
        await sdk.send(event.message, "<b>Help for Unknown Telegram</b>\n\n" + help_str)

    async def restart_cmd(self, event: sdk.Event, command: sdk.Command):
        message = (await sdk.send(event.message, "<b>Restarting...</b>"))[0]
        self.bot.storage.dict["start_message"] = {
            "entity": message.chat,
            "id": message.id,
            "text": "<b>Restarted!</b>",
        }
        self.restart()

    async def update_cmd(self, event: sdk.Event, command: sdk.Command):
        if const.IS_DOCKER:
            await sdk.send(
                event.message, "<b>You need to pull Docker Image manually.</b>"
            )
            return

        await sdk.send(event.message, "<b>Fetching last version...</b>")
        repo = Repo(const.ROOT_DIRECTORY)

        # Delete origin if exist
        try:
            origin = repo.remotes["origin"]
            repo.delete_remote(origin)
        except:
            pass

        # Create new origin
        try:
            origin = repo.create_remote("origin", const.GIT_URL)
        except:
            await sdk.send(event.message, "<b>Cannot create origin.</b>")
            return

        # Get local commit hash
        local_hash, remote_hash = "", ""
        try:
            local_hash = str(repo.commit("main"))
        except:
            pass

        # Fetch and get remote commit hash
        try:
            fetch = origin.fetch()
            remote_hash = str(fetch[0].commit)
        except:
            await sdk.send(event.message, "<b>Cannot fetch from origin.</b>")
            return

        # Create main branch
        if not "main" in repo.heads:
            repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)

        # Compare local and remote hash
        if local_hash == remote_hash:
            await sdk.send(event.message, "<b>Already up to date.</b>")
            return

        # Pull changes
        origin.pull()

        # Update dependencies
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--user",
                    "-r",
                    os.path.join(const.ROOT_DIRECTORY, "requirements.txt"),
                ]
            )
        except:
            await sdk.send(event.message, "<b>Cannot update dependencies.</b>")
            return

        message = (
            await sdk.send(event.message, "<b>Update completed.\nRestarting...</b>")
        )[0]
        self.bot.storage.dict["start_message"] = {
            "entity": message.chat,
            "id": message.id,
            "text": "<b>Update completed!</b>",
        }
        self.restart()

    async def dlmod_cmd(self, event: sdk.Event, command: sdk.Command):
        if command.arg == "":
            await sdk.send(
                event.message, "<b>You need to specify module name or URL.</b>"
            )
            return

        url = (
            command.arg
            if (
                command.arg.startswith("http://") or command.arg.startswith("https://")
            )  # simple url checking
            else const.MODULES_URL.format(command.arg)
        )
        try:
            mod = self.bot.load_module_from_url(url)
        except Exception as ex:
            logger.exception('Cannot load module from "%s": %s', url, ex)
            if isinstance(ex, AlreadyLoaded):
                await sdk.send(event.message, "<b>This module is already loaded.</b>")
            else:
                await sdk.send(event.message, "<b>Cannot load module.</b>")
            return
        self.bot.storage.dict.setdefault("modules", []).append(url)
        await sdk.send(
            event.message, f'<b>Successfully loaded module "{mod.name}".</b>'
        )

    async def lsmod_cmd(self, event: sdk.Event, command: sdk.Command):
        modules = self.bot.storage.dict.get("modules", [])
        if len(modules) == 0:
            await sdk.send(event.message, "<b>There are no remote modules.</b>")
            return
        await sdk.send(
            event.message,
            "<b>Remote modules:</b>\n\n"
            + "\n".join(
                [
                    f"<b>• {ind+1}:</b> <code>{url}</code>"
                    for ind, url in enumerate(modules)
                ]
            ),
        )

    # TODO: maybe delete modules by url?
    async def rmmod_cmd(self, event: sdk.Event, command: sdk.Command):
        if command.arg == "":
            await sdk.send(event.message, "<b>You need to specify module index.</b>")
            return

        # idk how to do this
        modules, index = self.bot.storage.dict.get("modules", []), 0
        try:
            index = int(command.arg)
        except:
            pass
        if index < 1 or index > len(modules):
            await sdk.send(event.message, "<b>Invalid module index.</b>")
            return
        await sdk.send(
            event.message, f'<b>Deleted module "</b><code>{modules.pop(index-1)}</code><b>".</b>'
        )
