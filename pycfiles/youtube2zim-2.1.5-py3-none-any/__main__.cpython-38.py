# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: youtube2zim/__main__.py
# Compiled at: 2019-11-23 13:39:11
# Size of source mod 2**32: 368 bytes
import sys, pathlib

def main():
    sys.path = [
     str(pathlib.Path(__file__).parent.parent.resolve())] + sys.path
    import youtube2zim.entrypoint as entry
    entry()


if __name__ == '__main__':
    main()