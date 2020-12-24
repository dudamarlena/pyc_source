# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/py/py/_std.py
# Compiled at: 2019-02-14 00:35:48
import sys, warnings

class PyStdIsDeprecatedWarning(DeprecationWarning):
    pass


class Std(object):
    """ makes top-level python modules available as an attribute,
        importing them on first access.
    """

    def __init__(self):
        self.__dict__ = sys.modules

    def __getattr__(self, name):
        warnings.warn('py.std is deprecated, plase import %s directly' % name, category=PyStdIsDeprecatedWarning)
        try:
            m = __import__(name)
        except ImportError:
            raise AttributeError('py.std: could not import %s' % name)

        return m


std = Std()