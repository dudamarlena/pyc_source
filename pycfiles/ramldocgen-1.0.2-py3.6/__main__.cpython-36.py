# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ramldocgen\__main__.py
# Compiled at: 2017-06-28 07:33:00
# Size of source mod 2**32: 136 bytes
import sys
from .ramldocgen import cli

def main():
    sys.argv[0] = 'ramldocgen'
    cli.main()


if __name__ == '__main__':
    main()