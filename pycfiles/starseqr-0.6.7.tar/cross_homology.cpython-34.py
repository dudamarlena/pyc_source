# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/cross_homology.py
# Compiled at: 2017-12-07 17:16:00
# Size of source mod 2**32: 2194 bytes
from __future__ import absolute_import, division, print_function
import os, logging, ssw, numpy as np, starseqr_utils as su
logger = logging.getLogger('STAR-SEQR')

def run_crosshom_ssw(reads_fq, trxleft_fa, trxright_fa):
    """get sw score for left and right gene"""
    aligner = ssw.Aligner(gap_open=12, gap_extend=4)
    rfq_gen = su.common.FastqParser(reads_fq)
    matches = []
    for rfq in (x for _, x in zip(range(500), rfq_gen)):
        l_max = 0
        r_max = 0
        if rfq.seq_len <= 20:
            matches.append(0)
        trxl_gen = su.common.fasta_iter(trxleft_fa)
        trxr_gen = su.common.fasta_iter(trxright_fa)
        for trxl_id, trxl_seq in trxl_gen:
            rfql_align = aligner.align(reference=rfq.sequence, query=trxl_seq)
            l_max = max(rfql_align.score, l_max)

        for trxr_id, trxr_seq in trxr_gen:
            rfqr_align = aligner.align(reference=rfq.sequence, query=trxr_seq)
            r_max = max(rfqr_align.score, r_max)

        read_norm = min(l_max, r_max) / (rfq.seq_len * 2)
        matches.append(read_norm)

    if len(matches) > 0:
        return float('{0:.3f}'.format(np.sum(i > 0.5 for i in matches) / len(matches)))
    else:
        return 0


def get_cross_homology(jxn, chim_dir):
    paired_res = None
    overhang_res = None
    clean_jxn = su.common.safe_jxn(jxn)
    jxn_dir = os.path.join('support', clean_jxn)
    trans_left_fa = os.path.join(chim_dir, 'transcripts-left-' + clean_jxn + '.fa')
    trans_right_fa = os.path.join(chim_dir, 'transcripts-right-' + clean_jxn + '.fa')
    paired_fq = os.path.join(jxn_dir, 'span.fastq')
    overhang_fq = os.path.join(jxn_dir, 'overhang.fastq')
    paired_res = run_crosshom_ssw(paired_fq, trans_left_fa, trans_right_fa)
    overhang_res = run_crosshom_ssw(overhang_fq, trans_left_fa, trans_right_fa)
    return (paired_res, overhang_res)