# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/SyzygyWrapperFlannick.py
# Compiled at: 2010-10-12 17:55:40
import GenerateCIFFile, FinalAnnotation, CleanUpSNPCalls, EMFreqAssocStrandNew, CalphaRareTest, runsamtools, runsamtoolsparallel, SAMPileupAnalysis, SAMpileuphelper, GenerateErrorModelrpy2, PlotVisualizations, IndividualPoolSummary, Learn2ndbestIntensity, AnnotateSNP
from mpgutils import utils
from mpgutils.RUtils import RscriptToPython
import runrscript, runrscriptparallel2, SyzygyPower
from optparse import OptionParser
import sys, re, numpy, ParseAnnotation, GenerateSNPCallsFile, GenerateAllCallsFile
from string import *
import pp
from pp import *
import EMFreqAssocStrandFixed

def main(argv=None):
    if not argv:
        argv = sys.argv
    lstRequiredOptions = [
     'tgf', 'pif', 'rarethr', 'samtoolspath', 'hg', 'sndb']
    usage = 'usage: %prog [options] '
    parser = OptionParser(usage)
    parser.add_option('-t', '--tgf', help='Experimental Target File')
    parser.add_option('-i', '--pif', help='Pool/Sample Info File')
    parser.add_option('-r', '--rarethr', help='Frequency Threshold for classifying variant as rare (default = .03)')
    parser.add_option('-g', '--hg', help='Specify Human Genome build being used (Currently 17 or 18)')
    parser.add_option('-s', '--samtoolspath', help='Specify SAMTools Path')
    parser.add_option('-n', '--sndb', help='2nd best base annotation with Quality Scores (true or false)', default='false')
    parser.add_option('-z', '--threaded', help='Allow Threading (default=false)', default='false')
    parser.add_option('-u', '--ncpu', help='Number of CPUs', default=1)
    parser.add_option('-q', '--bqthr', help='Base Quality Threshold (default Q = 22)', default=22)
    parser.add_option('-m', '--mqthr', help='Mapping Quality Threshold (default Q = 1)', default=1)
    parser.add_option('-d', '--dbsnp', help='dbSNP File')
    parser.add_option('-p', '--plots', help='Generates Plots for Error Modeling, Frequency Estimation, Power Computations, and Calpha Diagnostics (true or false)')
    parser.add_option('-b', '--bds', help='Bounds for Calpha Test (default = 5)', default=5)
    parser.add_option('-o', '--outputdir', help='Define directory for output files')
    parser.add_option('-f', '--ref', help='FASTA for Reference Genome')
    parser.add_option('-c', '--cif', help=' Coordinate File for SAMTools (default: generate from target file)', default='')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if dctOptions.dbsnp and dctOptions.pif and dctOptions.hg:
        possible_args = [
         'outputdir', 'pif', 'dbsnp', 'hg']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n---------Cleaning Up SNP Calls---------------------------'
        CleanUpSNPCalls.main(current_args)
    if dctOptions.outputdir and dctOptions.pif:
        possible_args = [
         'outputdir', 'pif']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Frequency and Association Testing-------'
        EMFreqAssocStrandFixed.main(current_args)
    if dctOptions.outputdir and dctOptions.sndb == 'true':
        possible_args = [
         'outputdir', 'sndb']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Running Second Best Base Analysis------'
        Learn2ndbestIntensity.main(current_args)
    if dctOptions.outputdir:
        possible_args = [
         'outputdir']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Generating Final Annotations--------------------'
        FinalAnnotation.main(current_args)
    if dctOptions.outputdir:
        possible_args = [
         'outputdir']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Generating .snpcalls File--------------------'
        GenerateSNPCallsFile.main(current_args)
    if dctOptions.outputdir and dctOptions.pif:
        possible_args = [
         'outputdir', 'pif']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Generating All Calls File--------------------'
        GenerateAllCallsFile.main(current_args)
    if dctOptions.outputdir:
        possible_args = [
         'outputdir']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Creating Pool By Pool Summary ---------------'
        IndividualPoolSummary.main(current_args)
    if dctOptions.outputdir and dctOptions.pif and dctOptions.tgf:
        possible_args = [
         'outputdir', 'pif', 'tgf']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n-------Rare Variant Testing--------------------'
        CalphaRareTest.main(current_args)
    if dctOptions.outputdir:
        possible_args = [
         'outputdir']
        current_args = MakeArguments(possible_args, dctOptions)
        print '\n---------Plotting Power Visualizations---------------------------'
        PlotVisualizations.main(current_args)
    if dctOptions.outputdir and dctOptions.pif:
        piffile = open(dctOptions.pif, 'r').readlines()
        scratchpath = os.path.join(dctOptions.outputdir, 'scratch/')
        resultspath = os.path.join(dctOptions.outputdir, 'results/')
        ensurePathSyzygy(scratchpath)
        ensurePathSyzygy(resultspath)
        for line in piffile[1:]:
            filemove = []
            line = line.rstrip()
            line = line.split()
            pool = line[0]
            filemove.append(str(pool) + '.pileup')
            filemove.append(str(pool) + '.pileup.' + str(dctOptions.bqthr) + 'thresholded.coverage')
            filemove.append(str(pool) + '.combined.error.coverage')
            filemove.append(str(pool) + '.combined.error.coverage.calls')
            filemove.append(str(pool) + '.pileup' + str(dctOptions.bqthr) + '.r.miscallrate.plots001.pdf')
            filemove.append(str(pool) + '.pileup' + '.bq' + str(dctOptions.bqthr) + '.mq' + str(dctOptions.mqthr) + '.bes')
            filemove.append(str(pool) + '.pileup' + str(dctOptions.bqthr) + '.r' + '.miscallrate.' + 'plots001.png')
            filemove.append(str(pool) + '.pileup' + str(dctOptions.bqthr) + '.r' + '.miscallrate.' + 'plots002.png')
            filemove.append(str(pool) + '.pileup' + str(dctOptions.bqthr) + '.r' + '.miscallrate.' + 'plots003.png')
            filemove.append('error.model.pooledexperiment001.png')
            filemove.append('error.model.pooledexperiment002.png')
            filemove.append('error.model.pooledexperiment003.png')
            filemove.append(str(dctOptions.tgf) + '.cif')
            for src in filemove:
                srcpath = os.path.join(dctOptions.outputdir, src)
                if os.path.exists(srcpath):
                    last_part = os.path.split(src)[1]
                    os.rename(srcpath, os.path.join(scratchpath, last_part))

        filemove = []
        filemove.append('miscallrate.universal.' + str(dctOptions.bqthr) + '001' + '.pdf')
        filemove.append('snps.annotation.full.1')
        filemove.append('snplist.alleles.nc')
        filemove.append('snplist.alleles.utr')
        filemove.append('snplist.alleles.utrncnt')
        filemove.append('snplist.alleles.ns')
        filemove.append('snplist.alleles.syn')
        filemove.append('snplist.alleles.high')
        filemove.append('snplist.alleles.poor')
        filemove.append('snplist.alleles.readyannot')
        filemove.append('EMFreqAssoc.out')
        for src in filemove:
            srcpath = os.path.join(dctOptions.outputdir, src)
            if os.path.exists(srcpath):
                last_part = os.path.split(srcpath)[1]
                os.rename(srcpath, os.path.join(scratchpath, last_part))

        filemove = []
        filemove.append('snps.dosage.pool')
        filemove.append('snps.dosage')
        filemove.append('PooledExperiment.summary')
        filemove.append('PooledExperiment.pbp')
        filemove.append('PooledExperiment.allpositions')
        filemove.append('PooledExperiment.snpcalls')
        filemove.append('PooledExperiment.pf')
        filemove.append('heatmap.exon.matrix')
        filemove.append('RareTest.Calpha.regions')
        filemove.append('RareTest.Calpha')
        filemove.append('RareTest.Calpha.mix')
        filemove.append('Power001.eps')
        filemove.append('Power001.pdf')
        for src in filemove:
            pathrewrite = os.path.join(dctOptions.outputdir, src)
            if os.path.exists(pathrewrite):
                srcpath = pathrewrite
                last_part = os.path.split(srcpath)[1]
                os.rename(srcpath, os.path.join(resultspath, last_part))


def ensurePathSyzygy(path):
    path = os.path.expanduser(path)
    if os.path.exists(path):
        return path
    else:
        (path, file) = os.path.split(path)
        pattern = re.compile(str(file).replace('.', '[.]'), re.IGNORECASE)
        if os.path.exists(path):
            for item in os.listdir(path):
                match = pattern.search(item)
                if match:
                    return os.path.join(path, file)
                    file = os.path.join(path, file)
                    print 'Creating file: ' + file
                    open(file, 'w').close()
                    return file
                else:
                    return
                return path

        else:
            os.mkdir(path)
            print 'Creating Directory: ' + path
    return


def MakeArguments(possible_args, dctOptions):
    current_args = []
    for key in possible_args:
        item = getattr(dctOptions, key)
        if not item == None:
            if item == True:
                current_args.append('--' + key)
            elif item == False:
                continue
            else:
                current_args.append('--' + key)
                current_args.append(item)

    return current_args


if __name__ == '__main__':
    main()