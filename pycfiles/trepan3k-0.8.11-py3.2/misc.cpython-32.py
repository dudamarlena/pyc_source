# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/misc.py
# Compiled at: 2015-04-06 04:22:56


def option_set(options, value, default_options):
    if not options or value not in options:
        return default_options.get(value)
    else:
        return options.get(value)
        return


def bool2YN(b):
    if b:
        return 'Y'
    else:
        return 'N'


def wrapped_lines(msg_part1, msg_part2, width):
    if len(msg_part1) + len(msg_part2) + 1 > width:
        return msg_part1 + '\n\t' + msg_part2
    else:
        return msg_part1 + ' ' + msg_part2


import os
from glob import glob

def pyfiles(callername, level=2):
    """All python files caller's dir without the path and trailing .py"""
    d = os.path.dirname(callername)
    glob(os.path.join(d, '[a-zA-Z]*.py'))
    py_files = glob(os.path.join(d, '[a-zA-Z]*.py'))
    return [os.path.basename(filename[0:-3]) for filename in py_files]


if __name__ == '__main__':
    TEST_OPTS = {'a': True,  'b': 5,  'c': None}
    get_option = lambda key: option_set(opts, key, TEST_OPTS)
    opts = {'d': 6,  'a': False}
    for opt in ['a', 'b', 'c', 'd']:
        print(opt, get_option(opt))

    for b in [True, False]:
        print(bool2YN(b))

    print(wrapped_lines('hi', 'there', 80))
    print(wrapped_lines('hi', 'there', 5))
    print(pyfiles(__file__))