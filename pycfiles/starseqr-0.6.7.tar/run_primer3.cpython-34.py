# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/run_primer3.py
# Compiled at: 2018-04-06 09:49:00
# Size of source mod 2**32: 4571 bytes
from __future__ import absolute_import, division, print_function
import os, logging, primer3, starseqr_utils as su
logger = logging.getLogger('STAR-SEQR')

def runp3(seq_id, sequence, target=None):
    """ can either use ":" in sequence, a base target or choose the middle of a read"""
    if target:
        if target + 30 > len(sequence) or target - 30 < 0:
            return ()
        brk_target = [target - 10, 20]
    else:
        if ':' in sequence:
            mybrk = int(sequence.index(':'))
            sequence = sequence.replace(':', '')
            if mybrk + 30 > len(sequence) or mybrk - 30 < 0:
                return ()
            brk_target = [mybrk - 10, 20]
        else:
            if len(str(sequence)) < 75:
                return ()
            brk_target = [
             int(len(sequence) / 2), 1]
    mydres = {'SEQUENCE_ID': seq_id,  'SEQUENCE_TEMPLATE': sequence, 
     'SEQUENCE_TARGET': brk_target}
    mypres = {'PRIMER_NUM_RETURN': 1, 
     'PRIMER_TASK': 'generic', 
     'PRIMER_PICK_LEFT_PRIMER': 1, 
     'PRIMER_PICK_RIGHT_PRIMER': 1, 
     'PRIMER_PICK_INTERNAL_OLIGO': 1, 
     'PRIMER_OPT_SIZE': 20, 
     'PRIMER_MIN_SIZE': 18, 
     'PRIMER_MAX_SIZE': 27, 
     'PRIMER_OPT_TM': 60.0, 
     'PRIMER_MIN_TM': 55.0, 
     'PRIMER_MAX_TM': 65.0, 
     'PRIMER_OPT_GC_PERCENT': 50, 
     'PRIMER_MIN_GC': 20.0, 
     'PRIMER_MAX_GC': 80.0, 
     'PRIMER_LIBERAL_BASE': 0, 
     'PRIMER_MIN_THREE_PRIME_DISTANCE': 0, 
     'PRIMER_LOWERCASE_MASKING': 0, 
     'PRIMER_MAX_POLY_X': 100, 
     'PRIMER_INTERNAL_MAX_POLY_X': 100, 
     'PRIMER_INTERNAL_MAX_SELF_END': 8, 
     'PRIMER_SALT_MONOVALENT': 50.0, 
     'PRIMER_DNA_CONC': 50.0, 
     'PRIMER_MAX_NS_ACCEPTED': 0, 
     'PRIMER_MAX_SELF_ANY': 12, 
     'PRIMER_MAX_SELF_END': 8, 
     'PRIMER_PAIR_MAX_COMPL_ANY': 12, 
     'PRIMER_PAIR_MAX_COMPL_END': 8, 
     'PRIMER_PAIR_MAX_DIFF_TM': 6, 
     'PRIMER_PRODUCT_SIZE_RANGE': [
                                   [
                                    75, 200]]}
    try:
        p3output = primer3.bindings.designPrimers(mydres, mypres)
        if p3output['PRIMER_PAIR_NUM_RETURNED'] < 1:
            return ()
        p3res = parsep3(p3output)
    except OSError:
        logger.error('Primer Design Failed- continuing', exc_info=True)
        return ()
    except Exception:
        return ()

    return p3res


def parsep3(p3output):
    Lprimer = str(p3output['PRIMER_LEFT_0_SEQUENCE'])
    Rprimer = str(p3output['PRIMER_RIGHT_0_SEQUENCE'])
    return (
     Lprimer.upper(), Rprimer.upper())


def wrap_runp3(jxn, max_trx_fusion, chim_dir):
    """
    use the breakpoint info stored in the fasta file header.
    Design primers using predicted fusion transcripts from expression
    """
    clean_jxn = su.common.safe_jxn(jxn)
    fusionfa = os.path.join(chim_dir, 'transcripts-fusion-' + clean_jxn + '.fa')
    fusions_list = list(su.common.fasta_iter(fusionfa))
    max_trx_fusion = str(max_trx_fusion).split('|')[0]
    if fusions_list and max_trx_fusion:
        for fusion_name, fus_seq in fusions_list:
            jxn, side, fusion_name, brk = fusion_name.split('|')
            if fusion_name == max_trx_fusion:
                try:
                    brk = int(brk)
                    seq_len = len(fus_seq)
                    min_brk = brk - 200 if brk - 200 > 0 else 0
                    max_brk = brk + 200 if brk + 200 < seq_len else seq_len
                    sub_seq = fus_seq[min_brk:max_brk]
                    sub_brk = brk - min_brk
                    p3res = runp3(fusion_name, sub_seq.upper(), sub_brk)
                    return p3res
                except:
                    return ()

                continue

        return ()
    else:
        return ()