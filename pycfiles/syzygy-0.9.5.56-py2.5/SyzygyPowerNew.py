# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/SyzygyPowerNew.py
# Compiled at: 2010-10-12 17:55:40
from __future__ import division
from optparse import OptionParser
import array, numpy, math, sys, re, rpy2
from rpy2.rpy_classic import *
from SAMpileuphelper import *
import pp, time, os
from os import popen
import statslib

def main(argv=None):
    if not argv:
        argv = sys.argv
    usage = 'usage: %prog [options] '
    parser = OptionParser(usage)
    parser.add_option('-f', '--force', action='store_true', dest='force', default=False, help='proceed even with bad extensions')
    parser.add_option('--pif')
    parser.add_option('--hg')
    parser.add_option('--tgf')
    parser.add_option('--samtoolspath')
    parser.add_option('--ref')
    parser.add_option('--sndb')
    parser.add_option('--ncpu')
    parser.add_option('--dbsnp')
    parser.add_option('--out', default='PooledExperiment.pf')
    parser.add_option('--outputdir')
    (options, args) = parser.parse_args()
    if not options.force:
        set_default_mode(BASIC_CONVERSION)
        ppservers = ()
        ncpus = int(options.ncpu)
        job_server = pp.Server(ncpus, ppservers=ppservers)
        jobs = []
        powerdict = {}
        exonfile = options.tgf
        exonf = open(exonfile, 'r')
        exonf = exonf.readlines()
        poolfile = open(options.pif, 'r')
        poolfile = poolfile.readlines()
        poollist = []
        for linef in poolfile[1:]:
            linef = linef.rstrip()
            linef = linef.split()
            poolbam = linef[0]
            poollist.append(poolbam)
            phenotype = int(linef[1])
            inds = int(linef[2])
            chromosomes = int(linef[3])
            inputefile = str(poolbam) + '.combined.error.coverage'
            jobs.append(job_server.submit(statslib.EvaluatePower, (inputefile, exonfile, chromosomes, powerdict), (), ('math',
                                                                                                                       'numpy',
                                                                                                                       'rpy2.rpy_classic',
                                                                                                                       '__future__',
                                                                                                                       'rpy2',
                                                                                                                       'statslib')))

        start_time = time.time()
        for job in jobs:
            result = job()
            for key in result.keys():
                powerdict[key] = result[key]

        print 'Time elapsed: ', time.time() - start_time, 's'
        job_server.print_stats()
        summaryf = options.out
        summarywriteexon = open(summaryf, 'w')
        summarywriteexon.write('chr:offset target_id ')
        for pool in poollist:
            summarywriteexon.write(str(pool) + ' ')

        summarywriteexon.write('\n')
        for exonline in exonf[1:]:
            exonline = exonline.split()
            target = exonline[0]
            chr = exonline[1]
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
                if 'chr' in chr:
                    chroffset = str(chr) + ':' + str(pos)
                else:
                    chroffset = 'chr' + str(chr) + ':' + str(pos)
                summarywriteexon.write(str(chroffset) + ' ' + str(target) + ' ')
                for pool in poollist:
                    errorfile = pool + '.combined.error.coverage'
                    summarywriteexon.write('%4.4g ' % float(powerdict[(errorfile, chroffset)]))

                summarywriteexon.write('\n')


if __name__ == '__main__':
    main()