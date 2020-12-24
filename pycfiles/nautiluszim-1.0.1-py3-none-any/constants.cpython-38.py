# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/nautilus/nautiluszim/constants.py
# Compiled at: 2020-02-04 07:22:26
# Size of source mod 2**32: 382 bytes
import pathlib, logging
from zimscraperlib.logging import getLogger
ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name
with open(ROOT_DIR.joinpath('VERSION'), 'r') as (fh):
    VERSION = fh.read().strip()
SCRAPER = f"{NAME} {VERSION}"
logger = getLogger(NAME, level=(logging.DEBUG))