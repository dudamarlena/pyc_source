# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/gtf_convert.py
# Compiled at: 2017-12-07 17:16:00
# Size of source mod 2**32: 3147 bytes
from __future__ import absolute_import, division, print_function
import os, sys, subprocess as sp, logging, gzip
from intervaltree_bio import GenomeIntervalTree, UCSCTable
logger = logging.getLogger('STAR-SEQR')

def file_exists(fname):
    """Check if a file exists and is non-empty."""
    try:
        return fname and os.path.exists(fname) and os.path.getsize(fname) > 0
    except OSError:
        return False


def gtf_to_genepred(gtf, out_file):
    if file_exists(out_file):
        logger.warning('Skipping gtf_to_genepred as files already exist!')
        return out_file
    cmd = 'gtfToGenePred -allErrors -ignoreGroupsWithoutExons -genePredExt -geneNameAsName2 {gtf} {out_file}'
    sp.check_call(cmd.format(**locals()), shell=True)
    return out_file


def genepred_to_UCSCtable(genepred, out_file):
    if file_exists(out_file):
        logger.warning('Skipping genepred_to_UCSC_table as files already exist!')
        return out_file
    with open(genepred) as (in_handle):
        with gzip.open(out_file, 'wt') as (out_handle):
            counter = -1
            current_item = None
            for l in in_handle:
                item = l.split('\t')[0]
                if current_item != item:
                    current_item = item
                    counter = counter + 1
                out_handle.write('\t'.join([str(counter), l]))

    return out_file


def gtf2tree(gtf_path):
    genepred_annot = os.path.splitext(gtf_path)[0] + '.genePred'
    ucsc_annot = os.path.splitext(gtf_path)[0] + '.UCSCTable.gz'
    gtf_to_genepred(gtf_path, genepred_annot)
    genepred_to_UCSCtable(genepred_annot, ucsc_annot)
    kg = gzip.open(ucsc_annot)
    gtree = GenomeIntervalTree.from_table(fileobj=kg, mode='tx', parser=UCSCTable.ENS_GENE)
    return gtree


def gtf2trxfasta(gtf_path, ref_fasta, txfa_out, cds=False):
    if file_exists(txfa_out):
        logger.warning('Skipping gtf to transcript fasta conversion as files already exist!')
        return
    if cds:
        cmd = [
         'gffread', '-g', ref_fasta, '-x', txfa_out, gtf_path]
    else:
        cmd = [
         'gffread', '-g', ref_fasta, '-w', txfa_out, gtf_path]
    cmd_args = list(map(str, cmd))
    logger.info('*Command: ' + ' '.join(cmd_args))
    try:
        p = sp.Popen(cmd_args, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            logger.debug(stdout)
        if stderr:
            pass
        if p.returncode != 0:
            logger.error('Error: gffread failed', exc_info=True)
            sys.exit(1)
    except OSError as o:
        logger.error('Exception: ' + str(o))
        logger.error('gffread Failed', exc_info=True)
        sys.exit(1)