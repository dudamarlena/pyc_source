# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/cli/cli.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 689 bytes
import argparse, os, sys
from deephyper.core.cli import hps_init, hps, nas_init, nas

def create_parser():
    parser = argparse.ArgumentParser(description='DeepHyper command line.')
    subparsers = parser.add_subparsers()
    nas_init.add_subparser(subparsers)
    nas.add_subparser(subparsers)
    hps_init.add_subparser(subparsers)
    hps.add_subparser(subparsers)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    (args.func)(**vars(args))