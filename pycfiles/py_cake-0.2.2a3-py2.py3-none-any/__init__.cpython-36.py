# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\pycake\src\pycake\__init__.py
# Compiled at: 2018-11-08 05:45:53
# Size of source mod 2**32: 175 bytes
from .meta import __version__
from .cli import cli
if __name__ == '__main__':
    cli()