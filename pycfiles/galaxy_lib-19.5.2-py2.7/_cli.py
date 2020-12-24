# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/mulled/_cli.py
# Compiled at: 2018-04-20 03:19:42
"""CLI helpers for mulled command-line tools."""
import argparse

def arg_parser(argv, globals):
    """Build an argparser for this CLI tool."""
    doc = globals['__doc__']
    description, epilog = doc.split('\n', 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    return parser


__all__ = ('arg_parser', )