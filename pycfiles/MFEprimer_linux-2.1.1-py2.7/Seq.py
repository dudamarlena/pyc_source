# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MFEprimer/chilli/Seq.py
# Compiled at: 2017-07-16 05:34:29
"""
A class for manuplating biological sequences

Usage:

    import Seq
    s = 'CGTTGA'
    print s
    print Seq.Seq(s).com
    print Seq.Seq(s).revcom

by Wubin Qu <quwubin@gmail.com>
Copyright @ 2010, All Rights Reserved.
"""
Author = 'Wubin Qu <quwubin@gmail.com>, BIRM, China'
Date = '2010-3-2'
License = 'GPL v3'
Version = '1.0'
ambiguous_dna_complement = {'a': 't', 
   'c': 'g', 
   'g': 'c', 
   't': 'a', 
   'A': 'T', 
   'C': 'G', 
   'G': 'C', 
   'T': 'A', 
   'M': 'K', 
   'm': 'k', 
   'R': 'Y', 
   'r': 'y', 
   'W': 'W', 
   'w': 'w', 
   'S': 'S', 
   's': 's', 
   'Y': 'R', 
   'y': 'r', 
   'K': 'M', 
   'k': 'm', 
   'V': 'B', 
   'v': 'b', 
   'H': 'D', 
   'h': 'd', 
   'D': 'H', 
   'd': 'h', 
   'B': 'V', 
   'b': 'v', 
   'X': 'X', 
   'x': 'x', 
   'N': 'N', 
   'n': 'n', 
   '-': '-'}

def complement(seq):
    """Return the complement sequence"""
    return ('').join([ ambiguous_dna_complement[base] for base in seq ])


def reverse(seq):
    """Reverses a string given to it."""
    return seq[::-1]


def rev_com(seq):
    """Return the reverse_complement sequence"""
    com = complement(seq)
    rev_com = reverse(com)
    return rev_com


if __name__ == '__main__':
    pass