# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/GenerateCIFFile.py
# Compiled at: 2010-10-12 17:55:40
from __future__ import division
from optparse import OptionParser
import array, sys, re
from SAMpileuphelper import *
import os

def main(argv=None):
    if not argv:
        argv = sys.argv
    usage = 'usage: %prog [options] '
    parser = OptionParser(usage)
    parser.add_option('-f', '--force', action='store_true', dest='force', default=False, help='proceed even with bad extensions')
    parser.add_option('--tgf', default='na')
    parser.add_option('--samtoolspath')
    parser.add_option('--hg')
    parser.add_option('--ref')
    parser.add_option('--pif')
    parser.add_option('--dbsnp')
    parser.add_option('--ncpu')
    parser.add_option('--bqthr')
    parser.add_option('--sndb')
    parser.add_option('--skipannot')
    parser.add_option('--mqthr')
    parser.add_option('--chr', default='T')
    parser.add_option('--outputdir')
    (options, args) = parser.parse_args()
    if not options.force:
        exonf = open(options.tgf, 'r')
        exonf = exonf.readlines()
        pathname = os.path.join(options.outputdir, str(options.tgf) + '.cif')
        print pathname
        print '\n'
        summarywriteexon = open(pathname, 'w')
        for exonline in exonf[1:]:
            exonline = exonline.split()
            target = exonline[0]
            chrom = exonline[1]
            if options.chr == 'T':
                if 'chr' in chrom:
                    chr = chrom
                else:
                    chr = 'chr' + str(chrom)
            elif 'chr' in chrom:
                chr = chrom
                chr = chr.replace('chr', '')
            else:
                chr = chrom
            start = int(exonline[2])
            stop = int(exonline[3])
            size = int(exonline[4])
            if start < stop:
                beg = start - 5
                end = stop + 5
            elif stop < start:
                beg = stop - 5
                end = start + 5
            rangelist = r.seq(beg, end, 1)
            for pos in rangelist:
                summarywriteexon.write(str(chr) + ' ' + str(pos) + '\n')


if __name__ == '__main__':
    main()