# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/GenerateAllCallsFile.py
# Compiled at: 2010-10-12 17:55:40
"""
This script generates a File with all calls in all positions in the experiment
"""
from __future__ import division
from optparse import OptionParser
import sys, re, numpy
from string import *
from SAMpileuphelper import *
import os

def main(argv=None):
    if not argv:
        argv = sys.argv
    usage = 'usage: %prog [options] '
    parser = OptionParser(usage)
    parser.add_option('-f', '--force', action='store_true', dest='force', default=False, help='proceed even with bad extensions')
    parser.add_option('--pif')
    parser.add_option('--bqthr')
    parser.add_option('--chr')
    parser.add_option('--hg')
    parser.add_option('--tgf')
    parser.add_option('--samtoolspath')
    parser.add_option('--skipannot')
    parser.add_option('--ref')
    parser.add_option('--module')
    parser.add_option('--sndb')
    parser.add_option('--ncpu')
    parser.add_option('--dbsnp')
    parser.add_option('--outputdir')
    parser.add_option('--outcalls', default='PooledExperiment.allpositions')
    (options, args) = parser.parse_args()
    if not options.force:
        snpsdetected = {}
        pathname = os.path.join(options.outputdir, str(options.outcalls))
        outwritefile = open(pathname, 'w')
        id = 0
        snpcallsdict = {}
        outwritefile.write('pool chr:offset ref_base A C G T D I sum AR CR GR TR DR IR sumr allele1 allele2 combined_sum fwd_lod rev_lod combined_lod flag fisher-pval\n')
        poolfile = open(options.pif, 'r')
        poolfile = poolfile.readlines()
        for linef in poolfile[1:]:
            linef = linef.rstrip()
            linef = linef.split()
            fname = linef[0] + str('.combined.error.coverage.calls')
            filenamer = open(fname, 'r')
            fnamelist = fname.split('.')
            filenameread = filenamer.readlines()
            for line in filenameread[1:]:
                line = line.rstrip()
                line = line.split()
                outwritefile.write(str(fnamelist[0]) + ' ')
                for j in line:
                    outwritefile.write(str(j) + ' ')

                outwritefile.write('\n')

            outwritefile.write('\n\n')


if __name__ == '__main__':
    main()