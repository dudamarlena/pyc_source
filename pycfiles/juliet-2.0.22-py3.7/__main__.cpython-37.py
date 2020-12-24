# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/juliet/__main__.py
# Compiled at: 2019-10-01 14:49:21
# Size of source mod 2**32: 326 bytes
import sys

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    print('juliet command mode is under development. In the meantime, use the juliet.py script.')


if __name__ == '__main__':
    main()