# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/envs/nautilus/lib/python3.8/site-packages/zimscraperlib/constants.py
# Compiled at: 2020-04-20 14:04:33
# Size of source mod 2**32: 293 bytes
import pathlib
ROOT_DIR = pathlib.Path(__file__).parent
NAME = pathlib.Path(__file__).parent.name
with open(ROOT_DIR.joinpath('VERSION'), 'r') as (fh):
    VERSION = fh.read().strip()
SCRAPER = f"{NAME} {VERSION}"