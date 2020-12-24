# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pylox/__main__.py
# Compiled at: 2017-01-19 18:44:41
# Size of source mod 2**32: 493 bytes
import sys, argparse
from . import Lox

def get_args():
    parser = argparse.ArgumentParser(description='PyLox')
    parser.add_argument('script',
      type=str, nargs='?', help='script file name')
    return parser.parse_args()


def main():
    args = get_args()
    lox = Lox()
    if args.script:
        lox.run_file(args.script)
    else:
        lox.run_prompt()
    return lox.error_code()


if __name__ == '__main__':
    sys.exit(main())