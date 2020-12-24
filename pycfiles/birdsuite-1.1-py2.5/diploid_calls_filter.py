# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plink_pipeline/diploid_calls_filter.py
# Compiled at: 2009-01-27 09:41:59
from mpgutils import utils

class Filter(object):

    def __init__(self, strGenderFile, strSpecialSNPsFile):
        self._lstGenders = utils.loadGenders(strGenderFile)
        self._dctSpecialSNPs = {}
        utils.loadSpecialProbes(self._dctSpecialSNPs, strSpecialSNPsFile)
        self.lstExpectedSNPs = []
        self.lstUnexpectedSNPs = []

    def numSamples(self):
        return len(self._lstGenders)

    def filterCalls(self, strSNP, lstCalls):
        tupExpectedCount = self._dctSpecialSNPs.get(strSNP, (2, 2))
        lstOutput = [
         None] * len(lstCalls)
        lstGenders = self._lstGenders
        bAnyCallZapped = False
        for (i, strCall) in enumerate(lstCalls):
            if strCall is None:
                iA = -1
                iB = -1
            else:
                (iA, iB) = [ int(strVal) for strVal in strCall.split(',') ]
            if iA == -1:
                if iB != -1:
                    raise Exception('Strange call (' + strCall + ') for SNP ' + strSNP)
                lstOutput[i] = -1
            elif tupExpectedCount[lstGenders[i]] == 0:
                lstOutput[i] = -1
                bAnyCallZapped = True
            else:
                iTotal = iA + iB
                if iTotal != tupExpectedCount[lstGenders[i]]:
                    lstOutput[i] = -1
                    bAnyCallZapped = True
                elif iTotal == 2 or iB != 1:
                    lstOutput[i] = iB
                else:
                    lstOutput[i] = 2

        if bAnyCallZapped:
            self.lstUnexpectedSNPs.append(strSNP)
        else:
            self.lstExpectedSNPs.append(strSNP)
        return lstOutput