# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fragmap\debug.py
# Compiled at: 2019-09-05 13:55:36
# Size of source mod 2**32: 1524 bytes
import argparse, sys, logging
_logging_categories = [
 'grid', 'sorting', 'grouping', 'parser', 'update', 'console', 'test', 'matrix']
_enable_logging = {category:False for category in _logging_categories}
logging.basicConfig()
for cat in _logging_categories:
    l = logging.getLogger(cat)
    l.setLevel(logging.CRITICAL)

def is_logging(category):
    return _enable_logging[category]


def enable_logging(category):
    if category in _logging_categories:
        get(category).setLevel(logging.DEBUG)
        _enable_logging[category] = True
    else:
        print("WARNING: Unknown logging category '{}'".format(category))


def get(category):
    return logging.getLogger(category)


def parse_args(extendable=False):
    p = argparse.ArgumentParser(add_help=(not extendable))
    p.add_argument('--log', nargs='+', choices=([
     'all'] + _logging_categories),
      metavar='CATEGORY',
      help='Which categories of log messages to send to standard output: %(choices)s')
    args, unknown_args = p.parse_known_args()
    if args.log:
        if args.log[0] == 'all':
            args.log = _logging_categories
        for cat in args.log:
            if cat == 'all':
                pass
            else:
                enable_logging(cat)

    sys.argv[1:] = unknown_args
    if extendable:
        return p