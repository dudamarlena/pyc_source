# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/instatrace/control.py
# Compiled at: 2010-05-17 21:22:05
import argparse, logging, sys
from . import commands
parser = argparse.ArgumentParser(description='Instatrace control')
parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
subparsers = parser.add_subparsers(title='Commands')
commands.ExtractCommand.add_subparser(subparsers)
commands.HistogramsCommand.add_subparser(subparsers)

def main():
    args = parser.parse_args()
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logging.root.addHandler(console)
    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)
    try:
        args.run(args)
    except KeyboardInterrupt:
        print
        sys.exit(1)


if __name__ == '__main__':
    main()