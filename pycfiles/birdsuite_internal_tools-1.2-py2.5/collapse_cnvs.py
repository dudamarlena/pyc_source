# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/collapse_cnvs.py
# Compiled at: 2008-12-16 12:17:03
"""usage: %prog [options] <input file>

Take a file that has 6 columns:
sample_id
chr 
start 
end 
copy_number
score

Looks for common regions, and creates an output file of those common regions.
"""
import sys, numpy, optparse
from mpgutils import utils
import numpy
CNP_DEF_SAMPLE_ID_FIELD_INDEX = 0
CNP_DEF_CHR_FIELD_INDEX = 1
CNP_DEF_START_POSN_FIELD_INDEX = 2
CNP_DEF_END_POSN_FIELD_INDEX = 3
CNP_DEF_COPY_NUMBER_FIELD_INDEX = 4
CNP_DEF_CN_SCORE_FIELD_INDEX = 5
NUM_CNP_DEFINITION_FIELDS = 6

class RangeCNP(object):
    """Holds the definition of a CNP that is described by start and end loci."""

    def __init__(self, strLine):
        lstFields = strLine.split()
        if len(lstFields) < NUM_CNP_DEFINITION_FIELDS - 1 or len(lstFields) > NUM_CNP_DEFINITION_FIELDS:
            raise Exception('Wrong number of fields (%d).  Expected %d fields.' % (
             len(lstFields), NUM_CNP_DEFINITION_FIELDS))
        self.strSampleID = lstFields[CNP_DEF_SAMPLE_ID_FIELD_INDEX]
        self.iChr = int(utils.convertChromosomeStr(lstFields[CNP_DEF_CHR_FIELD_INDEX]))
        self.iStartPosn = int(lstFields[CNP_DEF_START_POSN_FIELD_INDEX])
        self.iEndPosn = int(lstFields[CNP_DEF_END_POSN_FIELD_INDEX])
        self.iCopyNumber = int(lstFields[CNP_DEF_COPY_NUMBER_FIELD_INDEX])
        self.iCNScore = float(lstFields[CNP_DEF_CN_SCORE_FIELD_INDEX])

    def getOutputFields(self):
        return [
         self.strSampleID, str(self.iChr), str(self.iStartPosn), str(self.iEndPosn), str(self.iCopyNumber), str(self.iCNScore)]

    def __str__(self):
        return str(self.getOutputFields())

    def cmpCNPDefinitionsByPosition(a, b):
        """Sorts CNPs by locus.  Primary sort is chromosome, then start posn, then end posn"""
        iCmpChromosome = cmp(a.iChr, b.iChr)
        if iCmpChromosome != 0:
            return iCmpChromosome
        iCmpStartPosn = cmp(a.iStartPosn, b.iStartPosn)
        if iCmpStartPosn != 0:
            return iCmpStartPosn
        return cmp(a.iEndPosn, b.iEndPosn)

    def isOverlapping(self, other, overlapDistance, overlapPercent):
        inner = min(self.iEndPosn, other.iEndPosn) - max(self.iStartPosn, other.iStartPosn)
        outer = max(self.iEndPosn, other.iEndPosn) - min(self.iStartPosn, other.iStartPosn)
        thisOverlapPct = float(inner) / float(outer)
        if abs(self.iStartPosn - other.iStartPosn) < overlapDistance and abs(self.iEndPosn - other.iEndPosn) < overlapDistance and thisOverlapPct > overlapPercent and self.iChr == other.iChr:
            return True
        return False

    def prettyOut(self):
        return ('\t').join(self.getOutputFields())


def loadRangeCNPDefinitions(strCnpDefsFile):
    """Reads the CNP definitions from the file, does some validation, sorts by genomic positions,
    and returns a list of RangeCNP objects."""
    lstRet = []
    fIn = open(strCnpDefsFile)
    strHeader = fIn.readline()
    lstFields = strHeader.split()
    for strLine in fIn:
        lstRet.append(RangeCNP(strLine))

    fIn.close()
    lstRet.sort(cmp=RangeCNP.cmpCNPDefinitionsByPosition)
    return lstRet


def getSampleSize(lstRangeCNPs):
    setSampleNames = set()
    for cnp in lstRangeCNPs:
        setSampleNames.add(cnp.strSampleID)

    print 'Number of unique samples' + str(len(setSampleNames))
    return len(setSampleNames)


def filterByScore(lstRangeCNPs, fScoreThreshold):
    """Filter CNPs by score threshold.  They must have a score >= threshold to be incorperated."""
    lstResult = []
    for cnp in lstRangeCNPs:
        if cnp.iCNScore >= fScoreThreshold:
            lstResult.append(cnp)

    print 'retained ' + str(len(lstResult)) + ' of ' + str(len(lstRangeCNPs)) + ' events'
    return lstResult


def testFreq(sampleSize, idxIncluded, frequencyThreshold):
    return float(len(idxIncluded)) / float(sampleSize) > frequencyThreshold


def getMedianStart(lstRangeCNPs, index):
    lstTemp = []
    for i in index:
        lstTemp.append(lstRangeCNPs[i].iStartPosn)

    return int(numpy.median(lstTemp))


def getMedianEnd(lstRangeCNPs, index):
    lstTemp = []
    for i in index:
        lstTemp.append(lstRangeCNPs[i].iEndPosn)

    return int(numpy.median(lstTemp))


def writeMergedCNV(baseCNV, lstRangeCNPs, idxIncluded, outFile):
    outFields = [
     str(baseCNV.iChr), str(baseCNV.iStartPosn), str(baseCNV.iEndPosn)]
    for cnpIdx in idxIncluded:
        cnp = lstRangeCNPs[cnpIdx]
        outFields.append(cnp.strSampleID)

    print >> outFile, ('\t').join(outFields)


def findOverlaps(lstRangeCNPs, sampleSize, overlapDistance, overlapPercent, frequencyThreshold, outFile, verbose=True):
    baseCNV = None
    lastGoodIdx = -1
    index = 0
    allGoodCNVIdx = []
    while index < len(lstRangeCNPs):
        if baseCNV is None:
            index = lastGoodIdx + 1
            lastGoodIdx = index
            if index + 1 >= len(lstRangeCNPs):
                break
            baseCNV = lstRangeCNPs[index]
            idxIncluded = [index]
            index = index + 1
        nextCNV = lstRangeCNPs[index]
        if verbose:
            print 'BaseCNV ' + ('\t').join(baseCNV.getOutputFields())
            print 'NextCNV ' + ('\t').join(nextCNV.getOutputFields())
        if baseCNV.isOverlapping(nextCNV, overlapDistance, overlapPercent):
            if verbose:
                print 'merged'
            idxIncluded.append(index)
            baseCNV.iStartPosn = getMedianStart(lstRangeCNPs, idxIncluded)
            baseCNV.iEndPosn = getMedianEnd(lstRangeCNPs, idxIncluded)
            lastGoodIdx = index
        elif abs(baseCNV.iStartPosn - nextCNV.iStartPosn) > overlapDistance or baseCNV.iChr != nextCNV.iChr:
            if verbose:
                print 'stop merge'
            freqFlag = testFreq(sampleSize, idxIncluded, frequencyThreshold)
            if freqFlag:
                allGoodCNVIdx.extend(idxIncluded)
                writeMergedCNV(baseCNV, lstRangeCNPs, idxIncluded, outFile)
                if verbose:
                    print 'Final CNV ' + ('\t').join(baseCNV.getOutputFields())
            baseCNV = None
        elif verbose:
            print 'not merged'
        index = index + 1

    print 'done finding overlaps'
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--score_threshold', dest='scoreThreshold', default=10, help='Filter the events so that they have a score >= the threshold provided.\n                      Default score is 10.')
    parser.add_option('--overlap_distance', dest='overlapDistance', default=100000, help="the maximum distance between the putative CNP's\nstart/end site and the test CNV's start/end site, for the test CNV to\nbe added.  Reasonable values are anywhere between 10kb (10000) and 1Mb (1000000).\nDefault:100000")
    parser.add_option('--overlap_pct', dest='overlapPercent', default=0.3, help='he minimum overlap between the putative CNP and the\ntest CNV, for the test CNV to be added.  Reasonable values are in the\nrange of 0.01-0.8.  Default .3')
    parser.add_option('--frequency', dest='frequency', default=0.01, help='the frequency of the new CNP for it to be "worth" being\ncalled a CNP.  Anywhere from 0.00001 to 0.05 is reasonable.  I should\nnote this number is actually compared to % of the population with a\nCNV call, not allele frequency...so 0.05 really corresponds more to a\n2.5% AF  Default .01')
    parser.add_option('--output_collapsed', dest='outputCollapsed', default='new_cnps.txt', help='The collapsed CNV output file.  Default is new_cnps.txt')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) < 2:
        print >> sys.stderr, 'ERROR: Missing required arguments.  Requires at least 1 cnv events file.\n'
        parser.print_help()
        return 1
    fOut = open(dctOptions.outputCollapsed, 'w')
    try:
        fScoreThreshold = float(dctOptions.scoreThreshold)
    except TypeError:
        print str(dctOptions.scoreThreshold) + 'is not a number!'

    lstRangeCNPs = loadRangeCNPDefinitions(lstArgs[1])
    lstRangeCNPs = filterByScore(lstRangeCNPs, fScoreThreshold)
    numSamples = getSampleSize(lstRangeCNPs)
    findOverlaps(lstRangeCNPs, numSamples, dctOptions.overlapDistance, dctOptions.overlapPercent, dctOptions.frequency, fOut)
    print 'FINISHED.'
    return


if __name__ == '__main__':
    sys.exit(main())