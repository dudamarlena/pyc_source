# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/tests/fixtures.py
# Compiled at: 2008-12-19 12:41:15
from testfixtures import Comparison

class Identity:

    def __repr__(self):
        return '<identity>'


identity = Identity()

def check(callable, arg, expected, errors):
    try:
        actual = callable(arg)
    except Exception, ex:
        actual = Comparison(ex)

    base = 'Expected %r of %r %%s %r, but was %r' % (
     callable, arg, expected, actual)
    if expected is identity:
        if actual is not arg:
            errors.append(base % 'to be')
    elif actual != expected:
        errors.append(base % 'equal to')