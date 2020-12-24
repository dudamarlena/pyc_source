# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sillymap/mapper.py
# Compiled at: 2017-04-04 09:38:27
from .backwards_search import backwards_search
import pickle

def mapper_main(args):
    ref_output = ('{}.silly').format(args.reference)
    with open(ref_output, 'rb') as (ref_fh):
        count_lookup, rank, burrows_wheeler, sa_index = pickle.load(ref_fh)
    total_length = len(sa_index)
    with open(args.reads) as (reads_fh):
        for i, line in enumerate(reads_fh):
            if i % 4 == 0:
                read_id = line.strip()[1:]
            if i % 4 == 1:
                line = line.strip()
                s, e = backwards_search(line, count_lookup, rank, total_length)
                if s <= e:
                    print ('{},{}').format(read_id, sa_index[s])