# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/cnv_definition_collection.py
# Compiled at: 2008-12-08 17:00:29
from __future__ import division
import fileinput, sys
from mpgutils import utils

class CNVDefinition(object):

    def __init__(self, strCNVName, strChrName, iStartPosn, iEndPosn):
        self.strCNVName = strCNVName
        self.strChrName = strChrName
        self.iStartPosn = iStartPosn
        self.iEndPosn = iEndPosn

    def __str__(self):
        return self.strCNVName + ' chr' + self.strChrName + ' ' + str(self.iStartPosn) + ':' + str(self.iEndPosn)

    def length(self):
        return self.iEndPosn - self.iStartPosn + 1


def _cmpCNVDefinitionByStart(cnv1, cnv2):
    return cmp(cnv1.iStartPosn, cnv2.iStartPosn)


def _cmpCNVDefinitionByEnd(cnv1, cnv2):
    return cmp(cnv1.iEndPosn, cnv2.iEndPosn)


def _findCNVCandidatesUsingStartPosn(lstCNV, iStartPosn):
    """lstCNV is ordered by start posn.  Return index if the first
    CNV definition that has start posn > iStartPosn."""
    lo = 0
    hi = len(lstCNV)
    while lo < hi:
        mid = (lo + hi) // 2
        if iStartPosn < lstCNV[mid].iStartPosn:
            hi = mid
        else:
            lo = mid + 1

    return lo


def _findCNVCandidatesUsingEndPosn(lstCNV, iEndPosn):
    """lstCNV is ordered by end posn.  Return index if the first
    CNV definition that has end posn >= iEndPosn."""
    lo = 0
    hi = len(lstCNV)
    while lo < hi:
        mid = (lo + hi) // 2
        if lstCNV[mid].iEndPosn < iEndPosn:
            lo = mid + 1
        else:
            hi = mid

    return lo


class CNVDefinitionCollection(object):

    def __init__(self, strCNVDefsPath):
        self._dctCNVs = {}
        self._fIn = fileinput.FileInput([strCNVDefsPath])
        self._strLine = self._fIn.readline().rstrip('\n')
        lstHeaders = self._strLine.split()
        if lstHeaders != ['cnp_id', 'chr', 'start', 'end']:
            self._reportError('Unexpected header line in CNV definition file')
        for self._strLine in self._fIn:
            self._strLine = self._strLine.rstrip('\n')
            lstFields = self._strLine.split()
            if len(lstFields) < 4:
                self._reportError('Not enough fields in CNV definition file')
            for i in [1, 2, 3]:
                if not lstFields[i].isdigit():
                    self._reportError('Non-numeric value in column ' + str(i))

            if lstFields[0] in self._dctCNVs:
                self._reportError('CNV defined more than once')
            self._dctCNVs[lstFields[0]] = CNVDefinition(lstFields[0], lstFields[1], int(lstFields[2]), int(lstFields[3]))

        self._fIn.close()
        del self._fIn
        del self._strLine
        dctCNVsByChromosome = {}
        for cnv in self._dctCNVs.values():
            try:
                dctCNVsByChromosome[cnv.strChrName].append(cnv)
            except KeyError:
                dctCNVsByChromosome[cnv.strChrName] = [
                 cnv]

        self._dctCNVStartAndEndListsByChromosome = {}
        for (strChr, lstCNVs) in dctCNVsByChromosome.iteritems():
            lstCNVs.sort(_cmpCNVDefinitionByStart)
            lstCNVsSortedByEnd = lstCNVs[:]
            lstCNVsSortedByEnd.sort(_cmpCNVDefinitionByEnd)
            self._dctCNVStartAndEndListsByChromosome[strChr] = (lstCNVs, lstCNVsSortedByEnd)

    def getCNVsForLocus(self, strChr, iPosn):
        """Return set of CNVs that contain the given locus"""
        (lstOrderedByStart, lstOrderedByEnd) = self._dctCNVStartAndEndListsByChromosome[strChr]
        stCandidatesByStartPosn = set(lstOrderedByStart[:_findCNVCandidatesUsingStartPosn(lstOrderedByStart, iPosn)])
        stCandidatesByEndPosn = set(lstOrderedByEnd[_findCNVCandidatesUsingEndPosn(lstOrderedByEnd, iPosn):])
        return stCandidatesByStartPosn & stCandidatesByEndPosn

    def getCNV(self, strCNV):
        if strCNV not in self._dctCNVs:
            return
        return self._dctCNVs[strCNV]

    def _reportError(self, strErrorMessage):
        utils.raiseExceptionWithFileInput(self._fIn, 'CNV definition file', strErrorMessage)


def main(argv=None):
    """Just for testing this module"""
    if argv is None:
        argv = sys.argv
    cnvDefs = CNVDefinitionCollection(argv[1])
    while True:
        strLine = raw_input('Enter chromosome number and position separated by space: ')
        (strChr, strPosn) = strLine.split()
        stCNVs = cnvDefs.getCNVsForLocus(strChr, int(strPosn))
        for cnv in stCNVs:
            print cnv

    return


if __name__ == '__main__':
    sys.exit(main())