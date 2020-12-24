# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martijn/.virtualenvs/zeekoers/lib/python3.7/site-packages/zeekoers/cli.py
# Compiled at: 2020-03-23 07:00:50
# Size of source mod 2**32: 917 bytes
"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mzeekoers` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``zeekoers.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``zeekoers.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('names', metavar='NAME', nargs=(argparse.ZERO_OR_MORE), help='A name of something.')

def main(args=None):
    args = parser.parse_args(args=args)
    print(args.names)