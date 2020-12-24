# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/Hexamer.py
# Compiled at: 2019-12-07 22:50:39
# Size of source mod 2**32: 3117 bytes
import os, sys, numpy as np
from .utils import GetFasta
from .utils import Codon2AA2
_AA_list = [
 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
_Di_Codon_list = []
for aa1 in _AA_list:
    for aa2 in _AA_list:
        _Di_Codon_list.append(aa1 + aa2)

_DNA = ['A', 'C', 'G', 'T']
_3mer_list = []
for dna1 in _DNA:
    for dna2 in _DNA:
        for dna3 in _DNA:
            _3mer_list.append(dna1 + dna2 + dna3)

_6mer_list = []
for mer1 in _3mer_list:
    for mer2 in _3mer_list:
        _6mer_list.append(mer1 + mer2)

def HexamerGenerate(seq, logscore_dict):
    """Generate hexamer"""
    hexamer_list = []
    hexamer_score_list = []
    if len(seq) > 3:
        num = len(seq) // 3
        for i in range(0, num - 1):
            tmp = seq[i * 3:(i + 2) * 3]
            hexamer_list.append(tmp)
            if tmp in logscore_dict:
                hexamer_score_list.append(logscore_dict[tmp])
            else:
                hexamer_score_list.append(0)

    return hexamer_score_list


def ReadLogScore(logscore_file):
    """return a dict of logscore"""
    logscore_dict = {}
    with open(logscore_file, 'rU') as (fl):
        for line in fl.readlines():
            line = line.strip()
            logscore_dict[line.split()[0]] = float(line.split()[1])

        return logscore_dict


def MSSL(array, length):
    if len(array) < length:
        print('The array is too short!')
        return -1
    else:
        Subarray = 0
        for i in range(length):
            Subarray += array[i]

        MaxValue = Subarray
        best = MaxValue
        cur = 0
        start = 0
        end = length
        for k in range(length, len(array)):
            Subarray = Subarray + array[k] - array[(k - length)]
            if MaxValue + array[k] > Subarray:
                MaxValue = MaxValue + array[k]
            else:
                MaxValue = Subarray
                cur = k - length + 1
            if MaxValue > best:
                best = MaxValue
                start = cur
                end = k + 1

        return [
         start, end, best]


def MLC(seq, logscore_dict):
    """Hexamer-based-CDS"""
    hexamer_score_list = [HexamerGenerate(seq[i:], logscore_dict) for i in range(3)]
    start_index = [
     0, 0, 0]
    end_index = [0, 0, 0]
    best = [0, 0, 0]
    for i in range(3):
        start_index[i], end_index[i], best[i] = MSSL(hexamer_score_list[i], 3)

    phase = np.argmax(best)
    start = start_index[phase]
    end = end_index[phase]
    mlc_start = start * 3 + phase
    mlc_end = (end + 1) * 3 + phase
    mlc_seq = seq[start * 3 + phase:(end + 1) * 3 + phase]
    average_hexamer_score = best[phase] / (end - start)
    return [
     mlc_seq, average_hexamer_score, mlc_start, mlc_end]


def HexamerScore2(seq, logscore_dict):
    """compute the hexamer score given a sequence"""
    total = 0.0
    log_score = 0.0
    for k in HexamerGenerate(seq, logscore_dict):
        log_score += k
        total += 1

    try:
        return log_score / total
    except:
        return -1