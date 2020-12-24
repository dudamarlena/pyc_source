# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/wstools/UserTuple.py
# Compiled at: 2006-10-25 20:34:29
"""
A more or less complete user-defined wrapper around tuple objects.
Adapted version of the standard library's UserList.

Taken from Stefan Schwarzer's ftputil library, available at
<http://www.ndh.net/home/sschwarzer/python/python_software.html>, and used under this license:

Copyright (C) 1999, Stefan Schwarzer 
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

- Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

- Neither the name of the above author nor the names of the
  contributors to the software may be used to endorse or promote
  products derived from this software without specific prior written
  permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

class UserTuple:

    def __init__(self, inittuple=None):
        self.data = ()
        if inittuple is not None:
            if type(inittuple) == type(self.data):
                self.data = inittuple
            elif isinstance(inittuple, UserTuple):
                self.data = inittuple.data[:]
            else:
                self.data = tuple(inittuple)
        return

    def __repr__(self):
        return repr(self.data)

    def __lt__(self, other):
        return self.data < self.__cast(other)

    def __le__(self, other):
        return self.data <= self.__cast(other)

    def __eq__(self, other):
        return self.data == self.__cast(other)

    def __ne__(self, other):
        return self.data != self.__cast(other)

    def __gt__(self, other):
        return self.data > self.__cast(other)

    def __ge__(self, other):
        return self.data >= self.__cast(other)

    def __cast(self, other):
        if isinstance(other, UserTuple):
            return other.data
        else:
            return other

    def __cmp__(self, other):
        return cmp(self.data, self.__cast(other))

    def __contains__(self, item):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __getslice__(self, i, j):
        i = max(i, 0)
        j = max(j, 0)
        return self.__class__(self.data[i:j])

    def __add__(self, other):
        if isinstance(other, UserTuple):
            return self.__class__(self.data + other.data)
        else:
            if isinstance(other, type(self.data)):
                return self.__class__(self.data + other)
            return self.__class__(self.data + tuple(other))

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__