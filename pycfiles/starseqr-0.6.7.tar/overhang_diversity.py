# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/overhang_diversity.py
# Compiled at: 2017-12-07 17:16:00
from __future__ import absolute_import, division, print_function
import os, logging, numpy as np, starseqr_utils as su
logger = logging.getLogger('STAR-SEQR')

def find_unique_overhangs(reads_fq):
    """get unique overhang reads per sam flag"""
    rfq_gen = su.common.FastqParser(reads_fq)
    res_seqs = set()
    for rfq in rfq_gen:
        res_seqs.add(rfq.sequence)

    res_seq_len = [ len(i) for i in res_seqs ]
    all_min20 = np.sum(i > 20 for i in res_seq_len)
    all_min35 = np.sum(i > 35 for i in res_seq_len)
    return (len(res_seqs), all_min20, all_min35)


def get_diversity(jxn):
    clean_jxn = su.common.safe_jxn(jxn)
    jxn_dir = os.path.join('support', clean_jxn)
    overhang_fq = os.path.join(jxn_dir, 'overhang.fastq')
    overhang_res = find_unique_overhangs(overhang_fq)
    return overhang_res