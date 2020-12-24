# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/run_assembly.py
# Compiled at: 2017-12-07 17:16:00
# Size of source mod 2**32: 4229 bytes
from __future__ import absolute_import, division, print_function
import sys, os, logging, subprocess as sp, re, starseqr_utils as su
logger = logging.getLogger('STAR-SEQR')

def do_velvet(assemdir, fastq, kmer, errlog, *args):
    """ Run velvet with single or multiple fastqs """
    logger.debug('*Running Velvet.')
    velveth_cmd = ['velveth', assemdir, str(kmer), '-short', '-fastq', fastq]
    for ar in args:
        velveth_cmd.extend(['-shortPaired', '-fastq', ar])

    vh_args = list(map(str, velveth_cmd))
    logger.debug('*velveth Command: ' + ' '.join(vh_args))
    try:
        p = sp.Popen(velveth_cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            errlog.write(str(stdout))
        if stderr:
            errlog.write(str(stderr))
        if p.returncode != 0:
            logger.error('Error: velveth failed')
    except OSError as o:
        logger.error('Exception: ' + str(o))
        logger.error('velveth Failed!', exc_info=True)
        sys.exit(1)

    velvetg_cmd = [
     'velvetg', assemdir, '-cov_cutoff', '2']
    vg_args = list(map(str, velvetg_cmd))
    logger.debug('*velvetg Command: ' + ' '.join(vg_args))
    try:
        p = sp.Popen(velvetg_cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            errlog.write(str(stdout))
        if stderr:
            errlog.write(str(stderr))
        if p.returncode != 0:
            logger.error('Error: velvetg failed')
            sys.exit(1)
    except OSError as o:
        logger.error('Exception: ' + str(o))
        logger.error('velvetg Failed!', exc_info=True)
        sys.exit(1)

    records = su.common.fasta_iter(assemdir + '/contigs.fa')
    return records


def get_assembly_info(jxn, as_type):
    clean_jxn = su.common.safe_jxn(jxn)
    jxn_dir = os.path.join('support', clean_jxn)
    fusionfq = os.path.join(jxn_dir, 'transcripts-fusion.fa')
    fusions_list = list(su.common.fasta_iter(fusionfq))
    pairfq = os.path.join(jxn_dir, 'span.fastq')
    junctionfq = os.path.join(jxn_dir, 'split.fastq')
    assembly_list = []
    if as_type == 'velvet':
        errlog = open(os.path.join(jxn_dir, 'assembly_log.txt'), 'w')
        assembly_list = list(do_velvet(os.path.join(jxn_dir, 'assem_pair'), junctionfq, 17, errlog, pairfq))
        errlog.close()
    all_crossing = []
    all_seq = []
    all_len = []
    if len(assembly_list) > 0:
        for assembly in assembly_list:
            as_id, as_seq = assembly
            as_len = as_id.split('_')[3]
            all_seq.append(as_seq)
            all_len.append(as_len)
            as_crossing_fusions = []
            if len(fusions_list) > 0:
                for fusion in fusions_list:
                    fjxn, fside, fusion_name, brk = fusion[0].split('|')
                    brk = int(brk)
                    fusion_seq = fusion[1][brk - 10:brk + 10].upper()
                    fusion_seq_re = re.compile('|'.join(fusion_seq[:i] + '.{0,2}' + fusion_seq[i + 1:] for i in range(len(fusion_seq))))
                    if len(fusion_seq_re.findall(as_seq.upper())) or len(fusion_seq_re.findall(su.common.rc(as_seq).upper())) > 0:
                        as_crossing_fusions.append(fusion_name)
                        continue

                all_crossing.extend(as_crossing_fusions)
                continue

    all_seq = ','.join(list(map(str, all_seq)))
    all_len = ','.join(list(map(str, all_len)))
    all_crossing = ','.join(list(map(str, all_crossing)))
    return (all_seq, all_len, all_crossing)