# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lkalan/my_python-2.7.5/lib/python2.7/site-packages/decontamlib/sam.py
# Compiled at: 2016-01-13 15:33:38
import pysam

def get_mapped_reads(fp, min_pct_id, min_len_frac):
    sam = pysam.AlignmentFile(fp)
    for read in sam:
        if read.is_unmapped:
            yield (
             read.query_name, read.is_read1, None)
        elif _get_frac(read) < min_len_frac:
            yield (
             read.query_name, read.is_read1, None)
        else:
            pct_id = _get_pct_identity(read)
            if pct_id < min_pct_id:
                yield (
                 read.query_name, read.is_read1, None)
            else:
                ref_id = sam.getrname(read.reference_id)
                yield (read.query_name, read.is_read1, ref_id)

    return


def _get_pct_identity(read):
    if read.has_tag('NM'):
        edit_dist = read.get_tag('NM')
    else:
        edit_dist = 0
    pct_mm = float(edit_dist) / read.alen
    return 1 - pct_mm


def _get_frac(read):
    cigar = read.cigartuples
    clip = 0
    for pair in cigar:
        if pair[0] == 4 or pair[0] == 5:
            clip = clip + pair[1]

    frac = float(read.query_alignment_length) / (read.query_alignment_length + clip)
    return frac