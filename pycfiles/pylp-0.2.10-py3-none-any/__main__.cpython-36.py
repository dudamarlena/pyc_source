# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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