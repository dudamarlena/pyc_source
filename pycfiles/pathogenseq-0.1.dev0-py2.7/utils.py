# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pathogenseq/utils.py
# Compiled at: 2018-07-14 05:50:46
import re
from .fasta import *
indelre = re.compile('(\\w)[\\+\\-](\\d+)(\\w+)')
gap_char = '-'

def recode_indels(indels):
    sorted_indels = sorted([ x for x in indels ], key=lambda y: len(y))
    largest_del = sorted([ x for x in indels if gap_char in x ], key=lambda y: len(y))
    if len(largest_del) == 0:
        leftseq = indelre.search(sorted_indels[(-1)]).group(1)
        rightseq = ''
    else:
        leftseq = indelre.search(largest_del[(-1)]).group(1)
        rightseq = indelre.search(largest_del[(-1)]).group(3)
    refseq = leftseq + rightseq
    recoded_indels = []
    for i in indels:
        if gap_char in i:
            indel_len = int(indelre.search(i).group(2))
            iseq = leftseq + rightseq[:-(len(rightseq) - indel_len)]
        elif '+' in i:
            iseq = leftseq + indelre.search(i).group(3) + rightseq
        else:
            iseq = i + rightseq
        recoded_indels.append(iseq)

    return (
     refseq, recoded_indels)


def variants2vcf(var_file, seq1_file, seq2_file, prefix, vcf_file):
    seq1_dict = fasta(seq1_file)
    seq2_dict = fasta(seq2_file)
    good_dp = 20
    realign_min_length = 5
    min_flank = 100
    seq1_chrom_i = 0
    seq1_pos_i = 1
    seq1_i = 2
    seq2_i = 3
    seq2_pos_i = 4
    seq2_chrom_i = 5
    gap_char = '-'
    del_lines = []
    ins_lines = []
    indel_line_set = set()
    tmp = []
    prev_type = None
    prev_pos = None
    prev_seq1_chrom = None
    lines = [ l.rstrip().split() for l in open(var_file).readlines() ]
    for i in range(len(lines)):
        row = lines[i]
        pos = int(row[seq1_pos_i])
        seq1_chrom = row[seq1_chrom_i]
        if row[seq1_i] == gap_char or row[seq2_i] == gap_char:
            indel_line_set.add(i)
            if prev_pos == None:
                tmp = [
                 i]
            elif row[seq1_i] == gap_char:
                if pos == prev_pos:
                    tmp.append(i)
                else:
                    if prev_type == 'ins':
                        ins_lines.append(tmp)
                    else:
                        del_lines.append(tmp)
                    tmp = [
                     i]
            elif row[seq2_i] == gap_char:
                if pos == prev_pos + 1:
                    tmp.append(i)
                else:
                    if prev_type == 'ins':
                        ins_lines.append(tmp)
                    else:
                        del_lines.append(tmp)
                    tmp = [
                     i]
            prev_type = 'ins' if row[seq1_i] == gap_char else 'del'
            prev_pos = pos
            prev_seq1_chrom = seq1_chrom

    variants = defaultdict(dict)
    for i in set(range(len(lines))) - indel_line_set:
        row = lines[i]
        pos, ref_seq, alt_seq = row[seq1_pos_i:seq1_pos_i + 3]
        seq1_chrom = row[seq1_chrom_i]
        variants[seq1_chrom][int(pos)] = (ref_seq, alt_seq, '1/1', good_dp)

    OUT = open(vcf_file, 'w')
    OUT.write('##fileformat=VCFv4.1\n##reference=/home/jody/refgenome/MTB-h37rv_asm19595v2-eg18.fa\n##contig=<ID=seq1_chromosome,length=4411532>\n##INFO=<ID=DP4,Number=4,Type=Integer,Description="Number of high-quality ref-forward , ref-reverse, alt-forward and alt-reverse bases">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Raw Depth">\n##INFO=<ID=MinDP,Number=1,Type=Integer,Description="Minimum per-sample depth in this gVCF block">\n##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s\n' % prefix)
    npos = None
    nseq1_chrom = None
    for seq1_chrom in sorted(variants):
        for pos in sorted(variants[seq1_chrom]):
            if nseq1_chrom != seq1_chrom:
                if pos != 1:
                    npos = 1
                    OUT.write('%s\t%s\t.\t%s\t.\t.\t.\tEND=%s;MinDP=20\tGT:DP\t0/0:%s\n' % (seq1_chrom, npos, seq1_dict.get_seq(seq1_chrom, npos), pos - 1, good_dp))
            elif pos != npos + 1:
                OUT.write('%s\t%s\t.\t%s\t.\t.\t.\tEND=%s;MinDP=20\tGT:DP\t0/0:%s\n' % (nseq1_chrom, npos + 1, seq1_dict.get_seq(seq1_chrom, npos), pos - 1, good_dp))
            var = variants[seq1_chrom][pos]
            if pos == 165608:
                log(var)
            if var[0] == 'N' or var[0] == 'n' or var[1] == 'N' or var[1] == 'n':
                if pos == 165608:
                    log(var)
                OUT.write('%s\t%s\t.\t%s\t%s\t255\t.\t.\tGT:DP\t%s:%s\n' % (seq1_chrom, pos, var[0], '.', './.', '.'))
            else:
                OUT.write('%s\t%s\t.\t%s\t%s\t255\t.\t.\tGT:DP\t%s:%s\n' % (seq1_chrom, pos, var[0], var[1], var[2], var[3]))
            npos = pos
            nseq1_chrom = seq1_chrom

    OUT.close()
    return


def muscle_align(filename, outfile):
    cmd = 'muscle -in %s -out %s' % (filename, outfile)
    run_cmd(cmd)