# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/tools/trivial.py
# Compiled at: 2014-09-06 21:58:19
"""Tools so trivial that tracebacks should not descend into them

We define the ``__unittest`` symbol in their module namespace so unittest will
skip them when printing tracebacks, just as it does for their corresponding
methods in ``unittest`` proper.

"""
import re, unittest
__all__ = [
 'ok_', 'eq_']
__unittest = 1

def ok_(expr, msg=None):
    """Shorthand for assert. Saves 3 whole characters!
    """
    assert expr, msg


def eq_(a, b, msg=None):
    """Shorthand for 'assert a == b, "%r != %r" % (a, b)
    """
    assert a == b, msg or '%r != %r' % (a, b)


caps = re.compile('([A-Z])')

def pep8(name):
    return caps.sub(lambda m: '_' + m.groups()[0].lower(), name)


class Dummy(unittest.TestCase):

    def nop():
        pass


_t = Dummy('nop')
for at in [ at for at in dir(_t) if at.startswith('assert') and '_' not in at
          ]:
    pepd = pep8(at)
    vars()[pepd] = getattr(_t, at)
    __all__.append(pepd)

del Dummy
del _t
del pep8