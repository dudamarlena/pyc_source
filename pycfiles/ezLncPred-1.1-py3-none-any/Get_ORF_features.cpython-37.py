# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/PredLnc_GFStack/src/get_features_module/Get_ORF_features.py
# Compiled at: 2019-09-05 08:38:59
# Size of source mod 2**32: 5791 bytes
import numpy as np, pandas as pd, os
from Bio import SeqIO
import sys

class ExtractORF:

    def __init__(self, seq):
        self.seq = seq.upper()
        self.result = ['+', 0, 0, 0, 0]
        self.summary = []
        self.winner = 0
        self.longest_orf = ['+', 0, 0, 0, 0]
        self.first_orf = ['+', 0, 0, 0, 0]

    def _reverse_comp(self):
        swap = {'A':'T', 
         'T':'A',  'C':'G',  'G':'C',  'N':'N',  'X':'X'}
        return ''.join((swap[b] for b in self.seq))[::-1]

    def codons(self, frame):
        """ A generator that yields DNA in one codon blocks 
    
    "frame" counts for 0. This function yelids a tuple (triplet, index) with 
    index relative to the original DNA sequence 
    """
        start = frame
        while start + 3 <= len(self.seq):
            yield (
             self.seq[start:start + 3], start)
            start += 3

    def run_one(self, frame_number, start_coden, stop_coden):
        """ Search in one reading frame """
        codon_gen = self.codons(frame_number)
        start_codens = start_coden
        stop_codens = stop_coden
        while 1:
            try:
                c, index = codon_gen.__next__()
            except StopIteration:
                break

            if not c in start_codens:
                if start_codens or c not in stop_codens:
                    orf_start = index
                    end = False
                    while True:
                        try:
                            c, index = codon_gen.__next__()
                        except StopIteration:
                            end = True
                            integrity = -1

                        if c in stop_codens:
                            end = True
                            integrity = 1
                        if end:
                            orf_end = index + 3
                            L = orf_end - orf_start
                            if frame_number == 0:
                                self.first_orf = [
                                 frame_number + 1, orf_start, orf_end, L, integrity]
                            if L > self.winner:
                                self.winner = L
                                self.longest_orf = [frame_number + 1, orf_start, orf_end, L, integrity]
                            if L == self.winner:
                                if orf_start < self.longest_orf[1]:
                                    self.winner = L
                            self.result = [
                             frame_number + 1, orf_start, orf_end, L, integrity]
                            break

        self.summary.append(self.result)

    def get_orf(self, start_coden=[
 'ATG'], stop_coden=['TAG', 'TAA', 'TGA']):
        for frame in range(3):
            self.run_one(frame, start_coden, stop_coden)

        return list(self.summary)


def extract_feature_from_seq(seq, stt, stp):
    """extract features of sequence from fasta entry"""
    stt_coden = stt.strip().split(',')
    stp_coden = stp.strip().split(',')
    transtab = str.maketrans('ACGTNX', 'TGCANX')
    mRNA_seq = seq.upper()
    tmp = ExtractORF(mRNA_seq)
    all_orf = tmp.get_orf(start_coden=stt_coden, stop_coden=stp_coden)
    first_orf = tmp.first_orf
    longest_orf = tmp.longest_orf
    return (all_orf, first_orf, longest_orf)


start_codons = 'ATG'
stop_codons = 'TAG,TAA,TGA'
Coverage = 0
names = ['A', 'G', 'C', 'T', 'AA', 'AAA', 'AAC', 'AAG', 'AAT', 'AC', 'ACA', 'ACC', 'ACG', 'ACT', 'AG', 'AGA',
 'AGC', 'AGG', 'AGT', 'AT', 'ATA', 'ATC', 'ATG', 'ATT', 'CA', 'CAA', 'CAC', 'CAG',
 'CAT', 'CC', 'CCA', 'CCC', 'CCG', 'CCT', 'CG', 'CGA', 'CGC', 'CGG', 'CGT', 'CT',
 'CTA', 'CTC', 'CTG', 'CTT', 'GA', 'GAA', 'GAC', 'GAG', 'GAT', 'GC', 'GCA', 'GCC',
 'GCG', 'GCT', 'GG', 'GGA', 'GGC', 'GGG', 'GGT', 'GT', 'GTA', 'GTC', 'GTG', 'GTT',
 'TA', 'TAA', 'TAC', 'TAG', 'TAT', 'TC', 'TCA', 'TCC', 'TCG', 'TCT', 'TG', 'TGA',
 'TGC', 'TGG', 'TGT', 'TT', 'TTA', 'TTC', 'TTG', 'TTT']

def ORF_features(seq):
    all_orf, first_orf, longest_orf = extract_feature_from_seq(seq=seq, stt=start_codons, stp=stop_codons)
    mRNA_size = len(seq)
    first_orf_len = first_orf[3]
    first_orf_Rlen = float(first_orf[3]) / float(mRNA_size)
    longest_orf_len = longest_orf[3]
    longest_orf_Rlen = float(longest_orf[3]) / float(mRNA_size)
    integrity = longest_orf[4]
    if all_orf[0] == ['+', 0, 0, 0, 0]:
        if all_orf[1] != ['+', 0, 0, 0, 0]:
            all_orf[0] = all_orf[1]
        else:
            all_orf[0] = all_orf[2]
            all_orf[1] = all_orf[2]
    ORF_frame_score = ((all_orf[0][3] - all_orf[1][3]) ** 2 + (all_orf[0][3] - all_orf[2][3]) ** 2 + (all_orf[1][3] - all_orf[2][3]) ** 2) / 2
    reading_frame_1 = str(seq[all_orf[0][1]:all_orf[0][2] + 1])
    reading_frame_2 = str(seq[all_orf[1][1]:all_orf[1][2] + 1])
    reading_frame_3 = str(seq[all_orf[2][1]:all_orf[2][2] + 1])
    longest_orf = str(seq[longest_orf[1]:longest_orf[2] + 1])
    ORF_kmers = [longest_orf.count(x) / (longest_orf_len + 1) for x in names]
    return (mRNA_size, first_orf_len, first_orf_Rlen, longest_orf_len, longest_orf_Rlen, integrity, ORF_frame_score, reading_frame_1, reading_frame_2, reading_frame_3, ORF_kmers)