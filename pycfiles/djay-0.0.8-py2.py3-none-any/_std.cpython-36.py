# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/py/py/_std.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 631 bytes
import sys, warnings

class PyStdIsDeprecatedWarning(DeprecationWarning):
    pass


class Std(object):
    __doc__ = ' makes top-level python modules available as an attribute,\n        importing them on first access.\n    '

    def __init__(self):
        self.__dict__ = sys.modules

    def __getattr__(self, name):
        warnings.warn(('py.std is deprecated, plase import %s directly' % name), category=PyStdIsDeprecatedWarning)
        try:
            m = __import__(name)
        except ImportError:
            raise AttributeError('py.std: could not import %s' % name)

        return m


std = Std()