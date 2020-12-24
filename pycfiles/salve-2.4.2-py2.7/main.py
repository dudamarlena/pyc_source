# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/cli/main.py
# Compiled at: 2015-11-06 23:45:35
import sys
from .parser import load_args

def run():
    """
    Reads the commandline with a SALVE argument parser, and runs the function
    designated by the arguments.
    """
    args = load_args()
    args.func(args)


def main():
    if sys.version_info < (2, 6):
        sys.exit('Python Version Too Old! SALVE Requires Python >= 2.6')
    run()