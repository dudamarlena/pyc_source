# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/HmmFea.py
# Compiled at: 2019-10-31 07:26:01
import os, sys, numpy as np, subprocess
from utils import GetFasta
from utils import RevComp
from utils import Codon2AA2
_AA_list = [
 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
_DNA = [
 'A', 'C', 'G', 'T']
_3mer_list = []
for dna1 in _DNA:
    for dna2 in _DNA:
        for dna3 in _DNA:
            _3mer_list.append(dna1 + dna2 + dna3)

_IUPAC = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'R': 'AG', 'Y': 'CT', 'M': 'AC', 'K': 'GT', 'S': 'CG', 'W': 'AT', 'H': 'ACT', 'B': 'CGT', 'V': 'ACG', 'D': 'AGT', 'N': 'ACGT'}

def IUPAC_3mer(seq):
    """Return a list of all possible 3mers of the sequence"""
    kmer_list = []
    for dna1 in _IUPAC[seq[0]]:
        for dna2 in _IUPAC[seq[1]]:
            for dna3 in _IUPAC[seq[2]]:
                if Codon2AA2(dna1 + dna2 + dna3) != 'J':
                    kmer_list.append(dna1 + dna2 + dna3)

    return kmer_list


def SixFrame(seq, direction=1):
    """Translate RNA to protein in three of six frames
       direction = 1: forward
       direction = 0: both
       direction = 2: minus
    """
    protein_list = []
    if direction == 1:
        for i in range(3):
            protein_list.append(Translation(seq[i:]))

    elif direction == 2:
        for i in range(3):
            protein_list.append(Translation(RevComp(seq)[i:]))

    elif direction == 0:
        for i in range(3):
            protein_list.append(Translation(seq[i:]))
            protein_list.append(Translation(RevComp(seq)[i:]))

    return protein_list


def Translation(seq):
    """translate DNA to protein"""
    length = len(seq) / 3
    protein = ''
    for i in range(length):
        if Codon2AA2(seq[i * 3:(i + 1) * 3]) == 'J':
            tmpAA = '*'
        elif Codon2AA2(seq[i * 3:(i + 1) * 3]) == 'Z':
            tmp_3mer_list = IUPAC_3mer(seq[i * 3:(i + 1) * 3])
            tmp_aa_list = []
            for tmp_3mer in tmp_3mer_list:
                tmp_aa_list.append(Codon2AA2(tmp_3mer))

            if len(set(tmp_aa_list)) > 1:
                tmpAA = 'X'
            elif len(set(tmp_aa_list)) == 1:
                tmpAA = tmp_aa_list[0]
            else:
                tmpAA = '*'
        else:
            tmpAA = Codon2AA2(seq[i * 3:(i + 1) * 3])
        protein += tmpAA

    return protein


def GenerateTrans(fasta, outfile):
    """generate translated fasta file"""
    try:
        f = open(outfile, 'w')
    except (IOError, ValueError) as e:
        print >> sys.stderr, str(e)
        sys.exit(1)

    SeqID, SeqList = GetFasta(fasta)
    for seqid, seq in zip(SeqID, SeqList):
        tmp_protein_list = SixFrame(seq, direction=1)
        for tmp_protein in tmp_protein_list:
            f.write(('').join(['>', seqid]) + '\n')
            f.write(tmp_protein + '\n')

    f.close()


def RunHMM(fasta, output, pfam, thread=8):
    """run HMMER and generate output"""
    out1 = output + '.out1'
    out2 = output + '.out2'
    cmd = 'hmmsearch -o ' + out1 + ' --domtblout ' + out2 + ' --noali -E 0.1 --domE 0.1 --cpu ' + str(thread) + ' ' + pfam + ' ' + fasta
    subprocess.call(cmd, shell=True)
    subprocess.call('rm ' + out1, shell=True)


def ReadHmm(hmmOut):
    """Read hmmer output file and extract features"""
    try:
        hmm = open(hmmOut, 'rU')
    except (IOError, ValueError) as e:
        print >> sys.stderr, str(e)
        sys.exit(1)

    HMM_dict = {}
    for line in hmm.readlines():
        line = line.strip()
        if line[0] == '#':
            continue
        tmpfeature_list = []
        tmplist = line.split()
        tmpid = tmplist[0]
        tmpfeature_list.append(tmplist[11])
        tmpfeature_list.append(tmplist[13])
        tmpfeature_list.append(str(abs(int(tmplist[16]) - int(tmplist[15])) / float(tmplist[5])))
        tmpfeature_list.append(str(abs(int(tmplist[18]) - int(tmplist[17])) / float(tmplist[2])))
        tmpfeature_list.append(int(tmplist[17]) * 3)
        tmpfeature_list.append(int(tmplist[18]) * 3)
        if HMM_dict.has_key(tmpid):
            if HMM_dict.get(tmpid)[0] > tmpfeature_list[0]:
                HMM_dict[tmpid] = tmpfeature_list
        else:
            HMM_dict[tmpid] = tmpfeature_list

    hmm.close()
    return HMM_dict