# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/cli/cli.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 488 bytes
import argparse, os, sys
from deephyper.core.cli import nas_init

def create_parser():
    parser = argparse.ArgumentParser(description='DeepHyper command line.')
    subparsers = parser.add_subparsers(help='Menus.')
    nas_init.add_subparser(subparsers)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        (args.func)(**vars(args))
    except AttributeError:
        parser.print_help()