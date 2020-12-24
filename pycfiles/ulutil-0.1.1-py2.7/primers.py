# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/primers.py
# Compiled at: 2014-12-19 21:46:55
from ulutil import oligoTm, unafold, seqtools

def generate_candidates(seq, minlen=18, maxlen=30):
    candidates = []
    for start in xrange(len(seq)):
        length = minlen
        while length <= maxlen and start + length <= len(seq):
            candidates.append(seq[start:start + length])
            length += 1

    return candidates


def choose_PCR_primer(seq, target_Tm=62.0):
    candidates = generate_candidates(seq)
    candidates = filter(lambda s: abs(oligoTm.oligoTm(s) - target_Tm) <= 2, candidates)
    if len(candidates) == 0:
        raise ValueError, 'No primer candidates meet Tm cutoffs'
    candidates = filter(lambda s: abs(seqtools.gc_content(s) - 0.5) <= 0.1, candidates)
    if len(candidates) == 0:
        raise ValueError, 'No primer candidates meet GC content cutoffs'
    candidates.sort(key=unafold.hybrid_ss_min)
    return candidates[0]