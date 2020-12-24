# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/scheme.py
# Compiled at: 2018-10-29 10:17:46
# Size of source mod 2**32: 947 bytes
from __future__ import unicode_literals
from .compat import str, py2

class Scheme(object):
    __slots__ = ('name', )
    slashed = False

    def __init__(self, name):
        self.name = str(name).strip().lower()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, self.__class__):
            return self is other

    def __hash__(self):
        return hash(self.name)

    def __neq__(self, other):
        return not self == other

    def __bytes__(self):
        return self.name.encode('ascii')

    def __str__(self):
        return self.name

    if py2:
        __unicode__ = __str__
        __str__ = __bytes__
        del __str__

    def is_relative(self, uri):
        return False


class URLScheme(Scheme):
    slashed = True

    def is_relative(self, uri):
        return not uri._host or not uri._path.is_absolute()