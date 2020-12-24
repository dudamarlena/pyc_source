# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/birdsuite/pre_birdseye.py
# Compiled at: 2009-04-08 14:34:54
"""usage: %prog
"""
from __future__ import division
import optparse, os, sys, initializeCNGaussians
from mpgutils import utils
lstRequiredOptions = [
 'basename', 'summary', 'snp_clusters', 'gender_file']
strBIRDSEYE_DIRECTORY_EXTENSION = '.birdseye_dir'
iPROBE_NAME_INDEX = 0
iPROBE_TYPE_INDEX = 3
iNUM_FIELDS_OF_INTEREST = 4

def loadClusters(strClustersFile):
    dctRet = {}
    fIn = open(strClustersFile)
    for strLine in fIn:
        lstFields = strLine.split(';', 1)
        strSNPName = lstFields[0]
        if not strSNPName.endswith('-2'):
            continue
        strSNPName = strSNPName[:-2]
        dctRet[strSNPName] = strLine

    fIn.close()
    return dctRet


def loadSpecialProbes(strSpecialProbesFile):
    stRet = set()
    fIn = open(strSpecialProbesFile)
    for strLine in fIn:
        if strLine.startswith('probeset_id'):
            break

    for strLine in fIn:
        stRet.add(strLine.split()[0])

    fIn.close()
    return stRet


def getProbeName(lstFields):
    strProbeName = lstFields[iPROBE_NAME_INDEX]
    if lstFields[iPROBE_TYPE_INDEX] == 'C':
        return strProbeName
    assert strProbeName.endswith('-A') or strProbeName.endswith('-B')
    return strProbeName[:-2]


def readHeader(fIn):
    lstHeaderLines = []
    for strLine in fIn:
        lstHeaderLines.append(strLine)
        if strLine.startswith('probeset_id'):
            break

    return lstHeaderLines


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-b', '--basename', help='(Required) Used to name all the output files.')
    parser.add_option('--summary', help='(Required) Annotated allele summaries')
    parser.add_option('--snp_clusters', help='(Required) Clusters produced by birdseed --write-clusters option.')
    parser.add_option('--gender_file', help='(Required) File containing a line for each sample in the calls file.\n0=female, 1=male, 2=unknown.  This file must have a header line "gender".\nOrder must agree with order of summary file.')
    parser.add_option('--special_probes', action='append', help='Special SNPs and/or special CN probes file.  This option may be used more than\nonce if special SNPs and special CN probes are in separate files.  Any probe that is special is not used by\nbirdseye.  Default: No probes are considered special')
    parser.add_option('--exclusions', help='File specifying CN/sample pairs to be excluded when generating CN clusters.')
    parser.add_option('-o', '--output_dir', default='.', help='A subdirectory containing birdseye input files for each chromosome\nis created in this directory.  Default: current directory')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    dctSnpClusters = loadClusters(dctOptions.snp_clusters)
    stSpecialProbes = set()
    for strSpecialProbesFile in dctOptions.special_probes:
        stSpecialProbes |= loadSpecialProbes(strSpecialProbesFile)

    if dctOptions.exclusions is not None:
        dctExclusions = initializeCNGaussians.parseExclusions(dctOptions.exclusions, bIncludeSNPs=False)
    else:
        dctExclusions = None
    lstGenders = utils.loadGenders(dctOptions.gender_file)
    lstFemaleIndices = [ i for (i, iGender) in enumerate(lstGenders) if iGender == 0 ]
    lstMaleIndices = [ i for (i, iGender) in enumerate(lstGenders) if iGender == 1 ]
    fIn = open(dctOptions.summary)
    lstHeaderLines = readHeader(fIn)
    strCurrChr = None
    fCNSummaries = None
    fSNPSummaries = None
    for strLine in fIn:
        lstFields = strLine.split(None, iNUM_FIELDS_OF_INTEREST)
        if strCurrChr != lstFields[1]:
            if strCurrChr is not None:
                if fSNPSummaries is not None:
                    fSNPSummaries.close()
                    fSNPClusters.close()
                if fCNSummaries is not None:
                    fCNSummaries.close()
                    if strCurrChr == '23':
                        lstIndicesToInclude = lstFemaleIndices
                    elif strCurrChr == '24':
                        lstIndicesToInclude = lstMaleIndices
                        print lstMaleIndices
                    else:
                        lstIndicesToInclude = None
                    initializeCNGaussians.doIt(os.path.join(strCurrOutputDir, 'CNsummaries.txt'), os.path.join(strCurrOutputDir, 'CNclusters.txt'), bExpectHeader=True, dctExclusions=dctExclusions, lstSampleIndices=lstIndicesToInclude)
                print 'Done pre-birdseye for', strCurrOutputDir
                fSNPSummaries = None
                fSNPClusters = None
                fCNSummaries = None
            strCurrChr = lstFields[1]
            strCurrOutputDir = os.path.join(dctOptions.output_dir, dctOptions.basename + '.' + strCurrChr + strBIRDSEYE_DIRECTORY_EXTENSION)
            if not os.path.exists(strCurrOutputDir):
                os.mkdir(strCurrOutputDir)
        strProbeName = getProbeName(lstFields)
        if strProbeName in stSpecialProbes:
            continue
        if lstFields[iPROBE_TYPE_INDEX] == 'C':
            if fCNSummaries is None:
                fCNSummaries = open(os.path.join(strCurrOutputDir, 'CNsummaries.txt'), 'w')
                fCNSummaries.write(lstHeaderLines[(-1)])
            fCNSummaries.write(strLine)
        else:
            if fSNPSummaries is None:
                fSNPSummaries = open(os.path.join(strCurrOutputDir, 'SNPsummaries.txt'), 'w')
                fSNPSummaries.write(lstHeaderLines[(-1)])
                fSNPClusters = open(os.path.join(strCurrOutputDir, 'SNPclusters.txt'), 'w')
            fSNPSummaries.write(strLine)
            if lstFields[iPROBE_NAME_INDEX].endswith('-A'):
                if strProbeName in dctSnpClusters:
                    fSNPClusters.write(dctSnpClusters[strProbeName])
                else:
                    print >> fSNPClusters, strProbeName + '-0'

    if fSNPSummaries is not None:
        fSNPSummaries.close()
        fSNPClusters.close()
    if fCNSummaries is not None:
        fCNSummaries.close()
        if strCurrChr == '23':
            lstIndicesToInclude = lstFemaleIndices
        elif strCurrChr == '24':
            lstIndicesToInclude = lstMaleIndices
        else:
            lstIndicesToInclude = None
        initializeCNGaussians.doIt(os.path.join(strCurrOutputDir, 'CNsummaries.txt'), os.path.join(strCurrOutputDir, 'CNclusters.txt'), bExpectHeader=True, dctExclusions=dctExclusions, lstSampleIndices=lstIndicesToInclude)
    print 'Done pre-birdseye for', strCurrOutputDir
    return


if __name__ == '__main__':
    sys.exit(main())