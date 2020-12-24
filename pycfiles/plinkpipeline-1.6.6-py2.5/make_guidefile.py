# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/make_guidefile.py
# Compiled at: 2010-07-13 12:32:47
"""usage %prog [options]
Make a guide file from a cel_map file mapping a cel file to a sample name,
and a  list of celFiles in a calls file.
"""
from __future__ import division
import optparse, sys, string
from mpgutils import utils
lstRequiredOptions = [
 'pedigree', 'output', 'celMap']

def getCelsForCallsFile(callFile):
    """Parse the calls or confidence file, returning the list of cel names"""
    fIn = open(callFile, 'rU')
    line = fIn.readline()
    s = line.split()
    lstCells = s[1:]
    fIn.close()
    return lstCells


def getCelMap(celMapFile):
    """Parse a file that has the cel name in col 1, and the sample name in col 2, and return a dictionary."""
    fIn = open(celMapFile, 'rU')
    lstTmp = []
    for strLine in fIn:
        s = strLine.split()
        lstTmp.append(s)

    dctCelSample = dict(lstTmp)
    fIn.close()
    return dctCelSample


def buildGuideFile(celList, dctCelSample, outFile):
    fOut = open(outFile, 'w')
    for c in celList:
        try:
            s = dctCelSample[c]
        except KeyError:
            print 'Cel file ' + c + ' had no entry in celMap'
            s = None

        fOut.write(s + '\n')

    fOut.close()
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--celMap', default=None, help='(Required) File with two columns in tab seperated format:\n                      CEL_NAME and SAMPLE_NAME.  This file maps one or more cel names to a sample name.')
    parser.add_option('-c', '--calls', default=None, help='(option) A calls or confidence file in traditional apt-probeset-genotype format.')
    parser.add_option('-o', '--output', default=None, help='(Required) Output calls file in tped (transposed ped) format')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    lstRequiredOptions = ['calls', 'celMap', 'output']
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    celList = getCelsForCallsFile(dctOptions.calls)
    dctCelSample = getCelMap(dctOptions.celMap)
    buildGuideFile(celList, dctCelSample, dctOptions.output)
    return


if __name__ == '__main__':
    sys.exit(main())