# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/nautilus/nautiluszim/constants.py
# Compiled at: 2020-05-05 11:49:35
# Size of source mod 2**32: 662 bytes
import pathlib, logging
import zimscraperlib.logging as lib_getLogger
ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name
with open(ROOT_DIR.joinpath('VERSION'), 'r') as (fh):
    VERSION = fh.read().strip()
SCRAPER = f"{NAME} {VERSION}"

class Global:
    debug = False


def setDebug(debug):
    """ toggle constants global DEBUG flag (used by getLogger) """
    Global.debug = bool(debug)


def getLogger():
    """ configured logger respecting DEBUG flag """
    return lib_getLogger(NAME, level=(logging.DEBUG if Global.debug else logging.INFO))