# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/TuIndexer.py
# Compiled at: 2017-10-03 13:07:16
"""Provides a means of linking to a translation unit to HTML.
"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip import ExceptionCpip
from cpip.util import OaS

class ExceptionTuIndexer(ExceptionCpip):
    """Exception when handling PpLexer object."""
    pass


class TuIndexer(object):
    """Provides a means of indexing into a TU html file."""

    def __init__(self, tuFileName):
        self._tuName = tuFileName
        self._tuMarkerS = []

    def __str__(self):
        if len(self._tuMarkerS) == 0:
            return 'TuIndexer for "%s", no values' % self._tuName
        return 'TuIndexer for "%s". number of values=%d from %d to %d' % (
         self._tuName, len(self._tuMarkerS), self._tuMarkerS[0], self._tuMarkerS[(-1)])

    def add(self, theTuIndex):
        """Adds an integer index to the list of markers, returns the href name."""
        if len(self._tuMarkerS) > 0 and theTuIndex < self._tuMarkerS[(-1)]:
            raise ExceptionTuIndexer('Out of sequence: %s' % theTuIndex)
        self._tuMarkerS.append(theTuIndex)
        return '_%d' % theTuIndex

    def href(self, theTuIndex, isLB):
        """Returns an href string for the TuIndex. If isLB is true returns
        the nearest lower bound, otherwise the nearest upper bound."""
        if isLB:
            myIdx = OaS.indexLB(self._tuMarkerS, theTuIndex)
        else:
            myIdx = OaS.indexUB(self._tuMarkerS, theTuIndex)
        if myIdx >= len(self._tuMarkerS):
            raise ExceptionTuIndexer('Over-range index, isLB=%s: %s' % (isLB, theTuIndex))
        if myIdx == -1:
            raise ExceptionTuIndexer('Under-range index, isLB=%s: %s' % (isLB, theTuIndex))
        return '%s#_%d' % (self._tuName, self._tuMarkerS[myIdx])