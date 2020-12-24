# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/MatrixRep.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Makes replacements in a list of lines.'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import cpip

class ExceptionMatrixRep(cpip.ExceptionCpip):
    """Simple specialisation of an exception class for MatrixRep."""


class MatrixRep(object):
    """Makes replacements in a list of lines."""

    def __init__(self):
        """Constructor."""
        self._ir = {}

    def addLineColRep(self, l, c, was, now):
        """Adds to the IR. No test is made to see if there is an existing
        or pre-existing conflicting entry or if a sequence of entries makes
        sense.
        It is expected that callers call this in line/column order of the
        original matrix. If not the results of a subsequent call to
        sideEffect() are undefined. 
        """
        try:
            self._ir[l][c] = (
             len(was), now)
        except KeyError:
            self._ir[l] = {}
            self._ir[l][c] = (
             len(was), now)

    def sideEffect(self, theMat):
        """Makes the replacement, if line/col is out of range and
        ExceptionMatrixRep will be raised and the state of theMat argument
        is undefined."""
        for l in self._ir:
            if l >= len(theMat):
                raise ExceptionMatrixRep('Line index %d is out of range (max %d).' % (
                 l, len(theMat) - 1))
            colInc = 0
            colS = sorted(self._ir[l].keys())
            for c in colS:
                if c + colInc >= len(theMat[l]):
                    raise ExceptionMatrixRep('Col index %d is out of range (max %d).' % (
                     c + colInc, len(theMat[l]) - 1))
                x, r = self._ir[l][c]
                myLine = theMat[l]
                theMat[l] = myLine[:c + colInc] + r + myLine[c + colInc + x:]
                colInc += len(r) - x