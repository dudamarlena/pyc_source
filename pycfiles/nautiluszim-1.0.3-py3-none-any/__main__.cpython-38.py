# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: nautiluszim/__main__.py
# Compiled at: 2020-01-30 08:35:05
# Size of source mod 2**32: 365 bytes
import sys, pathlib

def main():
    sys.path = [
     str(pathlib.Path(__file__).parent.parent.resolve())] + sys.path
    import nautiluszim.entrypoint as entry
    entry()


if __name__ == '__main__':
    main()