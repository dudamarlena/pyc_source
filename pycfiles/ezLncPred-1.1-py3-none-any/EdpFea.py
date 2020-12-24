# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/EdpFea.py
# Compiled at: 2019-10-31 07:26:01
import os, sys, numpy as np
from utils import GetFasta
from utils import Codon2AA2
from HmmFea import ReadHmm
from HmmFea import RunHMM
from HmmFea import GenerateTrans
from Hexamer import HexamerScore2
from Hexamer import ReadLogScore
from Hexamer import MLC
_AA_list = [
 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
_DNA = [
 'A', 'C', 'G', 'T']
_Kmer_list = []
for dna1 in _DNA:
    for dna2 in _DNA:
        _Kmer_list.append(dna1 + dna2)

_3mer_list = []
for dna1 in _DNA:
    for dna2 in _DNA:
        for dna3 in _DNA:
            _3mer_list.append(dna1 + dna2 + dna3)

_IUPAC = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'R': 'AG', 'Y': 'CT', 'M': 'AC', 'K': 'GT', 'S': 'CG', 'W': 'AT', 'H': 'ACT', 'B': 'CGT', 'V': 'ACG', 'D': 'AGT', 'N': 'ACGT'}

def IUPAC_2mer(seq):
    """Return a list of all possible 2mers of the sequence"""
    kmer_list = []
    for dna1 in _IUPAC[seq[0]]:
        for dna2 in _IUPAC[seq[1]]:
            kmer_list.append(dna1 + dna2)

    return kmer_list


def IUPAC_3mer(seq):
    """Return a list of all possible 3mers of the sequence"""
    kmer_list = []
    for dna1 in _IUPAC[seq[0]]:
        for dna2 in _IUPAC[seq[1]]:
            for dna3 in _IUPAC[seq[2]]:
                if Codon2AA2(dna1 + dna2 + dna3) != 'J':
                    kmer_list.append(dna1 + dna2 + dna3)

    return kmer_list


def SixMer2AA(seq):
    """Convert 6mer to 2 AA"""
    return Codon2AA2(seq[0:3]) + Codon2AA2(seq[3:6])


def GetFeature(seq, seqid, HMMdict1, logscore_dict):
    if HMMdict1.has_key(seqid):
        hmmfeature = HMMdict1[seqid][1] + '\t' + HMMdict1[seqid][2] + '\t' + HMMdict1[seqid][3]
    else:
        hmmfeature = '0\t0\t0'
    seq = seq.strip()
    ORF, UTR5, UTR3, start, end = GetORF_UTR(seq)
    transcript_len = len(seq)
    if len(seq) > 15:
        mlc_seq, ave_hexamer_score, mlc_start, mlc_end = MLC(seq, logscore_dict)
    else:
        mlc_seq, ave_hexamer_score, mlc_start, mlc_end = ('', 0, 0, 0)
    if len(ORF) >= len(mlc_seq):
        tmp_seq = ORF
        ave_hexamer_score = HexamerScore2(tmp_seq, logscore_dict)
    else:
        tmp_seq = mlc_seq
    mlc_fea = str(len(tmp_seq)) + '\t' + str(len(tmp_seq) * 1.0 / transcript_len)
    if len(tmp_seq) < 6:
        EDP_fea = GetEDP_noORF()
    else:
        EDP_fea = GetEDP(tmp_seq, transcript_len)
    Kmer_EDP_fea = GetKmerEDP(tmp_seq)
    hex_score = str(ave_hexamer_score)
    A_pos_fea = GetBasePositionScore(seq, 'A')
    C_pos_fea = GetBasePositionScore(seq, 'C')
    G_pos_fea = GetBasePositionScore(seq, 'G')
    T_pos_fea = GetBasePositionScore(seq, 'T')
    base_ratio = GetBaseRatio(seq)
    fickett_fea = ('\t').join([str(A_pos_fea), str(C_pos_fea), str(G_pos_fea), str(T_pos_fea), str(base_ratio[0]), str(base_ratio[1]), str(base_ratio[2]), str(base_ratio[3])])
    feature = ('\t').join([EDP_fea, hmmfeature, Kmer_EDP_fea, hex_score, fickett_fea, mlc_fea])
    return feature


def GetBasePositionScore(seq, base):
    """
       compute base(A, C, G, T) position score based
       on Fickett's methods
    """
    base_num = [
     0, 0, 0]
    tmp = len(seq) / 3
    for i in range(0, tmp):
        for j in range(0, 3):
            if seq[(j + 3 * i)] == base:
                base_num[j] += 1

    base_pos_score = max(base_num) * 1.0 / (min(base_num) + 1)
    return base_pos_score


def GetBaseRatio(seq):
    """calculate the A, C, G, T percentage of ORF"""
    A, C, G, T = (1e-09, 1e-09, 1e-09, 1e-09)
    for i in range(0, len(seq)):
        if seq[i] == 'A':
            A += 1
        elif seq[i] == 'C':
            C += 1
        elif seq[i] == 'G':
            G += 1
        elif seq[i] == 'T':
            T += 1

    A = A * 1.0 / (len(seq) + 4e-09)
    C = C * 1.0 / (len(seq) + 4e-09)
    G = G * 1.0 / (len(seq) + 4e-09)
    T = T * 1.0 / (len(seq) + 4e-09)
    return [
     A, C, G, T]


def GetGC_Content(seq):
    """calculate GC content of sequence"""
    A, C, G, T = (1e-09, 1e-09, 1e-09, 1e-09)
    for i in range(0, len(seq)):
        if seq[i] == 'A':
            A += 1
        elif seq[i] == 'C':
            C += 1
        elif seq[i] == 'G':
            G += 1
        elif seq[i] == 'T':
            T += 1

    GC = (G + C) / (A + C + G + T)
    return GC


def GetORF_UTR(seq):
    """Get ORF and UTR from sequence"""
    STP = {}
    STP[0] = []
    STP[1] = []
    STP[2] = []
    STP[0].append(0)
    STP[1].append(1)
    STP[2].append(2)
    AAnum = len(seq) / 3
    for i in range(0, 3):
        for j in range(0, AAnum):
            tmp = seq[i + 3 * j:i + 3 * (j + 1)]
            if tmp == 'TAG' or tmp == 'TAA' or tmp == 'TGA':
                STP[i].append(i + 3 * j)

    ORF = {}
    for i in range(0, 3):
        for j in range(1, len(STP[i])):
            tmpN = (STP[i][j] - STP[i][(j - 1)]) / 3
            for k in range(0, tmpN):
                tmpS = seq[STP[i][(j - 1)] + 3 * k:STP[i][(j - 1)] + 3 * (k + 1)]
                if tmpS == 'ATG':
                    ORF[3 * k + STP[i][(j - 1)]] = STP[i][j] + 3
                    break

        codonNum = (len(seq) - STP[i][(-1)]) / 3
        for k in range(codonNum):
            if seq[STP[i][(-1)] + 3 * k:STP[i][(-1)] + 3 * (k + 1)] == 'ATG':
                ORF[STP[i][(-1)] + 3 * k] = len(seq)
                break

    ORFseq = []
    ORFlen = []
    ORFstart = []
    ORFend = []
    for k, v in ORF.items():
        ORFseq.append(seq[k:v])
        ORFlen.append(v - k)
        ORFstart.append(k)
        ORFend.append(v)

    if ORF:
        idx = np.argmax(ORFlen)
        ORF_l = ORFseq[idx]
        UTR5 = ''
        UTR3 = ''
        if len(seq[0:ORFstart[idx]]) > 0:
            UTR5 = seq[0:ORFstart[idx]]
        if len(seq[ORFend[idx]:]) > 0:
            UTR3 = seq[ORFend[idx]:]
        return [ORF_l, UTR5, UTR3, ORFstart[idx], ORFend[idx]]
    else:
        return [
         '', '', '', 0, 0]


def GetEDP_noORF():
    Codon = {}
    for aa in _AA_list:
        Codon[aa] = 1e-09

    sum_codon = 2e-08
    H = 0.0
    for k, v in Codon.items():
        Codon[k] /= sum_codon
        Codon[k] = -Codon[k] * np.log2(Codon[k])
        H += Codon[k]

    EDP = {}
    for k, v in Codon.items():
        EDP[k] = Codon[k] / H

    outline = ''
    for i in range(20):
        outline += str(0) + '\t'

    return outline


def GetEDP(seq, transcript_len):
    """get features including: ORF length, ORF ratio, ORF EDP of codon"""
    Codon = {}
    for aa in _AA_list:
        Codon[aa] = 1e-09

    sum_codon = 2e-08
    if len(seq) > 3:
        num = len(seq) / 3
        for i in range(0, num):
            if Codon2AA2(seq[i * 3:(i + 1) * 3]) == 'J':
                continue
            elif Codon2AA2(seq[i * 3:(i + 1) * 3]) == 'Z':
                tmp_kmer_list = IUPAC_3mer(seq[i * 3:(i + 1) * 3])
                for tmp_kmer in tmp_kmer_list:
                    Codon[Codon2AA2(tmp_kmer)] += 1.0 / len(tmp_kmer_list)

                sum_codon += 1.0
            else:
                Codon[Codon2AA2(seq[i * 3:(i + 1) * 3])] += 1.0
                sum_codon += 1.0

        H = 0.0
        for k, v in Codon.items():
            Codon[k] /= sum_codon
            Codon[k] = -Codon[k] * np.log2(Codon[k])
            H += Codon[k]

        EDP = {}
        for k, v in Codon.items():
            EDP[k] = Codon[k] / H

        outline = ''
        for k, v in EDP.items():
            outline += str(v) + '\t'

        return outline


def GetKmerEDP(seq):
    Kmer = {}
    for aa in _Kmer_list:
        Kmer[aa] = 1e-09

    sum_Kmer = 1.6e-08
    if len(seq) > 3:
        for i in range(0, len(seq) - 1):
            if seq[i:i + 2] not in _Kmer_list:
                tmp_kmer_list = IUPAC_2mer(seq[i:i + 2])
                for tmp_kmer in tmp_kmer_list:
                    Kmer[tmp_kmer] += 1.0 / len(tmp_kmer_list)

            else:
                Kmer[seq[i:i + 2]] += 1.0
            sum_Kmer += 1.0

        H = 0.0
        for k, v in Kmer.items():
            Kmer[k] /= sum_Kmer
            Kmer[k] = -Kmer[k] * np.log2(Kmer[k])
            H += Kmer[k]

        EDP = {}
        for k, v in Kmer.items():
            EDP[k] = Kmer[k] / H

        outline = ''
        for k, v in EDP.items():
            outline += str(v) + '\t'

        return outline
    return GetKmerEDP_Default()


def GetKmerEDP_Default():
    """kmer entropy density"""
    Kmer = {}
    for aa in _Kmer_list:
        Kmer[aa] = 1e-09

    sum_Kmer = 1.6e-08
    H = 0.0
    for k, v in Kmer.items():
        Kmer[k] /= sum_Kmer
        Kmer[k] = -Kmer[k] * np.log2(Kmer[k])
        H += Kmer[k]

    EDP = {}
    for k, v in Kmer.items():
        EDP[k] = Kmer[k] / H

    outline = ''
    for k, v in EDP.items():
        outline += str(v) + '\t'

    return outline