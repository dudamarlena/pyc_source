# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/PredLnc_GFStack/src/get_features_module/FrameKmer.py
# Compiled at: 2019-12-04 10:19:56
# Size of source mod 2**32: 4312 bytes
"""deal with Kmer. DNA sequence should only A, C, G, T. python2.7 or newer"""
import os, sys, numpy, math
from collections import Counter
import re, itertools
from .cpmodule import ireader

def word_generator(seq, word_size, step_size, frame=0):
    """generate DNA word from sequence using word_size and step_size. Frame is 0, 1 or2"""
    for i in range(frame, len(seq), step_size):
        word = seq[i:i + word_size]
        if len(word) == word_size:
            yield word


def seq_generator(fastafile):
    """DNA sequence only contains A,C,G,T,N. sequence with other characters will be removed"""
    tmpseq = ''
    name = ''
    DNA_pat = re.compile('^[ACGTN]+$')
    for line in ireader.reader(fastafile):
        line = line.strip().upper()
        if line.startswith(('#', ' ', '\n')):
            pass
        else:
            if line.startswith(('>', '@')):
                if tmpseq:
                    yield [
                     name, tmpseq]
                    tmpseq = ''
                name = line.split()[0][1:]
            else:
                if DNA_pat.match(line):
                    tmpseq += line

    yield [
     name, tmpseq]


def all_possible_kmer(l):
    """return all possible combinations of A,C,G,T,N. only support A,C,G,T,N. l is length of kmer"""
    for i in itertools.product(['A', 'C', 'G', 'T', 'N'], repeat=l):
        yield ''.join(i)


def kmer_freq_file(fastafile, word_size, step_size=1, frame=0, min_count=0):
    """Calculate kmer frequency from fasta file"""
    seq_num = 0
    ret_dict = {}
    for n, s in seq_generator(fastafile):
        seq_num += 1
        if seq_num == 1:
            count_table = Counter(word_generator(s, word_size=word_size, step_size=step_size, frame=frame))
        else:
            count_table.update(word_generator(s, word_size=word_size, step_size=step_size, frame=frame))

    for kmer in all_possible_kmer(word_size):
        if kmer not in count_table:
            count_table[kmer] = 0
        if count_table[kmer] >= min_count:
            if 'N' in kmer:
                pass
            else:
                ret_dict[kmer] = count_table[kmer]

    return ret_dict


def kmer_freq_seq(seq, word_size, step_size=1, frame=0, min_count=0):
    """Calculate kmer frequency from DNA sequence. coding. genome is hexamer table calculated
        from coding region and whole genome (as background control)
        """
    count_table = Counter(word_generator(seq, word_size=word_size, step_size=step_size, frame=frame))
    for kmer in all_possible_kmer(word_size):
        if kmer not in count_table:
            count_table[kmer] = 0


def kmer_ratio(seq, word_size, step_size, coding, noncoding):
    if len(seq) < word_size:
        return 0
    sum_of_log_ratio_0 = 0.0
    sum_of_log_ratio_1 = 0.0
    sum_of_log_ratio_2 = 0.0
    frame0_count = 0.0
    frame1_count = 0.0
    frame2_count = 0.0
    for k in word_generator(seq=seq, word_size=word_size, step_size=step_size, frame=0):
        if not k not in coding:
            if k not in noncoding:
                pass
            else:
                if coding[k] > 0 and noncoding[k] > 0:
                    sum_of_log_ratio_0 += math.log(coding[k] / noncoding[k])
        if coding[k] > 0:
            if noncoding[k] == 0:
                sum_of_log_ratio_0 += 1
            else:
                if coding[k] == 0:
                    if noncoding[k] == 0:
                        continue
            if coding[k] == 0:
                if noncoding[k] > 0:
                    sum_of_log_ratio_0 -= 1
                else:
                    continue
                frame0_count += 1

    try:
        return sum_of_log_ratio_0 / frame0_count
    except:
        return -1