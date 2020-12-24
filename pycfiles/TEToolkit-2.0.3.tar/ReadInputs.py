# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yjin/Workspace/DiffChip/DiffChip2/DIFFCHIP/IO/ReadInputs.py
# Compiled at: 2014-02-11 09:52:02
"""
Created on Oct 12, 2011

this code is for reading input parameters.

@author: Ying Jin
@status: 
@contact: yjin@cshl.edu
@version: 
"""
import sys, os, re, logging, time, gzip
from math import log
from DIFFCHIP.Constants import *
from DIFFCHIP.ShortRead.ParseBEDFile import BEDFile, BAMFile, SAMFile
from DIFFCHIP.TEindex import *

def read_opts(parser):
    """ object parser contains parsed options """
    args = parser.parse_args()
    for i in range(len(args.tfiles)):
        if not os.path.isfile(args.tfiles[i]):
            logging.error('No such file: %s !\n' % args.tfiles[i])
            sys.exit(1)

    if not os.path.isfile(args.tinputs[0]):
        logging.error('No such file: %s !\n' % args.tinputs)
        sys.exit(1)
    if args.cfiles != None:
        for i in range(len(args.cfiles)):
            if not os.path.isfile(args.cfiles[i]):
                logging.error('No such file: %s !\n' % args.cfiles[i])
                sys.exit(1)
            elif args.cinputs == None:
                logging.error('No input for control samples!\n')
                sys.exit(1)

    else:
        args.cinputs = None
    if args.TEmode != 'multi' and args.TEmode != 'sameFamily':
        logging.error('Does not support TE mode : %s !\n' % args.TEmode)
    if args.format == 'BAM':
        args.parser = BAMFile
    elif args.format == 'SAM':
        args.parser = SAMFile
    elif args.format == 'BED':
        args.parser = BEDFile
    else:
        logging.error('Does not support such file format: %s !\n' % args.format)
        sys.exit(1)
    if args.wsize < 0:
        logging.error('window size should be greater than 0, default value %d was used\n' % WIN_SIZE)
        args.wsize = WIN_SIZE
    if args.step < 0:
        logging.error('step size should be greater than 0, default value  %d was used\n' % STEP)
        args.step = STEP
    if args.step > args.wsize:
        logging.error('step should be smaller than window size,default value %d was used\n' % STEP)
        args.step = STEP
    if args.minread < 0:
        args.minread = 0
    if args.minread > 20:
        args.minread = 20
    if args.species[0] not in ('hg', 'rn', 'mm', 'dm'):
        logging.error('species not found %s \n' % args.species[0])
        parser.print_help()
        sys.exit(1)
    args.gsize = efgsize[args.species[0]]
    args.gsize = float(args.gsize)
    if args.species[0] == 'hg':
        args.chrom = HS_CHROM
        args.species[0] = 'hg19'
    elif args.species[0] == 'rn':
        args.chrom = RN_CHROM
    elif args.species[0] == 'mm':
        args.chrom = MM_CHROM
        args.species[0] = 'mm9'
    elif args.species[0] == 'dm':
        args.chrom = DM_CHROM
        args.species[0] = 'dm3'
    if args.norm not in ('sd', 'bc'):
        logging.error('normalization method %s not supported\n' % args.norm)
        parser.print_help()
        sys.exit(1)
    if args.pval < 0 or args.pval > 1:
        logging.error('p-value should be a value in [0,1]\n')
        sys.exit(1)
    args.log_pvalue = log(args.pval, 10) * -10
    if args.gap < 0:
        logging.error('gap size should be greater than 0, default value was used\n')
        args.gap = GAP
    if args.fragsize < 0:
        logging.error('fragment size should be greater than 0, default value %d was used\n' % FRAG_SIZE)
        args.fragsize = FRAG_SIZE
    args.dfbs = args.prj_name + '_dfbs'
    logging.basicConfig(level=(4 - args.verbose) * 10, format='%(levelname)-5s @ %(asctime)s: %(message)s ', datefmt='%a, %d %b %Y %H:%M:%S', stream=sys.stderr, filemode='w')
    args.error = logging.critical
    args.warn = logging.warning
    args.debug = logging.debug
    args.info = logging.info
    cinput = None
    if args.cinputs != None:
        cinput = args.cinputs[0]
    args.argtxt = ('\n').join((
     '# ARGUMENTS LIST:',
     '# name = %s' % args.prj_name,
     '# treatment files = %s' % args.tfiles,
     '# control files = %s' % args.cfiles,
     '# treatment input = %s' % args.tinputs[0],
     '# control input = %s' % cinput,
     '# step = %d' % args.step,
     '# fragment size = %d' % args.fragsize,
     '# species = %s (hg:human, rn:rat, mm:mouse)' % args.species[0],
     '# min read cutoff = %d' % args.minread,
     '# statistical model = Poisson distribution',
     '# normalization = %s (sd: sequence depth, bc: bin correlation)' % args.norm,
     '# pvalue cutoff = %.2e' % args.pval,
     '# TEmode = %s ' % args.TEmode,
     '# TE annotation file = %s \n' % args.TEannotation))
    return args


def read_chrlen_tbl(chrfile, error, info):
    """ read in chrom_size file """
    if not os.path.isfile(chrfile):
        error('No such file: %s !\n' % chrfile)
        sys.exit(1)
    try:
        f = open(chrfile, 'r')
    except IOError:
        error('open file %s error !\n' % chrfile)
        sys.exit(1)
    else:
        chrlen_map = dict()
        cnt = 0
        for line in f:
            cnt += 1
            line = line.strip()
            items = line.split('\t')
            if len(items) < 2:
                info('Insufficient chromosome information at % s, line: %s. Skip!\n' % (chrfile, line))
            if re.match('^(c|C)hr', items[0]) and re.match('^[0-9]+$', items[1]):
                chrlen_map[items[0]] = int(items[1])
            else:
                info('Format error at %s, line %d: %s. Skip!\n' % (chrfile, cnt, line))

        f.close()

    return chrlen_map


def read_te_annotation(filename):
    """read TE annotation file """
    if not os.path.isfile(filename):
        logging.error('No such file %s !\n' % filename)
        sys.exit(1)
    logging.info('reading TE annoation file %s ...\n' % filename)
    time.sleep(1)
    TEidx = TEindex(filename)
    return TEidx


def read_short_reads(samples, parser):
    """read short reads from single or multple samples and stored in short read objects """
    shortReads = []
    for i in range(len(samples)):
        s = samples[i]
        if not os.path.isfile(s):
            logging.error('No such file %s !\n' % s)
            sys.exit(1)
        logging.info('reading sample file %s ...\n' % s)
        time.sleep(1)
        b = parser(s)
        t = b.build_fwtrack()
        shortReads.append(t)

    return shortReads


def read_short_reads_sameFam(samples, parser, teIdx):
    """read short reads from single or multple samples and stored in short read objects """
    shortReads = []
    for i in range(len(samples)):
        s = samples[i]
        if not os.path.isfile(s):
            logging.error('No such file %s !\n' % s)
            sys.exit(1)
        logging.info('reading sample file %s ...\n' % s)
        time.sleep(1)
        b = parser(s)
        t = b.build_fwtrack_v2(teIdx)
        shortReads.append(t)

    return shortReads


def __bam2bed(sample, pairend, error):
    res = sample + '.bed'
    if pairend == 0:
        try:
            os.system('bamToBED -ed -i sample >res')
            res = __assignWeight(sample, '.bed', error)
        except:
            error('file format error %s !\n' % sample)
            sys.exit(0)

    else:
        try:
            os.system('bamToBED -bedpe -i sample >res')
            res = __assignWeight(sample, '.bed', error)
        except:
            error('file format error %s !\n' % sample)
            sys.exit(0)

    return res


def __assignWeight(sample, suffix, error):
    src = sample + suffix
    dest = sample + '.bal.bed'
    lines = []
    cur_seqid = '-1'
    multi_num = 0
    try:
        f = open(src, 'r')
        of = open(dest, 'w')
    except IOError:
        error('open file %s error !\n' % src)
        sys.exit(1)
    else:
        for line in f:
            line = line.strip()
            arr = line.split('\t')
            if cur_seqid == arr[3]:
                lines.append(line)
                multi_num += 1
            else:
                if multi_num > 0:
                    val = 1 / multi_num
                    for record in lines:
                        of.write(record + '\t' + val + '\n')

                lines.clear()
                lines.append(line)
                cur_seqid = arr[3]
                multi_num = 1

        f.close()
        if multi_num > 0:
            val = 1 / multi_num
            for record in lines:
                of.write(record + '\t' + val + '\n')

    of.close()
    return dest