# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="unknown-telegram.log", mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("unknown-telegram")
