# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/bt/ctdt6vrj33n8yhzhpvyfy53h0000gn/T/pip-unpacked-wheel-a7yo76wc/zimscraperlib/constants.py
# Compiled at: 2020-05-05 04:38:33
# Size of source mod 2**32: 293 bytes
import pathlib
ROOT_DIR = pathlib.Path(__file__).parent
NAME = pathlib.Path(__file__).parent.name
with open(ROOT_DIR.joinpath('VERSION'), 'r') as (fh):
    VERSION = fh.read().strip()
SCRAPER = f"{NAME} {VERSION}"