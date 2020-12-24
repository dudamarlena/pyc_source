# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/helper/config.py
# Compiled at: 2012-07-04 07:16:58
from mole.helper import AttrDict
try:
    from ConfigParser import RawConfigParser as cp
    from ConfigParser import NoSectionError
except ImportError:
    from configparser import RawConfigParser as cp
    from configparser import NoSectionError

class MoleConfig(object):

    def __init__(self, f=None):
        self._values = cp()
        if f:
            self._values.read(f)

    def sections(self):
        return self._values.sections()

    def read(self, f):
        self._values.read(f)

    def __getattr__(self, item):
        if self._values.has_section(item):
            return AttrDict(self._values.items(item))
        else:
            return
            return

    def __iter__(self):
        for x in self._values.sections():
            yield (
             x, AttrDict(self._values.items(x)))

    def items(self, section):
        return self._values.items(section)

    def __repr__(self):
        return repr(dict([ x for x in self ]))