# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bryanbriney/git/abtools/abtools/utils/codons.py
# Compiled at: 2017-01-24 13:27:47
codon_lookup = {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S', 
   'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 
   'TAC': 'Y', 'TAA': '*', 'TAG': '*', 'TGT': 'C', 
   'TGC': 'C', 'TGA': '*', 'TGG': 'W', 'CTT': 'L', 
   'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 
   'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'CAT': 'H', 
   'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGT': 'R', 
   'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I', 
   'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'ACT': 'T', 
   'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 
   'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'AGT': 'S', 
   'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GTT': 'V', 
   'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A', 
   'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 
   'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 
   'GGC': 'G', 'GGA': 'G', 'GGG': 'G'}