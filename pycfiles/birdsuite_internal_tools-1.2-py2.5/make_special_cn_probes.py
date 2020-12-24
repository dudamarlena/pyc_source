# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/make_special_cn_probes.py
# Compiled at: 2008-12-05 10:08:25
"""usage: make_special_cn_probes.py annotation_file PARspec1 PARspec2... 

Create special_cn_probes file from Affy CN annotation file.  special_cn_probes
file is written to stdout.

PARspecs are in the form chr:start-end, e.g. X:1-2709520"""
from __future__ import division
import sys

class PARSpecs(object):

    def __init__(self, lstPARSpecs):
        self._lstSpecs = []
        for strPARSpec in lstPARSpecs:
            (strChr, strRest) = strPARSpec.split(':')
            (strStart, strEnd) = strRest.split('-')
            self._lstSpecs.append((strChr, int(strStart), int(strEnd)))

    def convertChrForPAR(self, strChr, iStart, iEnd):
        for tupPARSpec in self._lstSpecs:
            if strChr == tupPARSpec[0] and iStart >= tupPARSpec[1] and iEnd <= tupPARSpec[2]:
                return 'PAR'

        return strChr


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parSpecs = PARSpecs(argv[2:])
    fIn = open(argv[1])
    for strLine in fIn:
        if not strLine.startswith('#'):
            break

    assert strLine.startswith('"Probe Set ID"')
    print ('\t').join(['probeset_id', 'chr', 'copy_male', 'copy_female'])
    for strLine in fIn:
        strLine = strLine.rstrip('"\n')
        strLine = strLine.lstrip('"')
        lstFields = strLine.split('","')
        if lstFields[1] not in ('X', 'Y', 'MT'):
            continue
        strProbe = lstFields[0]
        strChr = lstFields[1]
        iStart = int(lstFields[2])
        iEnd = int(lstFields[3])
        strChr = parSpecs.convertChrForPAR(strChr, iStart, iEnd)
        if strChr == 'X':
            iCopyMale = 1
            iCopyFemale = 2
        elif strChr == 'Y':
            iCopyMale = 1
            iCopyFemale = 0
        elif strChr == 'PAR':
            iCopyMale = 2
            iCopyFemale = 2
        elif strChr == 'MT':
            iCopyMale = 1
            iCopyFemale = 1
        print ('\t').join([strProbe, strChr, str(iCopyMale), str(iCopyFemale)])

    fIn.close()
    return


if __name__ == '__main__':
    sys.exit(main())