# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/mendel_errors_by_chromosome.py
# Compiled at: 2010-07-13 12:32:47
"""usage %prog --mendel input-mendel-file --probe-locus input-probe-locus-file --probes probe-list-file [--output outfile]

Tabulate Mendel errors by sample and chromosome.
"""
from __future__ import division
import optparse, sys
from mpgutils import utils
lstRequiredOptions = [
 'mendel', 'probe_locus', 'probes']

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-m', '--mendel', help='(Required) .mendel file produced by mendel_check.py.')
    parser.add_option('--probe_locus', help='(Required)  List of probe locations.')
    parser.add_option('--probes', help='(Required)  List of all probes of the type being counted.')
    parser.add_option('-o', '--output', help='Where to write output.  Default: stdout')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    if dctOptions.output is not None:
        fOut = open(dctOptions.output, 'w')
    else:
        fOut = sys.stdout
    dctProbeLocus = utils.loadProbeLocus(dctOptions.probe_locus)
    lstProbesPerChromosome = [
     0] * (utils.iNUM_CHROMOSOMES + 1)
    for (strProbe,) in utils.iterateWhitespaceDelimitedFile(dctOptions.probes, iNumFieldsExpected=1):
        try:
            (strChromosome, iPosition) = dctProbeLocus[strProbe]
            iChromosome = int(strChromosome)
        except KeyError:
            iChromosome = 0

        lstProbesPerChromosome[iChromosome] += 1

    dctErrorsBySampleAndChromosome = {}
    lstErrorsByChromosome = [
     0] * (utils.iNUM_CHROMOSOMES + 1)
    for lstFields in utils.iterateWhitespaceDelimitedFile(dctOptions.mendel, bSkipHeader=True):
        tupSample = tuple(lstFields[:2])
        strProbe = lstFields[2]
        (strChromosome, iPosn) = dctProbeLocus.get(strProbe, (0, 0))
        iChromosome = int(strChromosome)
        lstErrorsByChromosome[iChromosome] += 1
        try:
            lstForSample = dctErrorsBySampleAndChromosome[tupSample]
        except KeyError:
            lstForSample = [
             0] * (utils.iNUM_CHROMOSOMES + 1)
            dctErrorsBySampleAndChromosome[tupSample] = lstForSample

        lstForSample[iChromosome] += 1

    lstHeaders = ['FID', 'KID'] + [ str(val) for val in xrange(utils.iNUM_CHROMOSOMES + 1) ]
    print >> fOut, ('\t').join(lstHeaders)
    lstTotals = ['Totals', '0'] + [ '%.5f' % (100 * float(lstErrorsByChromosome[i]) / lstProbesPerChromosome[i]) for i in xrange(len(lstErrorsByChromosome)) ]
    print >> fOut, ('\t').join(lstTotals)
    lstKeys = dctErrorsBySampleAndChromosome.keys()
    lstKeys.sort()
    for tupKey in lstKeys:
        lstForSample = dctErrorsBySampleAndChromosome[tupKey]
        lstFields = list(tupKey) + [ '%.5f' % (100 * float(lstForSample[i]) / lstProbesPerChromosome[i]) for i in xrange(len(lstForSample)) ]
        print >> fOut, ('\t').join(lstFields)

    if dctOptions.output is not None:
        fOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())