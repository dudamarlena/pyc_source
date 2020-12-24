# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/segregate_probes_in_cnvs.py
# Compiled at: 2008-12-08 17:00:29
"""usage %prog [options]"""
from __future__ import division
import optparse, sys, cnv_definition_collection
from mpgutils import utils
lstRequiredOptions = [
 'probes_in_cnvs', 'cnv_defs', 'probes_not_in_cnvs', 'probe_locus']

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-i', '--input', help='(Required)  List of probes to be divided into two groups.')
    parser.add_option('-c', '--cnv_defs', help='(Required)  CNV definitions file.  Must be relative to same genome build as birdseye calls.')
    parser.add_option('--probe_locus', help='(Required)  List of SNP and CN probe locations, sorted by chromosome and position.\nThis is used to determine how many probes are encompassed by a Birdseye or Canary call.\nMust be relative to same genome build as birdseye calls.')
    parser.add_option('--probes_in_cnvs', help='(Required)  Probes from input that are in a cnv are written to this file.')
    parser.add_option('--probes_not_in_cnvs', help='(Required)  Probes from input that are not in a cnv are written to this file.')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    cnvDefs = cnv_definition_collection.CNVDefinitionCollection(dctOptions.cnv_defs)
    dctProbeLocus = utils.loadProbeLocus(dctOptions.probe_locus)
    fInCNV = open(dctOptions.probes_in_cnvs, 'w')
    fNotInCNV = open(dctOptions.probes_not_in_cnvs, 'w')
    for lstFields in utils.iterateWhitespaceDelimitedFile(dctOptions.input, iNumFieldsExpected=1):
        strProbe = lstFields[0]
        try:
            (strChr, iPosn) = dctProbeLocus[strProbe]
        except KeyError:
            print >> fNotInCNV, strProbe
            continue

        if len(cnvDefs.getCNVsForLocus(strChr, iPosn)) > 0:
            print >> fInCNV, strProbe
        else:
            print >> fNotInCNV, strProbe

    fInCNV.close()
    fNotInCNV.close()
    return


if __name__ == '__main__':
    sys.exit(main())