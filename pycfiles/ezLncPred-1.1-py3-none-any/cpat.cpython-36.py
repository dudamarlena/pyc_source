# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/CPAT/bin/cpat.py
# Compiled at: 2020-01-13 01:03:23
# Size of source mod 2**32: 10445 bytes
"""---------------------------------------------------------------------------------------
CPAT: Coding Potential Assessing Tool
------------------------------------------------------------------------------------------"""
import os, sys, os, sys, string
from optparse import OptionParser
import warnings, string, collections, signal
from numpy import mean, median, std, nansum
import subprocess, pysam, numpy as np
from ..lib.cpmodule import fickett
from ..lib.cpmodule import orf
from ..lib.cpmodule import fasta
from ..lib.cpmodule import FrameKmer
from ..lib.cpmodule import ireader
__author__ = 'Liguo Wang'
__contributor__ = 'Liguo Wang, Hyun Jung Park, Wei Li'
__copyright__ = 'Copyright 2012, Mayo Clinic'
__credits__ = []
__license__ = 'GPL'
__version__ = '1.2.4'
__maintainer__ = 'Liguo Wang'
__email__ = 'wang.liguo@mayo.edu; wangliguo78@gmail.com'
__status__ = 'Production'

def coding_prediction(rdata, idata, outfile):
    """rdata stored the linear regression model, idata is data matrix containing features"""
    RCMD = open(outfile + '.r', 'w')
    print(('load("%s")' % rdata), file=RCMD)
    print(('test <- read.table(file="%s",sep="\\t",col.names=c("ID","mRNA","ORF","Fickett","Hexamer"),quote = "")' % idata), file=RCMD)
    print('test$prob <- predict(mylogit,newdata=test,type="response")', file=RCMD)
    print('attach(test)', file=RCMD)
    print('output <- cbind("mRNA_size"=mRNA,"ORF_size"=ORF,"Fickett_score"=Fickett,"Hexamer_score"=Hexamer,"coding_prob"=test$prob)', file=RCMD)
    print(('write.table(output,file="%s",quote=F,sep="\\t",row.names=ID)' % outfile), file=RCMD)
    RCMD.close()
    try:
        subprocess.call(('Rscript ' + outfile + '.r'), shell=True)
    except:
        pass


def sum_bwfile(inbedline, bwfile):
    """retrieve sum of conservation score for all exons from input bed line"""
    line = inbedline
    bw_signal = []
    try:
        fields = line.rstrip('\r\n').split()
        txStart = int(fields[1])
        chrom = fields[0]
        strand = fields[5]
        geneName = fields[3]
        score = fields[4]
        exon_start = map(int, fields[11].rstrip(',').split(','))
        exon_start = map(lambda x: x + txStart, exon_start)
        exon_end = map(int, fields[10].rstrip(',').split(','))
        exon_end = map(lambda x, y: x + y, exon_start, exon_end)
    except:
        print('Incorrect bed format.', file=(sys.stderr))

    try:
        for st, end in zip(exon_start, exon_end):
            bw_signal.extend(bwfile.get_as_array(chrom, st, end))
            wigsum = nansum(bw_signal)

    except:
        wigsum = 0

    wigsum = np.nan_to_num(wigsum)
    return wigsum


def bed_or_fasta(infile):
    """determine if the input file is bed or fasta format"""
    format = 'UNKNOWN'
    for line in ireader.reader(infile):
        byte = '#'.encode(encoding='utf-8', errors='strict')
        if line.startswith(byte):
            continue
        byte1 = '>'.encode(encoding='utf-8', errors='strict')
        if line.startswith(byte1):
            format = 'FASTA'
            return format
        if len(line.split()) == 12:
            format = 'BED'
            return format

    return format


def index_fasta(infile):
    """index fasta file using samTools"""
    if os.path.isfile(infile):
        pass
    else:
        print(('Indexing ' + infile + ' ...'), file=(sys.stderr))
        pysam.faidx(infile)
        print('Done!', file=(sys.stderr))


def extract_feature_from_bed(inbed, refgenome, stt, stp, c_tab, g_tab):
    """extract features of sequence from bed line"""
    stt_coden = stt.strip().split(',')
    stp_coden = stp.strip().split(',')
    transtab = str.maketrans('ACGTNX', 'TGCANX')
    mRNA_seq = ''
    mRNA_size = 0
    if inbed.strip():
        try:
            fields = inbed.split()
            chrom = fields[0]
            tx_start = int(fields[1])
            tx_end = int(fields[2])
            geneName = fields[3]
            strand = fields[5].replace(' ', '_')
            exon_num = int(fields[9])
            exon_sizes = map(int, fields[10].rstrip(',\n').split(','))
            exon_starts = map(int, fields[11].rstrip(',\n').split(','))
            exon_starts = map(lambda x: x + tx_start, exon_starts)
            exon_ends = map(int, fields[10].rstrip(',\n').split(','))
            exon_ends = map(lambda x, y: x + y, exon_starts, exon_ends)
            intron_starts = exon_ends[:-1]
            intron_ends = exon_starts[1:]
        except:
            print(('Wrong format!' + inbed), file=(sys.stderr))
            return
            mRNA_size = sum(exon_sizes)
            for st, end in zip(exon_starts, exon_ends):
                exon_coord = chrom + ':' + str(st + 1) + '-' + str(end)
                tmp = pysam.faidx(refgenome, exon_coord)
                mRNA_seq += ''.join([i.rstrip('\n\r') for i in tmp[1:]])

            if strand == '-':
                mRNA_seq = mRNA_seq.upper().translate(transtab)[::-1]
            tmp = orf.ORFFinder(mRNA_seq)
            CDS_size, CDS_frame, CDS_seq = tmp.longest_orf(direction='+', start_coden=stt_coden, stop_coden=stp_coden)
            fickett_score = fickett.fickett_value(CDS_seq)
            hexamer = FrameKmer.kmer_ratio(CDS_seq, 6, 3, c_tab, g_tab)
            return (
             geneName, mRNA_size, CDS_size, fickett_score, hexamer)


def extract_feature_from_seq(seq, stt, stp, c_tab, g_tab):
    """extract features of sequence from fasta entry"""
    stt_coden = stt.strip().split(',')
    stp_coden = stp.strip().split(',')
    transtab = str.maketrans('ACGTNX', 'TGCANX')
    mRNA_seq = seq.upper()
    mRNA_size = len(seq)
    tmp = orf.ORFFinder(mRNA_seq)
    CDS_size1, CDS_frame1, CDS_seq1 = tmp.longest_orf(direction='+', start_coden=stt_coden, stop_coden=stp_coden)
    fickett_score1 = fickett.fickett_value(CDS_seq1)
    hexamer = FrameKmer.kmer_ratio(CDS_seq1, 6, 3, c_tab, g_tab)
    return (mRNA_size, CDS_size1, fickett_score1, hexamer)


def main(args):
    options = args
    script_dir = os.path.split(os.path.realpath(__file__))[0]
    options.hexamer_dat = script_dir + '/../dat/' + options.species + '_Hexamer.tsv'
    options.logit_model = script_dir + '/../dat/' + options.species + '_logitModel.RData'
    for file in [options.fasta, options.outfile, options.logit_model, options.hexamer_dat]:
        if not file:
            parser.print_help()
            sys.exit(0)

    coding = {}
    noncoding = {}
    for line in open(options.hexamer_dat):
        line = line.strip()
        fields = line.split()
        if fields[0] == 'hexamer':
            continue
        coding[fields[0]] = float(fields[1])
        noncoding[fields[0]] = float(fields[2])

    count = 0
    TMP = open(options.outfile + '.dat', 'w')
    file_format = bed_or_fasta(options.fasta)
    if file_format == 'UNKNOWN':
        print("\nError: unknown file format of '-g'\n", file=(sys.stderr))
        parser.print_help()
        sys.exit(0)
    else:
        if file_format == 'FASTA':
            for sname, seq in FrameKmer.seq_generator(options.fasta):
                count += 1
                mRNA_size, CDS_size, fickett_score, hexamer = extract_feature_from_seq(seq=seq, stt=(options.start_codons), stp=(options.stop_codons), c_tab=coding, g_tab=noncoding)
                print(('\t'.join(str(i) for i in (sname, mRNA_size, CDS_size, fickett_score, hexamer))), file=TMP)

    TMP.close()
    coding_prediction(options.logit_model, options.outfile + '.dat', options.outfile)


if __name__ == '__main__':
    main()