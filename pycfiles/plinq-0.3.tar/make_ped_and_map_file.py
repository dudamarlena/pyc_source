# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/make_ped_and_map_file.py
# Compiled at: 2010-07-13 12:32:48
__doc__ = '%prog [options]\n\nCreate a PED and MAP file in the format desired by Plink, from 1chip-style calls & confidences files.\n'
from __future__ import division
import optparse, re, sys
strDefaultMap3Path = '/humgen/cnp04/sandbox/snp_analysis/20Ksnps.map3'
lstRequiredOptions = [
 'map3Path',
 'pedigreePath',
 'callsPath',
 'confidencesPath',
 'thresholdFloat',
 'outputMapPath',
 'outputPedPath']
dctCallMap = {None: '\t0 0', 
   -1: '\t0 0', 
   0: '\tA A', 
   1: '\tA B', 
   2: '\tB B'}
lstreCELNameSplitter = [
 re.compile('.+\\((?P<PLATE>.+)\\)_BI_SNP_(?P<WELL>[A-Z]\\d\\d)_\\d+(?:_\\d+)?\\.CEL$'),
 re.compile('.+/(?P<PLATE>[^/]+)_p_.*_BI_SNP_(?P<WELL>[A-Z]\\d\\d)_\\d+(?:_\\d+)?\\.CEL$')]

def loadTSV(strPath, lstKeyFields):
    """Read lines from strPath, which is a tab-delimited file.
    Return a dictionary in which each value is a list of all the values on a line.
    The key is a list of the values on that line in lstKeyFields.  if len(lstKeyFields) == 1,
    then the key is just that value."""
    dctRet = {}
    f = open(strPath)
    iSingleKeyField = None
    if len(lstKeyFields) == 1:
        iSingleKeyField = lstKeyFields[0]
    for strLine in f:
        strLine = strLine.rstrip('\n').rstrip('\r')
        lstFields = strLine.split('\t')
        if iSingleKeyField is not None:
            dctRet[lstFields[iSingleKeyField]] = lstFields
        else:
            lstKey = []
            for iKeyField in lstKeyFields:
                lstKey.append(lstFields[iKeyField])

            dctRet[tuple(lstKey)] = lstFields

    f.close()
    return dctRet


def loadColumnFromTSV(strPath, iColumn):
    """return a list of the value from column iColumn from the tab-delimited file strPath"""
    lstRet = []
    f = open(strPath)
    for strLine in f:
        lstFields = strLine.rstrip('\n').split('\t')
        lstRet.append(lstFields[iColumn])

    f.close()
    return lstRet


def findLineWithoutSymbol(matchString, file):
    while True:
        pos = file.tell()
        strCallHeader = file.readline()
        if not strCallHeader.startswith(matchString):
            file.seek(pos)
            return file


def getIndividualName(strCELFile, dctPlateMap, reIndividual=None):
    """Match the a cel file name to the regular expressions, in the order provided.  
Hopefully this lets you search over multiple patterns to find one that fits your cel file naming scheme.
More hopefully, there is only 1 or 2 of these nameing schemes in the first place!"""
    if reIndividual is not None:
        return reIndividual.match(strCELFile).group(1)
    for pattern in lstreCELNameSplitter:
        match = pattern.match(strCELFile)
        if match is not None:
            return dctPlateMap[match.groups()][2]

    print >> sys.stderr, 'ERROR: Unrecognized CEL file name', strCELFile
    sys.exit()
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--map3', dest='map3Path', help='tab-delimited map3 file with 3 columns: chromosome, SNP, position.  Default: ' + strDefaultMap3Path)
    parser.add_option('--platemap', dest='plateMapPath', help='tab-delimited file with 3 columns: container, well, participant ID, used to determine a participant ID for AGRE plates.')
    parser.add_option('--individual-regexp', dest='individualRegexp', help='Regexp used to get an individual ID from a CEL file name.')
    parser.add_option('--pedigree', dest='pedigreePath', help='tab-delimited file with 5 columns: Family ID, Individual ID, Father ID, Mother ID, Gender (1=M, 2=F)')
    parser.add_option('--calls', dest='callsPath', help='tab-delimited file with 1 line for each SNP, 1 column for each genotype call, plus 1st column is SNP name.  Header line has CEL file name for each column of genotypes.  Genotypes are: 0=AA, 1=AB, 2=BB.')
    parser.add_option('--confidences', dest='confidencesPath', help='tab-delimited file identical to calls file, except that each value in the matrix is a confidence of the ' + 'corresponding genotype call in the calls file.')
    parser.add_option('--threshold', dest='thresholdFloat', type='float', help='If a genotype has confidence <= this value, it is considered a no-call')
    parser.add_option('--output-map', dest='outputMapPath', help='Where to write the map file.')
    parser.add_option('--output-ped', dest='outputPedPath', help='Where to write the ped file.')
    parser.set_defaults(map3Path=strDefaultMap3Path, plateMapPath=None, pedigreePath=None, callsPath=None, confidencesPath=None, thresholdFloat=None, outputMapPath=None, outputPedPath=None, individualRegexp=None)
    (options, lstArgs) = parser.parse_args(argv)
    for strOpt in lstRequiredOptions:
        if getattr(options, strOpt) is None:
            print >> sys.stderr, 'ERROR:', strOpt, 'argument is required.'
            parser.print_help()
            return 1

    if not options.plateMapPath and not options.individualRegexp:
        print >> sys.stderr, 'ERROR: You must use either --platemap or --individual-regexp.'
        parser.print_help()
        return 1
    if len(lstArgs) > 1:
        print >> sys.stderr, 'ERROR: extra args on command line.'
        parser.print_help()
        return 1
    dctMap3 = loadTSV(options.map3Path, [1])
    dctPlateMap = None
    reIndividual = None
    if options.plateMapPath:
        dctPlateMap = loadTSV(options.plateMapPath, [0, 1])
    else:
        reIndividual = re.compile(options.individualRegexp)
    dctPedigree = loadTSV(options.pedigreePath, [1])
    lstSNPs = loadColumnFromTSV(options.map3Path, 1)
    fCalls = open(options.callsPath)
    fConfidences = open(options.confidencesPath)
    fCalls = findLineWithoutSymbol('#', fCalls)
    fConfidencesr = findLineWithoutSymbol('#', fConfidences)
    strCallsHeader = fCalls.readline()
    strConfidencesHeader = fConfidences.readline()
    if strCallsHeader != strConfidencesHeader:
        print >> sys.stderr, 'ERROR: Header lines in', options.callsPath, 'and', options.confidencesPath, 'do not agree.'
        return 1
    strCallsHeader = strCallsHeader.rstrip('\n')
    lstCELFiles = strCallsHeader.split('\t')[1:]
    lstIndividualIDs = []
    for strCELFile in lstCELFiles:
        strIndividualID = getIndividualName(strCELFile, dctPlateMap, reIndividual)
        if strIndividualID in lstIndividualIDs:
            lstIndividualIDs[lstIndividualIDs.index(strIndividualID)] = None
        lstIndividualIDs.append(strIndividualID)

    dctCallsBySNP = {}
    for (iLineNum, strCalls) in enumerate(fCalls):
        strCalls = strCalls.rstrip()
        strConfidences = fConfidences.readline().rstrip()
        lstCalls = strCalls.split('\t')
        lstConfidences = strConfidences.split('\t')
        if lstCalls[0] != lstConfidences[0]:
            print >> sys.stderr, 'ERROR: SNP mismatch between', options.callsPath, 'and', options.confidencesPath, 'at line', iLineNum, ';', lstCalls[0], '!=', lstConfidences[0]
            return 1
        strSNP = lstCalls[0]
        del lstCalls[0]
        del lstConfidences[0]
        if len(lstCalls) != len(lstIndividualIDs):
            print >> sys.stderr, 'ERROR: Wrong number of values in', options.callsPath, ':', iLineNum, '; Expected', len(lstIndividualIDs), 'but was', len(lstCalls)
            return 1
        if len(lstConfidences) != len(lstIndividualIDs):
            print >> sys.stderr, 'ERROR: Wrong number of values in', options.confidencesPath, ':', iLineNum, '; Expected', len(lstIndividualIDs), 'but was', len(lstConfidences)
            return 1
        lstConfidentCalls = []
        for i in xrange(len(lstCalls)):
            if float(lstConfidences[i]) >= options.thresholdFloat:
                lstConfidentCalls.append(None)
            else:
                lstConfidentCalls.append(int(lstCalls[i]))

        dctCallsBySNP[strSNP] = lstConfidentCalls

    lstCalledSNPs = [ strSNP for strSNP in lstSNPs if strSNP in dctCallsBySNP ]
    fMap = open(options.outputMapPath, 'w')
    for strSNP in lstCalledSNPs:
        print >> fMap, '%s\t%s\t0\t%s' % tuple(dctMap3[strSNP])

    fMap.close()
    fPed = open(options.outputPedPath, 'w')
    for (i, strIndividualID) in enumerate(lstIndividualIDs):
        if strIndividualID is None:
            continue
        try:
            tupPedigree = dctPedigree[strIndividualID]
        except KeyError:
            print >> sys.stderr, 'Could not find pedigree for', strIndividualID
            raise

        fPed.write(('\t').join(tupPedigree))
        fPed.write('\t0')
        for strSNP in lstCalledSNPs:
            fPed.write(dctCallMap[dctCallsBySNP[strSNP][i]])

        fPed.write('\n')

    fPed.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())