# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/calls_confidences_filter.py
# Compiled at: 2010-07-13 12:32:47
"""usage: %prog [options] 

Filters calls, confidences and/or guide file based on a list of samples and/or SNPs to include.

In general you only need to specify input and output file arguments for the files you want to filter.
However, if you are filtering by sample, you must supply an input calls file.  If you don't otherwise
care about the filtered calls file, supply /dev/null for --out-calls.  This is because the calls file
is used to determine the correspondence between samples and columns.
"""
from __future__ import division
import optparse, os.path, sys

def readSnpFile(strPath):
    f = open(strPath)
    setSnps = set()
    for line in f:
        line = line.split()
        if line[0] == 'probeset_id' or line[0] == 'cnp_id':
            continue
        setSnps.add(line[0])

    f.close()
    return setSnps


def readSampleList(strPath):
    f = open(strPath)
    lstRet = [ strLine.strip() for strLine in f ]
    f.close()
    return lstRet


def getSampleIndicesToProcess(lstSamplesToProcess, callFile):
    """Given a list of sample names, find the header line in the calls file,
    and return the 1-based indices of the samples in the list.  The indices
    are returned in ascending order, regardless of the order they appear in
    lstSamplesToProcess.  It is an error if a sample in the list is not found
    in the file."""
    fin = open(callFile)
    for strLine in fin:
        if strLine.startswith('#'):
            continue
        assert strLine.startswith('probeset_id') or strLine.startswith('cnp_id')
        break
    else:
        raise Exception("Strange calls file, can't find probeset_id: " + callFile)

    fin.close()
    lstFields = [ os.path.basename(strSample) for strSample in strLine.split() ]
    try:
        lstRet = [ lstFields.index(strSample) for strSample in lstSamplesToProcess ]
    except ValueError:
        strErr = 'ERROR: ' + strSample + ' was not found in ' + callFile
        raise Exception(strErr)

    lstRet.sort()
    return lstRet


class FilteringCallsFile(object):

    def __init__(self, fRaw, lstSampleIndices=None, stSNPs=None):
        self.fRaw = fRaw
        self.lstSampleIndices = lstSampleIndices
        self.stSNPs = stSNPs

    def close(self):
        self.fRaw.close()

    def readline(self):
        while True:
            strLine = self.fRaw.readline()
            if len(strLine) == 0:
                return strLine
            if strLine.startswith('#'):
                return strLine
            if strLine.startswith('probeset_id') or strLine.startswith('cnp_id') or self.stSNPs is None:
                return self.filterLineForSamples(strLine)
            strSNP = strLine.split(None, 1)[0]
            if strSNP in self.stSNPs:
                return self.filterLineForSamples(strLine)

        return

    def __iter__(self):
        while True:
            strLine = self.readline()
            if len(strLine) == 0:
                raise StopIteration
            yield strLine

    def filterLineForSamples(self, strLine):
        if self.lstSampleIndices is None:
            return strLine
        lstFields = strLine.split()
        lstRet = [lstFields[0]] + [ lstFields[i] for i in self.lstSampleIndices ]
        return ('\t').join(lstRet) + '\n'


class FilteringGuideFile(object):

    def __init__(self, fRaw, lstSampleIndices):
        self.fRaw = fRaw
        self.lstSampleIndices = lstSampleIndices
        self.iCurrentLine = 0
        self.iSampleIndex = 0

    def close(self):
        self.fRaw.close()

    def readline(self):
        if self.iSampleIndex >= len(self.lstSampleIndices):
            return ''
        iLineToReturn = self.lstSampleIndices[self.iSampleIndex]
        self.iSampleIndex += 1
        return self._returnLine(iLineToReturn)

    def _returnLine(self, iLineToReturn):
        while iLineToReturn > self.iCurrentLine:
            strLine = self.fRaw.readline()
            self.iCurrentLine += 1

        return strLine

    def __iter__(self):
        while True:
            strLine = self.readline()
            if strLine is None or len(strLine) == 0:
                raise StopIteration
            yield strLine

        return


class FilteringCallsAndConfidencesFileFactory(object):
    """After construction, self.fCalls and self.fConfidences are file-like objects that read from
    given calls and confidences files, possible with filtering of samples and/or SNPs.
    self.lstSampleIndicesToProcess if not None, is a 1-based list of indices of samples to be included.
    self.fGuide, if not None, is a file-like object that returns a filtered guide file."""

    def __init__(self, strCallsPath=None, strConfidencesPath=None, strGuidePath=None, strSamplesListPath=None, strSNPsListPath=None):
        """strSamplesListPath is a file containing sample file names to be included, one per line.
        If None, all samples are included.
        strSNPsListPath is a file containing SNPs to be included, one per line.  The file may optionally
        have a header line with the string "probeset_id".  If None, all SNPs are included."""
        self.lstSampleIndicesToProcess = None
        if strSamplesListPath is None and strSNPsListPath is None:
            if strCallsPath is not None:
                self.fCalls = open(strCallsPath)
            else:
                self.fCalls = None
            if strConfidencesPath is not None:
                self.fConfidences = open(strConfidencesPath)
            else:
                self.fConfidences = None
            if strGuidePath is not None:
                self.fGuide = open(strGuidePath)
            else:
                self.fGuide = None
            return
        if strSamplesListPath is not None:
            lstSamplesToProcess = readSampleList(strSamplesListPath)
            self.lstSampleIndicesToProcess = getSampleIndicesToProcess(lstSamplesToProcess, strCallsPath)
        if strSNPsListPath is not None:
            stSNPs = set(readSampleList(strSNPsListPath))
            print 'Filtering using ' + str(len(stSNPs)) + ' total snps'
        else:
            stSNPs = None
        if strCallsPath is not None:
            self.fCalls = FilteringCallsFile(open(strCallsPath), self.lstSampleIndicesToProcess, stSNPs)
        else:
            self.fCalls = None
        if strConfidencesPath is not None:
            self.fConfidences = FilteringCallsFile(open(strConfidencesPath), self.lstSampleIndicesToProcess, stSNPs)
        else:
            self.fConfidences = None
        if strGuidePath is None:
            self.fGuide = None
        elif self.lstSampleIndicesToProcess is None:
            self.fGuide = open(strGuidePath)
        else:
            self.fGuide = FilteringGuideFile(open(strGuidePath), self.lstSampleIndicesToProcess)
        return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--samples', dest='sampleFilePath', help='File containing subset of samples to be included in the output.\n                      File should contain one sample per line.\n                      Default is to use all samples in the call and confidence files.')
    parser.add_option('--snps', dest='snpFilePath', help="File containing subset of SNPS to be included in the output.\n                      File should contain one snp name per line in the first column.\n                      The file can optionally contain a header with 'probeset_id' in the first line.\n                      Default is to use all snps in the call and confidence files.")
    parser.add_option('--in-calls', dest='inCallsPath', help='Input calls file to be filtered.  Default: Do not write an output calls file.')
    parser.add_option('--in-confidences', dest='inConfidencesPath', help='Input confidences file to be filtered.  Default: Do not write an output confidences file.')
    parser.add_option('--in-guide', dest='inGuidePath', help='File containing the NA number (one per line) for each cel file\n                      in the input calls and confidences file.  The number of lines in the guide file\n                      must equal the number of cel files in these files.  If this file is present,\n                      it is filtered according to the --samples file.')
    parser.add_option('--out-calls', dest='outCallsPath', help='Output calls file.  This is required if --in-calls is specified.')
    parser.add_option('--out-confidences', dest='outConfidencesPath', help='Output confidences file.  This is required if --in-confidences is specified.')
    parser.add_option('--out-guide', dest='outGuidePath', help='Output guide file.   This is required if --in-guide is specified.')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) > 1:
        print >> sys.stderr, 'ERROR: Extra arguments on command line.\n'
        parser.print_help()
        return 1
    if not dctOptions.snpFilePath and not dctOptions.sampleFilePath:
        print >> sys.stderr, 'ERROR: Neither --snps nor --samples specified.  No filtering to be done.\n'
        parser.print_help()
        return 1
    factory = FilteringCallsAndConfidencesFileFactory(dctOptions.inCallsPath, dctOptions.inConfidencesPath, dctOptions.inGuidePath, dctOptions.sampleFilePath, dctOptions.snpFilePath)
    if factory.fCalls is not None:
        if dctOptions.outCallsPath is None:
            print >> sys.stderr, 'ERROR: If --in-calls is specified, --out-calls is required.\n'
            parser.print_help()
            return 1
        fOut = open(dctOptions.outCallsPath, 'w')
        for strLine in factory.fCalls:
            fOut.write(strLine)

        fOut.close()
    if factory.fConfidences is not None:
        if dctOptions.outConfidencesPath is None:
            print >> sys.stderr, 'ERROR: If --in-confidences is specified, --out-confidences is required.\n'
            parser.print_help()
            return 1
        fOut = open(dctOptions.outConfidencesPath, 'w')
        for strLine in factory.fConfidences:
            fOut.write(strLine)

        fOut.close()
    if factory.fGuide is not None:
        if dctOptions.outGuidePath is None:
            print >> sys.stderr, 'ERROR: If --in-guide is specified, --out-guide is required.\n'
            parser.print_help()
            return 1
        fOut = open(dctOptions.outGuidePath, 'w')
        for strLine in factory.fGuide:
            fOut.write(strLine)

        fOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())