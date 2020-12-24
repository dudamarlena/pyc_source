# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/merge_birdsuite_plink_qc.py
# Compiled at: 2010-07-13 12:32:46
"""usage %prog [options]

Merge Plink HWE and Mendel error reports with Birdsuite mendel_check reports.
Uses only ALL lines from Plink HWE.  Only prints a record if it appears in
the Birdsuite HWE file, which implies that a record is printed only for those SNPs
that are tri-allelic (or less).
"""
from __future__ import division
import optparse, sys
from mpgutils import utils
lstRequiredOptions = [
 'plink_hwe', 'plink_lmendel', 'birdsuite_hwe', 'birdsuite_lmendel', 'output']

def loadMap(strMapPath):
    dctRet = {}
    for (strRS, strSNP) in utils.iterateWhitespaceDelimitedFile(strMapPath, iNumFieldsExpected=2):
        dctRet[strRS] = strSNP

    return dctRet


def loadPlinkHWE(strPlinkHWE, dctSNPMap):
    dctRet = {}
    for lstFields in utils.iterateWhitespaceDelimitedFile(strPlinkHWE, iNumFieldsExpected=6, bSkipHeader=True):
        if lstFields[1] != 'ALL':
            continue
        strSNP = lstFields[0]
        if dctSNPMap is not None:
            strSNP = dctSNPMap[strSNP]
        dctRet[strSNP] = lstFields[5]

    return dctRet


def loadPlinkLMendel(strPlinkLMendel, dctSNPMap):
    dctRet = {}
    for lstFields in utils.iterateWhitespaceDelimitedFile(strPlinkLMendel, iNumFieldsExpected=3, bSkipHeader=True):
        strSNP = lstFields[1]
        if dctSNPMap is not None:
            strSNP = dctSNPMap[strSNP]
        dctRet[strSNP] = lstFields[2]

    return dctRet


def loadBirdsuiteLMendel(strBirdsuiteLMendel):
    dctRet = {}
    for (strSNP, strCount) in utils.iterateWhitespaceDelimitedFile(strBirdsuiteLMendel, iNumFieldsExpected=2, bSkipHeader=True):
        dctRet[strSNP] = strCount

    return dctRet


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--plink_hwe', help='(Required) HWE file produced by Plink.')
    parser.add_option('--plink_lmendel', help='(Required) lmendel file produced by Plink.')
    parser.add_option('--birdsuite_hwe', help='(Required) HWE file produced by mendel_check.py on larry_bird calls.')
    parser.add_option('--birdsuite_lmendel', help='(Required) lmendel file produced by mendel_check.py on larry_bird calls.')
    parser.add_option('-o', '--output', help='(Required) Output file.')
    parser.add_option('--snp_map', help='Map from SNP names in Plink input files to those in Birdsuite input files.')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if dctOptions.snp_map is not None:
        dctSNPMap = loadMap(dctOptions.snp_map)
    else:
        dctSNPMap = None
    dctPlinkHWE = loadPlinkHWE(dctOptions.plink_hwe, dctSNPMap)
    dctPlinkLMendel = loadPlinkLMendel(dctOptions.plink_lmendel, dctSNPMap)
    dctBirdsuiteLMendel = loadBirdsuiteLMendel(dctOptions.birdsuite_lmendel)
    fOut = open(dctOptions.output, 'w')
    print >> fOut, ('\t').join(['SNP', 'POBS_HWE_PValue', 'POBS_Mendel_Errors', 'Birdsuite_HWE_PValue', 'Birdsuite_Mendel_Errors',
     'Birdsuite_0_Freq', 'Birdsuite_A_Freq', 'Birdsuite_B_Freq'])
    for lstFields in utils.iterateWhitespaceDelimitedFile(dctOptions.birdsuite_hwe, iNumFieldsExpected=7, bSkipHeader=True):
        strSNP = lstFields[0]
        (strPValue, str0Freq, strAFreq, strBFreq) = lstFields[3:]
        print >> fOut, ('\t').join([strSNP, dctPlinkHWE[strSNP], dctPlinkLMendel[strSNP],
         strPValue, dctBirdsuiteLMendel[strSNP], str0Freq, strAFreq, strBFreq])

    fOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())