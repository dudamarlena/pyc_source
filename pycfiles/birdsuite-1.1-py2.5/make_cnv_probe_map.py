# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/birdsuite/make_cnv_probe_map.py
# Compiled at: 2009-01-27 09:42:05
"""usage %prog [options]

Create an output file that maps each probe to the CNV it resides in.  Probes that are not in a CNV are not written."""
from __future__ import division
import optparse, sys, cnv_definition_collection
from mpgutils import utils
lstRequiredOptions = [
 'cnv_defs', 'probe_locus']

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--output', help='Where to write output.  Default: stdout')
    parser.add_option('-c', '--cnv_defs', help='(Required)  CNV definitions file.  Must be relative to same genome build as probe_locus file.')
    parser.add_option('--probe_locus', help='(Required)  List of SNP and CN probe locations.\nMust be relative to same genome build as cnv_defs file.')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    cnvDefs = cnv_definition_collection.CNVDefinitionCollection(dctOptions.cnv_defs)
    dctProbeLocus = utils.loadProbeLocus(dctOptions.probe_locus)
    if dctOptions.output is None:
        fOut = sys.stdout
    else:
        fOut = open(dctOptions.output, 'w')
    for lstFields in utils.iterateWhitespaceDelimitedFile(dctOptions.probe_locus, iNumFieldsExpected=3):
        strSNP = lstFields[0]
        strChr = utils.convertChromosomeStr(lstFields[1])
        iPosn = int(lstFields[2])
        stCNVs = cnvDefs.getCNVsForLocus(strChr, iPosn)
        for cnv in stCNVs:
            print >> fOut, cnv.strCNVName, strSNP

    if dctOptions.output is not None:
        fOut.close()
    return


if __name__ == '__main__':
    sys.exit(main())