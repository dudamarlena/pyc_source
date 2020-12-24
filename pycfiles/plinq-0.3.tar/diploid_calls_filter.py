# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/plink_pipeline/diploid_calls_filter.py
# Compiled at: 2010-07-19 17:15:11
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