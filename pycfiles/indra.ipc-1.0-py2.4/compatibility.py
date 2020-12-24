# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/ipc/compatibility.py
# Compiled at: 2008-07-28 17:15:44
"""@file compatibility.py
@brief Classes that manage compatibility states.

$LicenseInfo:firstyear=2007&license=mit$

Copyright (c) 2007-2008, Linden Research, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
$/LicenseInfo$
"""

class _Compatibility(object):
    __module__ = __name__

    def __init__(self, reason):
        self.reasons = []
        if reason:
            self.reasons.append(reason)

    def combine(self, other):
        if self._level() <= other._level():
            return self._buildclone(other)
        else:
            return other._buildclone(self)

    def prefix(self, leadin):
        self.reasons = [ leadin + r for r in self.reasons ]

    def same(self):
        return self._level() >= 1

    def deployable(self):
        return self._level() > 0

    def resolved(self):
        return self._level() > -1

    def compatible(self):
        return self._level() > -2

    def explain(self):
        return self.__class__.__name__ + '\n' + ('\n').join(self.reasons) + '\n'

    def _buildclone(self, other=None):
        c = self._buildinstance()
        c.reasons = self.reasons
        if other:
            c.reasons = c.reasons + other.reasons
        return c

    def _buildinstance(self):
        return self.__class__(None)


class Incompatible(_Compatibility):
    __module__ = __name__

    def _level(self):
        return -2


class Mixed(_Compatibility):
    __module__ = __name__

    def __init__(self, *inputs):
        _Compatibility.__init__(self, None)
        for i in inputs:
            self.reasons += i.reasons

        return

    def _buildinstance(self):
        return self.__class__()

    def _level(self):
        return -1


class _Aged(_Compatibility):
    __module__ = __name__

    def combine(self, other):
        if self._level() == other._level():
            return self._buildclone(other)
        if int(self._level()) == int(other._level()):
            return Mixed(self, other)
        return _Compatibility.combine(self, other)


class Older(_Aged):
    __module__ = __name__

    def _level(self):
        return -0.25


class Newer(_Aged):
    __module__ = __name__

    def _level(self):
        return 0.25


class Same(_Compatibility):
    __module__ = __name__

    def __init__(self):
        _Compatibility.__init__(self, None)
        return

    def _buildinstance(self):
        return self.__class__()

    def _level(self):
        return 1