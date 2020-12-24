# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/cn_select_autosomal_probes_for_normalization.py
# Compiled at: 2010-07-13 12:32:47
"""usage: %prog --cnv-probe-info <cnv-file> --snp-probe-info <snp-file> --num-probes <number>

Randomly select some autosomal probes from the probes specified in the input files.
The probe names are written to stdout.
"""
from __future__ import division
import optparse, random, sys, cn_annotate_allele_summary

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--cnv-probe-info', dest='cnvProbeInfo', help='Input file containing metadata for CNV probes.')
    parser.add_option('--snp-probe-info', dest='snpProbeInfo', help='Input file containing metadata for SNP probe sets.')
    parser.add_option('--num-probes', dest='numProbes', type='int', help='The number of probes to select')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if dctOptions.snpProbeInfo is None or dctOptions.cnvProbeInfo is None or dctOptions.numProbes is None:
        print >> sys.stderr, 'ERROR: Arguments --snp-probe-info, --cnv-probe-info and --num-probes must be specified.\n'
        parser.print_help()
        return 1
    dctProbeToGenomicPosition = {}
    cn_annotate_allele_summary.mapCNPs(dctProbeToGenomicPosition, dctOptions.cnvProbeInfo)
    cn_annotate_allele_summary.mapSNPs(dctProbeToGenomicPosition, dctOptions.snpProbeInfo)
    lstAutosomalProbes = [ strProbeName for (strProbeName, tupLocus) in dctProbeToGenomicPosition.iteritems() if strProbeName.startswith('CN_') if tupLocus[0] not in ('23',
                                                                                                                                                                       '24')
                         ]
    lstAutosomalProbes.sort()
    for strProbe in random.sample(lstAutosomalProbes, dctOptions.numProbes):
        print strProbe

    return


if __name__ == '__main__':
    sys.exit(main())