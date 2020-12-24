# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hapmap3/sangerFormat_to_annotatedSummary.py
# Compiled at: 2009-01-27 09:42:00
"""%prog [-o outputfile ] <sanger format intensity data>

Read the sanger format intensity files as produced by extract_intensity_sanger_format (or by sanger themselves),
and create our default annotated summary format.  This has the ability to concatonate a number of files that span 
chromosomes.
"""
from __future__ import division
import optparse, sys
from copy import deepcopy
from mpgutils.fk_utils import arbslice
from mpgutils import fk_utils
iPROBESET_ID_FIELD = 0
iCHROMOSOME_FIELD = 1
iPOSITION_FIELD = 2
iALLELE_FIELD = 3
iFIRST_INTENSITY_FIELD = 4
MISSING_VALUE_LABEL = str(-9999)

def splitIntoAlleleFields(strLine):
    """Splits line into A and B lines.  Returns the info fields (probeset, chr, etc),
    the A probe fields, and the B probe fields."""
    lstFields = strLine.split()
    fieldAIndex = range(iFIRST_INTENSITY_FIELD, len(lstFields), 2)
    fieldBIndex = range(iFIRST_INTENSITY_FIELD + 1, len(lstFields), 2)
    lstAFields = arbslice(lstFields, fieldAIndex)
    lstBFields = arbslice(lstFields, fieldBIndex)
    infoFields = lstFields[:iFIRST_INTENSITY_FIELD]
    return (infoFields, lstAFields, lstBFields)


def getHeader(strLine):
    """Returns the header line"""
    (infoFields, lstAFields, lstBFields) = splitIntoAlleleFields(strLine)
    infoFields[iPROBESET_ID_FIELD] = 'probeset_id'
    infoFields[iCHROMOSOME_FIELD] = 'chr'
    infoFields[iALLELE_FIELD] = 'probeset_type'
    lstFields = [ x[:-2] for x in lstAFields ]
    lstResult = []
    lstResult.extend(infoFields)
    lstResult.extend(lstFields)
    strHeader = ('\t').join(lstResult) + '\n'
    return strHeader


def getLine(strLine, probeAllele, intensityMultiplier, missingValueLabel):
    """Convert 1 line that has A and B intensity info into one lines of output, 
    either the A or B probe depending on which probe allele is requested."""
    setValidProbeAlleles = set(['A', 'B'])
    if probeAllele not in setValidProbeAlleles:
        print >> sys.stderr, "ERROR: You can't use probe allele " + probeAllele
        return 1
    (infoFields, lstAFields, lstBFields) = splitIntoAlleleFields(strLine)
    infoFields[iALLELE_FIELD] = probeAllele
    infoFields[iPROBESET_ID_FIELD] = infoFields[iPROBESET_ID_FIELD] + ('-' + probeAllele)
    lstResult = []
    lstResult.extend(infoFields)
    if probeAllele == 'A':
        lstAFields = modifyIntensitySpace(lstAFields, intensityMultiplier, missingValueLabel)
        lstResult.extend(lstAFields)
    else:
        lstBFields = modifyIntensitySpace(lstBFields, intensityMultiplier, missingValueLabel)
        lstResult.extend(lstBFields)
    strResult = ('\t').join(lstResult) + '\n'
    return strResult


def modifyIntensitySpace(lstIntensity, intensityMultiplier, missingValueLabel):
    strRow = [ str(x) for x in lstIntensity ]
    idxMissingVals = fk_utils.indices(strRow, str(missingValueLabel))
    result = [ float(x) * intensityMultiplier for x in lstIntensity ]
    result = [ str(x) for x in result ]
    if len(idxMissingVals) > 0:
        for i in idxMissingVals:
            result[i] = MISSING_VALUE_LABEL

    return result


def processFile(strFile, fOut, intensityMultiplier, missingValueLabel, boolWriteHeader):
    fIn = open(strFile)
    strLine = None
    for strLine in fIn:
        if strLine.startswith('probe_name') or strLine.startswith('probeset_id'):
            strHeader = getHeader(strLine)
            if boolWriteHeader:
                fOut.write(strHeader)
        elif strLine.startswith('#') == False:
            strAResult = getLine(strLine, 'A', intensityMultiplier, missingValueLabel)
            strBResult = getLine(strLine, 'B', intensityMultiplier, missingValueLabel)
            fOut.write(strAResult)
            fOut.write(strBResult)

    return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--output', dest='output', help='Where to write output.  Default: stdout')
    parser.add_option('-i', '--intensity_multiplier', dest='intensityMultiplier', default=1, help='What to multiply intensity by to make it similar to other data sets. \n                      Defaults to 1 (no change)')
    parser.add_option('-m', '--missing_value_label', dest='missingValueLabel', default='-9999', help='Encode this value in the canonical missing value label (-9999)')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) == 1:
        print >> sys.stderr, 'ERROR: at least one intensity file must be specified.\n'
        parser.print_help()
        return 1
    if dctOptions.output is not None:
        fOut = open(dctOptions.output, 'w')
    else:
        fOut = sys.stdout
    intensityMultiplier = float(dctOptions.intensityMultiplier)
    missingValueLabel = dctOptions.missingValueLabel
    for i in xrange(1, len(lstArgs)):
        strFile = lstArgs[i]
        if i == 1:
            processFile(strFile, fOut, intensityMultiplier, missingValueLabel, True)
        else:
            processFile(strFile, fOut, intensityMultiplier, missingValueLabel, False)

    fOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())