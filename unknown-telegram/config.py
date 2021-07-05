# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import json

from . import const


class Config:
    """Stores Telegram application data"""

    def __init__(self):
        self.id: int = const.APP_ID
        self.hash: str = const.APP_HASH
        self.app_version: str = const.APP_VERSION
        self.device_model: str = const.APP_DEVICE_MODEL
        self.system_version: str = const.APP_SYSTEM_VERSION

    def load(self, filename: str):
        """Load config from given filename"""
        with open(filename, "r") as file:
            obj = json.load(file)

            self.id = obj["id"]
            self.hash = obj["hash"]
            self.app_version = obj["app_version"]
            self.device_model = obj["device_model"]
            self.system_version = obj["system_version"]

    def save(self, filename: str):
        """Save config to given filename"""
        with open(filename, "w") as file:
            json.dump(self.__dict__, file, indent=4)
