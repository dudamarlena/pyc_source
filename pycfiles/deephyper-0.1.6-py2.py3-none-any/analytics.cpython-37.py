# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/logs/analytics.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1066 bytes
import argparse, os, sys
from deephyper.core.logs import json, parsing
from deephyper.core.plot import hps, multi, post_train, single

def create_parser():
    parser = argparse.ArgumentParser(description='Run some analytics for deephyper.')
    subparsers = parser.add_subparsers(help='Kind of analytics.')
    mapping = dict()
    name, func = parsing.add_subparser(subparsers)
    mapping[name] = func
    name, func = json.add_subparser(subparsers)
    mapping[name] = func
    name, func = single.add_subparser(subparsers)
    mapping[name] = func
    name, func = multi.add_subparser(subparsers)
    mapping[name] = func
    name, func = post_train.add_subparser(subparsers)
    mapping[name] = func
    name, func = hps.add_subparser(subparsers)
    mapping[name] = func
    return (
     parser, mapping)


def main():
    parser, mapping = create_parser()
    args = parser.parse_args()
    (mapping[sys.argv[1]])(**vars(args))