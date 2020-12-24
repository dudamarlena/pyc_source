# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/periodnumber.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
__all__ = ['genPNclass']

def genPNclass(llimit, ulimit):
    assert llimit < ulimit

    class Periodnumber:
        __module__ = __name__

        def __init__(self, data):
            gap = ulimit - llimit
            self.data = (data - llimit) % gap + llimit

        def __float__(self):
            return self.data

        def __str__(self):
            return str(self.data)

        def __repr__(self):
            return '%s(%s)' % (self.__class__.__name__, repr(self.data))

        def __add__(self, other):
            return self.__class__(self.data + float(other))

        def __sub__(self, other):
            return self.__class__(self.data - float(other))

        def __neg__(self):
            return self.__class__(-self.data)

        def __abs__(self):
            return abs(self.data)

    return Periodnumber