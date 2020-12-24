# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/__main__.py
# Compiled at: 2018-08-21 11:41:53
# Size of source mod 2**32: 462 bytes
"""llb3d - LLVM Blitz3d implementation."""
import argparse
from . import __version__

def main():
    """Execute, when user call llb3d."""
    parser = argparse.ArgumentParser(description=('llb3d ' + __version__))
    parser.add_subparsers(title='commands', help='commands for compiler')
    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
    else:
        args.func(args)