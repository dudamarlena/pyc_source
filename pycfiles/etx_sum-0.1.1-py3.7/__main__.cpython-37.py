# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etx/__main__.py
# Compiled at: 2020-04-08 09:02:42
# Size of source mod 2**32: 530 bytes
import sys, argparse
from .summeriser import Summary

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='ext-sum.py is intended to be a small utillity script that gives a few greate stats on your daytrading results')
    parser.add_argument('file', metavar='f', nargs=1, help='path to your ETX capital histroy csv file')
    args = parser.parse_args()
    sum = Summary(args.filePath)
    sum.summarize()


if __name__ == '__main__':
    main()