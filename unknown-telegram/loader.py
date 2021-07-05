# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import importlib
import os
import tempfile
from urllib.parse import urlparse

import requests

from .logging import logger


class Module:
    """Base object of the module"""

    def __init__(self):
        self.name: str = "Unknown"
        self.storage: dict = {}


class Modules:
    """Storage for loaded modules"""

    def __init__(self):
        self.modules: list = []
        self.names: list = []
        self.commands: dict = {}
        self.incoming: list = []

    def register_module(self, mod: Module):
        """Register given module in the storage"""
        for func in [
            func
            for func in dir(mod)
            if callable(getattr(mod, func))
            and not func.startswith("__")
            and func.lower().endswith("_cmd")
        ]:
            cmd = func.lower()[:-4]
            if cmd not in self.commands:
                self.commands[cmd] = getattr(mod, func)
            else:
                logger.warning('Command "%s" is already registered', cmd)

        incoming = getattr(mod, "incoming", None)
        if callable(incoming):
            self.incoming.append(incoming)

        self.modules.append(mod)
        self.names.append(mod.__module__)

    def load_spec(self, path: str, name: str = "") -> importlib.machinery.ModuleSpec:
        """Load module spec from given path"""
        name = (
            __package__
            + ".modules."
            + ((os.path.basename(path)[:-3].lower()) if name == "" else name)
        )
        if name in self.names:
            raise Exception(f'Module name "{name}" is already used')
        return importlib.util.spec_from_file_location(
            name,
            path,
        )

    def load_module_from_spec(self, spec: importlib.machinery.ModuleSpec) -> Module:
        """Load module from given spec"""
        py_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(py_mod)

        mod = getattr(py_mod, "Module")
        if not issubclass(mod, Module):
            raise TypeError("Invalid module type")
        return mod()

    def load_module_from_url(self, url: str) -> Module:
        """Load module from given URL"""
        path = tempfile.mkstemp(prefix="unknown-telegram-", suffix=".py")[1]
        with open(path, "wb+") as file:
            file.write(requests.get(url).content)
        mod = self.load_module_from_spec(
            self.load_spec(
                path,
                name=os.path.splitext(os.path.basename(urlparse(url).path))[0].lower(),
            )
        )
        try:
            os.remove(path)
        except:
            # Cannot remove on windows ¯\_(ツ)_/¯
            pass
        return mod
