# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import pickle


class Storage:
    """Stores modules data"""

    def __init__(self, path: str):
        self.path = path
        self.dict: dict = {}
        self.checksum: str = ""
        try:
            with open(self.path, "rb") as file:
                self.dict = pickle.load(file)
        except:
            pass

    def sync(self):
        """Sync storage data with file"""
        data = pickle.dumps(self.dict)
        checksum = hash(data)
        if checksum != self.checksum:
            with open(self.path, "wb+") as file:
                file.write(data)
            self.checksum = checksum
