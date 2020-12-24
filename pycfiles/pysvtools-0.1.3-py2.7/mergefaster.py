# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pysvtools/mergefaster.py
# Compiled at: 2015-11-16 11:28:45
from __future__ import print_function
__desc__ = '\n    Merging procedure for Structural Variation events.\n    Follows the idea of centerpoint matching to allow flexible match vs. reciprocal overlap.\n'
__author__ = 'Wai Yi Leung <w.y.leung@lumc.nl>'
import argparse, collections, itertools
from natsort import natsorted
import logging, os, sys
try:
    import vcf
except:
    print('No PyVCF installation was found, please install with:\n\tpip install pyvcf')
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from pysvtools.models import Event, ExclusionRegion
from pysvtools.utils import extractTXmate, extractDPFromRecord, getSVType, getSVLEN, formatBedTrack, formatVCFRecord, vcfHeader, build_exclusion

class VCFEventLoader(object):
    """
        Load VCF File and transform VCF record into an `Event`
    """

    def __init__(self):
        pass


class SVMerger(object):

    def __init__(self):
        pass


class ReportExport(object):

    def __init__(self):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--exclusion_regions', action='append', help='Exclusion regions file in BED format')
    parser.add_argument('-f', '--flanking', type=int, help='Centerpoint flanking [100]', default=100)
    parser.add_argument('-s', '--sizeflanking', type=int, help='Size Deviation [50]', default=50)
    parser.add_argument('-t', '--translocation_only', action='store_true', help='Do translocations only', required=False, default=False)
    parser.add_argument('-i', '--vcf', nargs='+', help='The VCF(s) to compare, can be supplied multiple times')
    parser.add_argument('-o', '--output', help='Output summary to [sample.tsv]', default='sample.tsv')
    parser.add_argument('-b', '--bedoutput', help='Output bed file to [sample.bed]', default='sample.bed')
    parser.add_argument('-v', '--vcfoutput', help='Output summary to [sample.vcf]', default='sample.vcf')
    parser.add_argument('-r', '--regions_out', help='Output all regions to [regions_out.bed]', default='regions_out.bed')
    args = parser.parse_args()
    if args.vcf == None or len(args.vcf) < 2:
        logger.error('Please supply at least 2 VCF files to merge')
        sys.exit(1)
    startMerge(args.vcf, args.exclusion_regions, args.output, args.flanking, args.bedoutput, args.translocation_only, args.regions_out, args.vcfoutput)
    return


if __name__ == '__main__':
    main()