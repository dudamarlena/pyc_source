# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/clareau/dat/Research/BuenrostroResearch/lareau_dev/bap/bap/barcode/modes/barcodeHelp.py
# Compiled at: 2019-11-09 17:44:20
# Size of source mod 2**32: 1490 bytes
import os, re, regex, sys, gzip
from itertools import repeat
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzysearch import find_near_matches

def batch_iterator(iterator, batch_size):
    """
        Returns lists of tuples of length batch_size.
        """
    entry = True
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.__next__()
            except StopIteration:
                entry = None

            if entry is None:
                break
            batch.append(entry)

        if batch:
            yield batch


def chunk_writer_gzip(filename, what):
    """
        Basic function to write a chunk of a fastq file
        to a gzipped file
        """
    with gzip.open(filename, 'wt') as (out_write):
        out_write.writelines(what)
    return filename


def prove_barcode_simple(bc, valid_set):
    """
        Function that takes a putative barcode and returns the nearest valid one
        """
    if bc in valid_set:
        return bc
    else:
        return 'NA'


def prove_barcode(bc, valid_set, n_mismatch):
    """
        Function that takes a putative barcode and returns the nearest valid one
        """
    if bc in valid_set:
        return (bc, '0')
    else:
        eo = process.extractOne(bc, valid_set)
        if eo[1] >= (len(bc) - n_mismatch) / len(bc) * 100:
            return (
             eo[0], '1')
        return ('N' * len(bc), '0')


def formatRead(title, sequence, quality):
    """
        Takes three components of fastq file and stiches them together in a string
        """
    return '@%s\n%s\n+\n%s\n' % (title, sequence, quality)