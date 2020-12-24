# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/types/direction.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 771 bytes
import functools
NAMES = {'up':(0, -1), 
 'down':(0, 1), 
 'left':(-1, 0), 
 'right':(1, 0)}

@functools.singledispatch
def make(c):
    raise ValueError(ERROR % c)


@make.register(str)
def _(c):
    items = [v for k, v in NAMES.items() if k.startswith(c)]
    if len(items) != 1:
        raise ValueError(ERROR % c)
    return items[0]


@make.register(tuple)
def _(c):
    if c not in NAMES.values():
        raise ValueError(ERROR % (c,))
    return c


@make.register(list)
def _(c):
    return make(tuple(c))


USAGE = "Direction values can be\n* a string 'up', 'down', 'left', 'right', or\n* a string prefix like 'u' or 'ri'\n* one of four numeric pairs (0, -1), (0, 1), (-1, 0), (1, 0).\n"
ERROR = 'Don\'t understand direction "%s"\n' + USAGE