# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sillymap/index.py
# Compiled at: 2017-04-04 09:38:34
import pickle
from .count_lookup import count_lookup
from .rank_lookup import Rank
from .burrows_wheeler import burrows_wheeler

def index_main(args):
    with open(args.reference, 'r') as (ref_fh):
        reference_seq = ''
        for i, line in enumerate(ref_fh):
            if line.startswith('>'):
                if i != 0:
                    raise ValueError('Silly you, you expect sillymap to accept more than one reference sequence?')
                reference_id = line[1:].strip()
            else:
                reference_seq += line.strip()

    bw, sa_index = burrows_wheeler(reference_seq)
    cl = count_lookup(bw)
    rank = Rank()
    rank.add_text(bw)
    ref_output = ('{}.silly').format(args.reference)
    with open(ref_output, 'wb') as (pickle_fh):
        pickle.dump((cl, rank, bw, sa_index), pickle_fh)