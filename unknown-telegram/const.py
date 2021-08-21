# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import os
import sys

# DO NOT EDIT THESE VALUES!!
APP_ID = 10840
APP_HASH = "33c45224029d59cb3ad0c16134215aeb"
APP_VERSION = "7.9.2"
APP_DEVICE_MODEL = "iPhone XS"
APP_SYSTEM_VERSION = "14.4.1"
MODULES_FOLDER = "modules"
MODULES_URL = "https://raw.githubusercontent.com/unknown-telegram/modules/main/{}.py"
MODULES_DEFAULT = ["dump", "suspension", "afk", "sysinfo", "terminal", "ping"]
CONFIG_FILE = "unknown-telegram.json"
MESSAGE_ERROR = "<b>An error occurred while executing the module.</b>"
MESSAGE_SENDING_MEDIA = "<b>Sending media...</b>"
GIT_URL = "https://github.com/unknown-telegram/unknown-telegram.git"
ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lol
IS_DOCKER = ("-docker" in sys.argv)
DATA_FOLDER = ("data" if not IS_DOCKER else "/data")
