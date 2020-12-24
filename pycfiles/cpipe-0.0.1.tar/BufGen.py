# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/BufGen.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'A generator class with a buffer. This allows multiple inspections of the\nstream issued by a generator. For example this is used by MaxMunchGen.'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import types
from cpip import ExceptionCpip

class ExceptionBufGen(ExceptionCpip):
    """Exception specialisation for BufGen."""


class BufGen(object):
    """A generator class with a buffer."""

    def __init__(self, theGen):
        """Constructor with a generator as and argument."""
        self._gen = theGen
        self._buf = []

    def __str__(self):
        return 'BufGen: %s' % self._buf

    def _extendBuffer(self, idx):
        if idx < 0:
            raise IndexError('BufGen index out of range')
        try:
            while len(self._buf) <= idx:
                self._buf.append(next(self._gen))

        except StopIteration:
            raise IndexError('BufGen index out of range')

    def __getitem__(self, key):
        """Implements indexing and slicing. Negative indexes will raise an
        IndexError."""
        idx = key
        if isinstance(key, slice):
            idx = key.stop - 1
        if idx < 0:
            raise IndexError('BufGen can not handle negative indexes.')
        try:
            while len(self._buf) <= idx:
                self._buf.append(next(self._gen))

        except StopIteration:
            raise IndexError('BufGen index out of range')

        return self._buf[key]

    @property
    def lenBuf(self):
        """Returns the length of the existing buffer. NOTE: This may not be the
        final length as the generator might not be exhausted just yet."""
        return len(self._buf)

    def gen(self):
        """Yield objects from the generator via the buffer."""
        i = 0
        while 1:
            if len(self._buf) <= i:
                self._buf.append(next(self._gen))
            yield self._buf[i]
            i += 1

    def slice(self, sliceLen):
        """Returns a buffer slice of length sliceLen."""
        if sliceLen > len(self._buf):
            raise ExceptionBufGen('slice length %d > buffer size of %d' % (
             sliceLen, len(self._buf)))
        if sliceLen == 1:
            return [self._buf.pop(0)]
        retList = []
        i = 0
        while i < sliceLen:
            retList.append(self._buf.pop(0))
            i += 1

        return retList

    def replace(self, theIdx, theLen, theValueS):
        """Replaces within the buffer starting at theIdx removing theLen objects
        and replacing them with theValueS."""
        myIdxEnd = theIdx + theLen
        if theIdx >= self.lenBuf:
            raise ExceptionBufGen('replace start index %d >= buffer size of %d' % (
             theIdx, len(self._buf)))
        if myIdxEnd > self.lenBuf:
            raise ExceptionBufGen('replace end index %d > buffer size of %d' % (
             myIdxEnd, len(self._buf)))
        if theIdx < 0:
            raise ExceptionBufGen('negative index %d' % theIdx)
        if myIdxEnd < 0:
            raise ExceptionBufGen('negative index+length %d' % myIdxEnd)
        self._buf[theIdx:myIdxEnd] = theValueS