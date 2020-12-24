# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wisestork/gc.py
# Compiled at: 2019-06-13 09:35:55
# Size of source mod 2**32: 1530 bytes
"""
wisestork.gc
~~~~~~~~~~
:copyright: (c) 2016-2019 Sander Bollen
:license: GPL-3.0
"""
from Bio.SeqUtils import GC

def get_gc_for_bin(fasta, chromosome, bin):
    """
    Get number of GC bases in a region
    :param fasta: an instance of pyfaidx.Fasta
    :param chromosome: chromosome name
    :param bin: Bin namedtuple
    :return: integer
    """
    perc = GC(fasta[chromosome][bin.start:bin.end].seq)
    dist = bin.end - bin.start
    return int(perc * dist / 100)


def get_n_per_bin(fasta, chromosome, bin):
    """
    Get number of N bases in a region
    :param fasta: an instance of pyfaidx.Fasta
    :param chromosome: chromosome name
    :param bin: Bin namedtuple
    :return: integer
    """
    return fasta[chromosome][bin.start:bin.end].seq.upper().count('N')