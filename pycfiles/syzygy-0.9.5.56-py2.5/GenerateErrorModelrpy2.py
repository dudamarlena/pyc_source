# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/GenerateErrorModelrpy2.py
# Compiled at: 2010-10-12 17:55:36
from __future__ import division
from optparse import OptionParser
import numpy, re, sys, re
from SAMpileuphelper import *
import datetime, os
space = re.compile('\\s+')
from rpy2.rpy_classic import *

def main(argv=None):
    if not argv:
        argv = sys.argv
    usage = 'usage: %prog [options] '
    parser = OptionParser(usage)
    parser.add_option('-f', '--force', action='store_true', dest='force', default=False, help='proceed even with bad extensions')
    parser.add_option('--dbsnp', default='/seq/dirseq/rivas/Rivasglioma/dbsnp/basepos.snpshg18.dbsnp')
    parser.add_option('--hg')
    parser.add_option('--pif')
    parser.add_option('--bqthr', default=22)
    parser.add_option('--outputdir')
    parser.add_option('--ncpu')
    parser.add_option('--tgf')
    parser.add_option('--samtoolspath')
    parser.add_option('--ref')
    parser.add_option('--window', default=10)
    parser.add_option('--min_window_coverage', default=1000)
    (options, args) = parser.parse_args()
    if not options.force:
        set_default_mode(BASIC_CONVERSION)
        window = options.window
        minimum_coverage = int(options.min_window_coverage)
        dbsnp = {}
        exptchroffsets = {}
        accumcoveragefwd = {}
        accumcoveragerev = {}
        mcratefwd = {}
        mcraterev = {}
        refalleles = {}
        pools = 0
        dbsnpfile = options.dbsnp
        dbsnp = populate_dbsnp_dictionary(dbsnp, dbsnpfile)
        hgbuild = int(options.hg)
        poolnum = 0
        poolfile = open(options.pif, 'r')
        poolfile = poolfile.readlines()
        for linef in poolfile[1:]:
            linef = linef.rstrip()
            linef = linef.split()
            fname = linef[0]
            if '.bam' in fname:
                poolnum += 1

        mcratefwdavgfiles = [
         0] * poolnum
        mcraterevavgfiles = [0] * poolnum
        accumcoveragefwdfiles = [0] * poolnum
        accumcoveragerevfiles = [0] * poolnum
        filenumber = -1
        poolfile = open(options.pif, 'r')
        poolfile = poolfile.readlines()
        for linef in poolfile[1:]:
            linef = linef.rstrip()
            linef = linef.split()
            fname = linef[0]
            fnamer = os.path.join(options.outputdir, str(fname) + '.pileup.' + str(options.bqthr) + 'thresholded.coverage')
            print 'Processing %s ... ' % fnamer
            filenamer = open(fnamer, 'r')
            filenameread = filenamer.readlines()
            filenumber += 1
            pools += 1
            for line in filenameread[1:]:
                line = line.rstrip()
                line = space.split(line)
                chr = line[0].strip()
                if hgbuild == 17:
                    position = int(line[1])
                elif hgbuild == 18:
                    position = int(line[1])
                reference_allele = line[2]
                if reference_allele == 'A':
                    ref_index = 0
                elif reference_allele == 'C':
                    ref_index = 1
                elif reference_allele == 'G':
                    ref_index = 2
                elif reference_allele == 'T':
                    ref_index = 3
                chroffset = line[2].strip()
                ref_allele = line[3].strip()
                ref_index = int(line[4].strip())
                refalleles[chroffset] = ref_allele
                exptchroffsets[chroffset] = chroffset
                allele_counts = returnintlist(line[5:len(line)])
                if chroffset in dbsnp:
                    pass
                else:
                    accumcoveragefwdfiles[filenumber] += sum(returnintlist(line[5:11]))
                    accumcoveragerevfiles[filenumber] += sum(returnintlist(line[11:len(line)]))
                    mcratefwdavgfiles[filenumber] += sum(returnintlist(line[5:11])) - int(allele_counts[ref_index])
                    mcraterevavgfiles[filenumber] += sum(returnintlist(line[11:len(line)])) - int(allele_counts[(ref_index + 6)])
                if chroffset in accumcoveragefwd:
                    accumcoveragefwd[chroffset] += sum(returnintlist(line[5:11]))
                    accumcoveragerev[chroffset] += sum(returnintlist(line[11:len(line)]))
                else:
                    accumcoveragefwd[chroffset] = 0
                    accumcoveragerev[chroffset] = 0
                    accumcoveragefwd[chroffset] += sum(returnintlist(line[5:11]))
                    accumcoveragerev[chroffset] += sum(returnintlist(line[11:len(line)]))
                if chroffset in mcratefwd:
                    mcratefwd[chroffset] += sum(returnintlist(line[5:11])) - int(allele_counts[ref_index])
                    mcraterev[chroffset] += sum(returnintlist(line[11:len(line)])) - int(allele_counts[(ref_index + 6)])
                else:
                    mcratefwd[chroffset] = 0
                    mcraterev[chroffset] = 0
                    mcratefwd[chroffset] += sum(returnintlist(line[5:11])) - int(allele_counts[ref_index])
                    mcraterev[chroffset] += sum(returnintlist(line[11:len(line)])) - int(allele_counts[(ref_index + 6)])

        errormodelmcratefwd = []
        errormodelmcraterev = []
        errormodelnqsfwd = []
        errormodelnqsrev = []
        errormodeltrinucfwd = []
        errormodeltrinucrev = []
        errorcombinednqs = []
        errorcombinedmcrate = []
        allbasenqsfwd = {}
        allbasenqsrev = {}
        allbasetrinucfwd = {}
        allbasetrinucrev = {}
        debug = open('debug.txt', 'w+')
        for key in exptchroffsets:
            (chromosome, pos) = key.split(':')
            neighborsfwd = 0
            neighborsrev = 0
            averageflankfwd = 0
            averageflankrev = 0
            sumflankfwd = []
            sumflankrev = []
            leftint = int(pos) - 1
            rightint = int(pos) + 1
            neighborleftstring = str(chromosome) + ':' + str(leftint)
            neighborrightstring = str(chromosome) + ':' + str(rightint)
            for i in range(1, window + 1):
                neighborbasemin = int(pos) - i
                neighborbaseplus = int(pos) + i
                neighborbaseminstring = str(chromosome) + ':' + str(neighborbasemin)
                neighborbaseplusstring = str(chromosome) + ':' + str(neighborbaseplus)
                if neighborbaseminstring in accumcoveragefwd and accumcoveragefwd[neighborbaseminstring] > 0:
                    neighborsfwd += 1
                    sumflankfwd.append(accumcoveragefwd[neighborbaseminstring] / int(pools))
                if neighborbaseplusstring in accumcoveragefwd and accumcoveragefwd[neighborbaseplusstring] > 0:
                    neighborsfwd += 1
                    sumflankfwd.append(accumcoveragefwd[neighborbaseplusstring] / int(pools))
                if neighborbaseminstring in accumcoveragerev and accumcoveragerev[neighborbaseminstring] > 0:
                    neighborsrev += 1
                    sumflankrev.append(accumcoveragerev[neighborbaseminstring] / int(pools))
                if neighborbaseplusstring in accumcoveragerev and accumcoveragerev[neighborbaseplusstring] > 0:
                    neighborsrev += 1
                    sumflankrev.append(accumcoveragerev[neighborbaseplusstring] / int(pools))

            if neighborsfwd > 0 and neighborsrev > 0 and neighborleftstring in accumcoveragefwd and neighborrightstring in accumcoveragefwd:
                averageflankrev = numpy.median(sumflankrev)
                averageflankfwd = numpy.median(sumflankfwd)
                nqsstat1 = accumcoveragefwd[key] / int(pools) / averageflankfwd
                nqsstat2 = accumcoveragerev[key] / int(pools) / averageflankrev
                allbasenqsfwd[key] = nqsstat1
                allbasenqsrev[key] = nqsstat2
                trinucfwd = refalleles[neighborleftstring] + refalleles[key] + refalleles[neighborrightstring]
                trinucrev = reverse_complement(trinucfwd)
                allbasetrinucfwd[key] = trinucfwd
                allbasetrinucrev[key] = trinucrev
                if key in dbsnp:
                    pass
                elif accumcoveragefwd[key] > minimum_coverage and accumcoveragerev[key] > minimum_coverage and nqsstat1 > 0.2 and nqsstat1 <= 1.5 and nqsstat2 > 0.2 and nqsstat2 <= 1.5:
                    errormodeltrinucfwd.append(trinucfwd)
                    errormodeltrinucrev.append(trinucrev)
                    errormodelnqsfwd.append(nqsstat1)
                    errormodelnqsrev.append(nqsstat2)
                    debug.write(str(key) + ' ' + str(mcratefwd[key]) + ' ' + str(accumcoveragefwd[key]) + '\n')
                    errormodelmcratefwd.append(mcratefwd[key] / accumcoveragefwd[key])
                    errormodelmcraterev.append(mcraterev[key] / accumcoveragerev[key])

        errorcombinednqs = errormodelnqsfwd + errormodelnqsrev
        errorcombinedtrinuc = errormodeltrinucfwd + errormodeltrinucrev
        errorcombinedmcrate = errormodelmcratefwd + errormodelmcraterev
        errorcombinedtrinucfit = [ errorcombinedtrinuc[i] for i in range(0, len(errorcombinedtrinuc)) if errorcombinedmcrate[i] < 0.01 ]
        errorcombinednqsfit = [ errorcombinednqs[i] for i in range(0, len(errorcombinednqs)) if errorcombinedmcrate[i] < 0.01 ]
        errorcombinedmcratefit = [ errorcombinedmcrate[i] for i in range(0, len(errorcombinedmcrate)) if errorcombinedmcrate[i] < 0.01 ]
        r.png(file=os.path.join(options.outputdir, 'error.model.pooledexperiment%03d.png'))
        r.plot(errorcombinednqsfit, errorcombinedmcratefit, main='NLS Fit @ Min Cov: %s Window: %s' % (minimum_coverage, window), xlab='NQS', xlim=r.c(0, 2), ylim=r.c(0, 1), ylab='Miscall Rate')
        r.plot(errorcombinednqsfit, errorcombinedmcratefit, main='NLS Fit @ Min Cov: %s Window: %s' % (minimum_coverage, window), xlab='NQS', xlim=r.c(0, 2), ylim=r.c(0, 0.1), ylab='Miscall Rate')
        r.plot(errorcombinednqsfit, errorcombinedmcratefit, main='NLS Fit @ Min Cov: %s Window: %s' % (minimum_coverage, window), xlab='NQS', xlim=r.c(0, 2), ylim=r.c(0, 0.01), ylab='Miscall Rate')
        import rpy2.robjects as robjects
        ydata = robjects.FloatVector(errorcombinedmcratefit)
        xdata = robjects.FloatVector(errorcombinednqsfit)
        robjects.globalEnv['y'] = ydata
        robjects.globalEnv['x'] = xdata
        model = robjects.r.nls('y~a*x^3 + b*x^2 + c*x + d', start=robjects.r.list(a=0, b=0, c=0, d=0))
        fittedpoints = list(model.r['m'][0].r['fitted'][0]())
        r.points(errorcombinednqsfit, fittedpoints, col=r.c('blue'), pch=19)
        functionalfit = model.r['m'][0].r['getAllPars'][0]()
        residualerrorpoints = [ errorcombinedmcratefit[i] - fittedpoints[i] for i in range(0, len(errorcombinedmcratefit)) ]
        xdata = robjects.StrVector(errorcombinedtrinucfit)
        ydata = robjects.FloatVector(residualerrorpoints)
        robjects.globalEnv['yt'] = ydata
        robjects.globalEnv['xt'] = xdata
        modelresidual = robjects.r.lm('yt ~ 0 + xt')
        modelresidualfit = modelresidual.r['coefficients']
        r.dev_off()
    filenumout = -1
    poolfile = open(options.pif, 'r')
    poolfile = poolfile.readlines()
    for linef in poolfile[1:]:
        linef = linef.rstrip()
        linef = linef.split()
        fname = linef[0]
        fileoutput = os.path.join(options.outputdir, fname + '.combined.error.coverage')
        filenumout += 1
        poolerrorfwd = mcratefwdavgfiles[filenumout] / accumcoveragefwdfiles[filenumout]
        poolerrorrev = mcraterevavgfiles[filenumout] / accumcoveragerevfiles[filenumout]
        filenamer = os.path.join(options.outputdir, str(fname) + '.pileup.' + str(options.bqthr) + 'thresholded.coverage')
        filenameread = open(filenamer, 'r').readlines()
        outfilename = open(fileoutput, 'w')
        outfilename.write('chr offset loc ref_base ref_idx afwd cfwd gfwd tfwd dfwd ifwd mcratef arev crev grev trev drev irev mcrater' + '\n')
        for line in filenameread[1:]:
            line = line.rstrip()
            line = space.split(line)
            chr = line[0].strip()
            if hgbuild == 17:
                position = int(line[1])
            elif hgbuild == 18:
                position = int(line[1])
            reference_allele = line[2]
            if reference_allele == 'A':
                ref_index = 0
            elif reference_allele == 'C':
                ref_index = 1
            elif reference_allele == 'G':
                ref_index = 2
            elif reference_allele == 'T':
                ref_index = 3
            chroffset = line[2].strip()
            ref_allele = line[3].strip()
            ref_index = int(line[4].strip())
            allele_counts = returnintlist(line[5:len(line)])
            if chroffset in allbasenqsfwd and chroffset in allbasenqsrev and chroffset in allbasetrinucfwd and chroffset in allbasetrinucrev:
                if float(allbasenqsfwd[chroffset]) >= 0.2 and float(allbasenqsfwd[chroffset]) <= 1.7 and float(allbasenqsrev[chroffset]) >= 0.2 and float(allbasenqsrev[chroffset]) <= 1.7:
                    errorfwd = functionalfit.r['a'][0] * float(allbasenqsfwd[chroffset]) ** 3 + functionalfit.r['b'][0] * float(allbasenqsfwd[chroffset]) ** 2 + functionalfit.r['c'][0] * float(allbasenqsfwd[chroffset]) + functionalfit.r['d'][0] + float(modelresidualfit.r['coefficients'][0].r[('xt' + str(allbasetrinucfwd[chroffset]))][0])
                    errorrev = functionalfit.r['a'][0] * float(allbasenqsrev[chroffset]) ** 3 + functionalfit.r['b'][0] * float(allbasenqsrev[chroffset]) ** 2 + functionalfit.r['c'][0] * float(allbasenqsrev[chroffset]) + functionalfit.r['d'][0] + float(modelresidualfit.r['coefficients'][0].r[('xt' + str(allbasetrinucrev[chroffset]))][0])
                else:
                    errorfwd = mcratefwdavgfiles[filenumout] / accumcoveragefwdfiles[filenumout]
                    errorrev = mcraterevavgfiles[filenumout] / accumcoveragerevfiles[filenumout]
            else:
                errorfwd = mcratefwdavgfiles[filenumout] / accumcoveragefwdfiles[filenumout]
                errorrev = mcraterevavgfiles[filenumout] / accumcoveragerevfiles[filenumout]
            if errorfwd < 0.001 or errorrev < 0.001:
                if errorfwd < 0.001:
                    errorfwd = max(mcratefwdavgfiles[filenumout] / accumcoveragefwdfiles[filenumout], 0.001)
                if errorrev < 0.001:
                    errorrev = max(mcraterevavgfiles[filenumout] / accumcoveragerevfiles[filenumout], 0.001)
            outfilename.write(str(chr) + ' ' + str(position) + ' ' + str(chroffset) + ' ' + str(ref_allele) + ' ' + str(ref_index) + ' ' + str(allele_counts[0]) + ' ' + str(allele_counts[1]) + ' ' + str(allele_counts[2]) + ' ' + str(allele_counts[3]) + ' ' + str(0) + ' ' + str(0) + ' ' + str(errorfwd) + ' ' + str(allele_counts[6]) + ' ' + str(allele_counts[7]) + ' ' + str(allele_counts[8]) + ' ' + str(allele_counts[9]) + ' ' + str(0) + ' ' + str(0) + ' ' + str(errorrev) + '\n')


if __name__ == '__main__':
    main()