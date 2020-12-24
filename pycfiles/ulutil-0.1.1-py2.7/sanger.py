# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/sanger.py
# Compiled at: 2014-12-19 21:47:18
from ulutil import exonerate
standard_primers = {'M13R': 'caggaaacagctatgac', 
   'M13F-20': 'gtaaaacgacggccag', 
   'T3': 'attaaccctcactaaaggga', 
   'T7': 'taatacgactcactataggg'}
standard_vectors = {'pCR4-TOPO-left': 'catgattacgccaagctcagaattaaccctcactaaagggactagtcctgcaggtttaaacgaattcgccctt', 
   'pCR4-TOPO-right': 'aagggcgaattcgcggccgctaaattcaattcgccctatagtgagtcgtattacaattca', 
   'pCR4Blunt-TOPO-left': 'catgattacgccaagctcagaattaaccctcactaaagggactagtcctgcaggtttaaacgaattcgccctt', 
   'pCR4Blunt-TOPO-right': 'aagggcgaattcgcggccgctaaattcaattcgccctatagtgagtcgtattacaattca'}

def trimleft(left, read):
    """Align 2 seqs, forcing alignment of right-end of left.
    
                     ...RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR...
    ...LLLLLLLLLLLLLLLLLLLLLLLLLLL  <- (forced aln here)
    
    Uses exonerate.
    """
    cmd = exonerate.ExonerateCommand('findend', 'parsable', 'bestonly')
    rawaln = exonerate.run_exonerate2(cmd, left, read)
    if rawaln == '':
        return read
    aln = exonerate.parse_aln(rawaln)
    if aln['query_len'] != aln['query_aln_end']:
        raise ValueError, 'failed to align right-end of left sequence'
    if aln['query_strand'] != '+':
        raise ValueError, 'query strand has been reversed'
    if aln['target_strand'] != '+':
        raise ValueError, 'target strand has been reversed'
    return read[aln['target_aln_end']:]


def trimright(right, read):
    """Align 2 seqs, forcing alignment of left-end of right.
    
    ...DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD...
        (forced aln here) -> RRRRRRRRRRRRRRRRRRRRRRRRRRRRR...
    
    Uses exonerate.
    """
    cmd = exonerate.ExonerateCommand('findend', 'parsable', 'bestonly')
    rawaln = exonerate.run_exonerate2(cmd, right, read)
    if rawaln == '':
        return read
    aln = exonerate.parse_aln(rawaln)
    if aln['query_aln_begin'] != 0:
        raise ValueError, 'failed to align left-end of right sequence'
    if aln['query_strand'] != '+':
        raise ValueError, 'query strand has been reversed'
    if aln['target_strand'] != '+':
        raise ValueError, 'target strand has been reversed'
    return read[:aln['target_aln_begin']]


def bidirectional_alignment(forward, reverse):
    """Align forward and reverse sequence of bidirectional Sanger reads.
    
    forward and reverse sequences must already be in the same 'sense' (i.e.,
    reverse should be revcomped if necessary so that both strands in alignment
    are '+').
    
    Forces alignment of both ends (right end of forward, and left end of
    reverse).
    
    ...FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                               RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR...
    
    Uses exonerate.
    """
    cmd = exonerate.ExonerateCommand('findend', 'parsable', 'bestonly')
    rawaln = exonerate.run_exonerate2(cmd, forward, reverse)
    aln = exonerate.parse_aln(rawaln)
    if aln['query_strand'] != '+':
        raise ValueError, 'query strand has been reversed'
    if aln['target_strand'] != '+':
        raise ValueError, 'target strand has been reversed'
    if aln['query_len'] != aln['query_aln_end']:
        raise ValueError, 'failed to align right-end of forward sequence'
    if aln['query_aln_begin'] != 0:
        raise ValueError, 'failed to align left-end of right sequence'