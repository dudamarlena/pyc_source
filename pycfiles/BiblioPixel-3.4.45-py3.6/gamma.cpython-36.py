# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/types/gamma.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 940 bytes
import functools, numbers
from ...colors import gamma
NAMES = [d for d in dir(gamma) if d.isupper()]
USAGE = "\nA Gamma table is represented by one of:\n\n* A number, representing a floating gamma correction value\n* A string, representing a name of a standard gamma function\n* A list of up to three elements: arguments to Gamma's constructor.\n* A dictionary representing arguments to Gamma's constructor.\n\nPossible string names  are " + ', '.join(NAMES)

@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(numbers.Number)
def _(c):
    return gamma.Gamma(c)


@make.register(str)
def _(c):
    if c not in NAMES:
        raise ValueError('Unknown gamma %s: valid names are %s' % (c, NAMES))
    return getattr(gamma, c)


@make.register(list)
@make.register(tuple)
def _(c):
    return (gamma.Gamma)(*c)


@make.register(dict)
def _(c):
    return (gamma.Gamma)(**c)