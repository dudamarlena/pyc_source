# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/main/args.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 365 bytes
import argparse
from ..util import deprecated, log
ARGS = None

def set_args(description, argv, *argument_addders):
    global ARGS
    parser = argparse.ArgumentParser(description=description)
    for adder in (deprecated, log) + argument_addders:
        adder.add_arguments(parser)

    ARGS = parser.parse_args(argv)
    log.apply_args(ARGS)
    return ARGS