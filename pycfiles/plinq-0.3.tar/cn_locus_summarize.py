# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/cn_locus_summarize.py
# Compiled at: 2010-07-13 12:32:46
__doc__ = '%prog [-o outputfile] <allele_summary>\n\nRead the allele summary file as produced by cel2cn_allele.py, and write a locus summary file.\nFor CN probes, the output is the same as the input.  For SNP probes, the A and B allele summaries are\naveraged.\n'
from __future__ import division
import optparse, sys
from mpgutils import fk_utils
iPROBESET_ID_FIELD = 0
iCHROMOSOME_FIELD = 1
iPOSITION_FIELD = 2
iPROBESET_TYPE_FIELD = 3
iFIRST_INTENSITY_FIELD = 4

def summariesAlleles(strALine, strBLine, missingValueLabel):
    lstAFields = strALine.split()
    lstBFields = strBLine.split()
    missingDataIndexA = idx = fk_utils.indices(lstAFields, missingValueLabel)
    missingDataIndexB = idx = fk_utils.indices(lstBFields, missingValueLabel)
    if lstAFields[iCHROMOSOME_FIELD] != lstBFields[iCHROMOSOME_FIELD] or lstAFields[iPOSITION_FIELD] != lstBFields[iPOSITION_FIELD] or len(lstAFields) != len(lstBFields):
        raise Exception('A and B allele lines do not match: ' + strALine + strBLine)
    if not lstAFields[iPROBESET_ID_FIELD].endswith('-A'):
        raise Exception('A allele line has strange probeset id: ' + strALine)
    if not lstBFields[iPROBESET_ID_FIELD].endswith('-B'):
        raise Exception('B allele line has strange probeset id: ' + strBLine)
    lstAFields[iPROBESET_ID_FIELD] = lstAFields[iPROBESET_ID_FIELD][:-2]
    if lstAFields[iPROBESET_ID_FIELD] != lstBFields[iPROBESET_ID_FIELD][:-2]:
        raise Exception('A and B allele lines do not match: ' + strALine + strBLine)
    lstOutFields = lstAFields[iPROBESET_ID_FIELD:iPOSITION_FIELD + 1] + ['S'] + [
     None] * (len(lstAFields) - iFIRST_INTENSITY_FIELD)
    for i in xrange(iFIRST_INTENSITY_FIELD, len(lstAFields)):
        lstOutFields[i] = '%.2f' % ((float(lstAFields[i]) + float(lstBFields[i])) / 2)

    if len(missingDataIndexA) > 0:
        for i in missingDataIndexA:
            lstOutFields[i] = missingValueLabel

    if len(missingDataIndexB) > 0:
        for i in missingDataIndexB:
            lstOutFields[i] = missingValueLabel

    return ('\t').join(lstOutFields) + '\n'


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--output', dest='output', help='Where to write output.  Default: stdout')
    parser.add_option('-f', '--force_cn_summarization', dest='force', default=False, action='store_true', help='Force summarization of CN probes if they have an A and B allele.')
    parser.add_option('-m', '--missing_value_label', dest='missingValueLabel', default='NaN', help='Label of data that is missing from the platform.  \n                      Illumina products do not always have data available for every probe/individual combination.\n                      Default is %default')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    missingValueLabel = dctOptions.missingValueLabel
    if len(lstArgs) == 1:
        print >> sys.stderr, 'ERROR: allele summary file not specified.\n'
        parser.print_help()
        return 1
    if len(lstArgs) > 2:
        print >> sys.stderr, 'ERROR: Too many files on command line.\n'
        parser.print_help()
        return 1
    fIn = open(lstArgs[1])
    force = dctOptions.force
    if dctOptions.output is not None:
        fOut = open(dctOptions.output, 'w')
    else:
        fOut = sys.stdout
    strALine = None
    for strLine in fIn:
        if strLine.startswith('#') or strLine.startswith('probeset_id'):
            fOut.write(strLine)
        else:
            lstFields = strLine.split('\t', 4)
            if force and lstFields[iPROBESET_TYPE_FIELD] == 'C':
                if strALine is None:
                    strALine = strLine
                else:
                    strBLine = strLine
                    fOut.write(summariesAlleles(strALine, strLine))
                    strALine = None
            elif lstFields[iPROBESET_TYPE_FIELD] == 'C':
                fOut.write(strLine)
            elif lstFields[iPROBESET_TYPE_FIELD] == 'A':
                strALine = strLine
            else:
                if lstFields[iPROBESET_TYPE_FIELD] != 'B':
                    raise Exception('Strange value in probeset_type column for line: ' + strLine)
                fOut.write(summariesAlleles(strALine, strLine, missingValueLabel))
                strALine = None

    if strALine is not None:
        raise Exception('File ends with A allele line.')
    fOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())