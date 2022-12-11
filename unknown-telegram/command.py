# -*- coding: utf-8 -*-
# Coded by @altfoxie with power of Senko!

import re


class Command:
    """Parses text into command"""

    def __init__(self, text: str):
        self.text = ""
        self.arg = ""
        self.args = []
        if text.startswith("."):
            self.text = text[1:]

            parts = re.split(r"\s", self.text, 1)
            self.cmd = parts[0].lower()
            if len(parts) > 1:
                self.arg = parts[1]
                self.args = self.arg.split(" ")


# pasted from v1 lol
