# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/darpy/common.py
# Compiled at: 2017-11-03 16:11:21
from __future__ import print_function
import argparse, os, sys
from darpy.version import __version__

def darpy_run(cmd):
    print(cmd, file=sys.stderr)
    os.system(cmd)


def make_parser():

    class SharedParser(argparse.ArgumentParser):

        def __init__(self, func=None, *args, **kwargs):
            argparse.ArgumentParser.__init__(self, *args, **kwargs)
            self.set_defaults(func=func)
            self.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    parser = SharedParser(description='darpy')
    subparsers = parser.add_subparsers(title='Subcommands', parser_class=SharedParser, metavar='')
    return (
     parser, subparsers)