# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/utils.py
# Compiled at: 2019-12-07 22:50:39
# Size of source mod 2**32: 3157 bytes
import sys, numpy as np
np.seterr(all='ignore')

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


def GetFasta(inputfile):
    """Get sequence from input, seqid=the first part without space"""
    try:
        f = open(inputfile, 'r')
    except (IOError, ValueError) as e:
        (
         print >> sys.stderr, str(e))
        sys.exit(1)

    tmpseq = ''
    seqlist = []
    seqID = []
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        else:
            if line[0] == '>':
                seqID.append(line.split()[0][1:])
                if tmpseq != '':
                    seqlist.append(tmpseq)
                tmpseq = ''
            else:
                tmpseq += line.upper()

    seqlist.append(tmpseq)
    f.close()
    return [
     seqID, seqlist]


def RevComp(seq):
    """reverse complement of sequence"""
    complement = {'A':'T', 
     'C':'G',  'G':'C',  'T':'A',  'a':'T',  'c':'G',  'g':'C',  't':'A'}
    reverse_complement = ''.join(complement.get(base, base) for base in reversed(seq))
    return reverse_complement


def Codon2AA2(codon):
    """convert codon to aa"""
    if codon == 'TTT' or codon == 'TTC':
        return 'F'
    else:
        if codon == 'TTA' or codon == 'TTG' or codon == 'CTT' or codon == 'CTA' or codon == 'CTC' or codon == 'CTG':
            return 'L'
        else:
            if codon == 'ATT' or codon == 'ATC' or codon == 'ATA':
                return 'I'
            else:
                if codon == 'ATG':
                    return 'M'
                else:
                    if codon == 'GTA' or codon == 'GTC' or codon == 'GTG' or codon == 'GTT':
                        return 'V'
                    else:
                        if codon == 'GAT' or codon == 'GAC':
                            return 'D'
                        else:
                            if codon == 'GAA' or codon == 'GAG':
                                return 'E'
                            else:
                                if codon == 'TCA' or codon == 'TCC' or codon == 'TCG' or codon == 'TCT':
                                    return 'S'
                                else:
                                    if codon == 'CCA' or codon == 'CCC' or codon == 'CCG' or codon == 'CCT':
                                        return 'P'
                                    else:
                                        if codon == 'ACA' or codon == 'ACG' or codon == 'ACT' or codon == 'ACC':
                                            return 'T'
                                        else:
                                            if codon == 'GCA' or codon == 'GCC' or codon == 'GCG' or codon == 'GCT':
                                                return 'A'
                                            else:
                                                if codon == 'TAT' or codon == 'TAC':
                                                    return 'Y'
                                                if codon == 'CAT' or codon == 'CAC':
                                                    return 'H'
                                                if codon == 'CAA' or codon == 'CAG':
                                                    return 'Q'
                                            if codon == 'AAT' or codon == 'AAC':
                                                return 'N'
                                        if codon == 'AAA' or codon == 'AAG':
                                            return 'K'
                                    if codon == 'TGT' or codon == 'TGC':
                                        return 'C'
                                if codon == 'TGG':
                                    return 'W'
                            if codon == 'CGA' or codon == 'CGC' or codon == 'CGG' or codon == 'CGT':
                                return 'R'
                        if codon == 'AGT' or codon == 'AGC':
                            return 'S'
                    if codon == 'AGA' or codon == 'AGG':
                        return 'R'
                if codon == 'GGA' or codon == 'GGC' or codon == 'GGG' or codon == 'GGT':
                    return 'G'
            if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
                return 'J'
        return 'Z'


def SixMer2AA(seq):
    """Convert 6mer to 2 AA"""
    return Codon2AA2(seq[0:3]) + Codon2AA2(seq[3:6])