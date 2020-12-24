# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cufrancis/Develop/pelicantool/.env/lib/python3.6/site-packages/pelicantool/__main__.py
# Compiled at: 2018-01-12 03:23:11
# Size of source mod 2**32: 253 bytes
from .parser import ParserFactory
from .exceptions import ActionNotFound
import sys

def main():
    parser = ParserFactory.factory(sys.argv[1:])
    action = parser.instance()
    if action:
        action.run()
    else:
        raise ActionNotFound