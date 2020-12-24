# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/fluas/crossover_contamination.py
# Compiled at: 2018-05-04 16:38:01
# Size of source mod 2**32: 4821 bytes
import logging, os, pandas as pd
from collections import Counter
from contextlib import contextmanager
from .fastx import combine_fastas
from .utils import file_exists, runcmd
logger = logging.getLogger(__name__)

@contextmanager
def bwa_index(reference, options=None):
    """Builds an index using `bwa index`.

    Args:
        reference (str): file path of reference fasta
        options (Optional[str]): options passed to bwa index, eg. "-a is"

    Yields:
        str: file path of reference as it's used as the prefix in `bwa index`
    """
    ref = os.path.abspath(reference)
    idx_files = [ref + x for x in ('.amb', '.ann', '.bwt', '.pac', '.sa')]
    if not file_exists(idx_files):
        logger.debug('Creating BWA index for %s' % ref)
        cmd = 'bwa index {options}{reference}'.format(options=(options + ' ' if options else ''),
          reference=reference)
        runcmd(cmd)
    yield reference


def bwa_to_small_reference(fastq, references, out_file, threads=8, overlap=0.95, identity=0.95):
    """Align fastq to each reference saving read names that map and counts to which reference
    a read maps to.

    Args:
        fastq (str): file path of fastq to be checked for contamination
        references (list): list of reference fasta file paths
        out_file (str): file path for readname:referencename hits to be written
        threads (Optional[int]): number of threads to utilize during mapping
        overlap (Optional[float]): fraction of overlap when mapping sequence to reference
        identity (Optional[float]): fraction of matching bases in passing alignment

    Returns:
        collections.Counter: reference_name:count
    """
    logger.debug('bwa small reference on %s' % fastq)
    d_identity = 1.0 - identity
    reference_hits = Counter()
    seedlen = 100
    tmp_fasta = combine_fastas(references)
    with bwa_index(tmp_fasta, '-a is') as (bwaidx):
        with open(out_file, 'w') as (hits_file):
            cmd = 'bwa mem -t {threads} -k {seedlen} -a {index} {fastq} 2> {devnull} | samtools view -F 4 - 2> {devnull}'.format(threads=threads,
              seedlen=seedlen,
              index=bwaidx,
              fastq=fastq,
              devnull=(os.devnull))
            for aln in runcmd(cmd, iterable=True):
                try:
                    observed_mismatches = int(aln.split('NM:i:')[1][0])
                    toks = aln.rstrip('\r\n').split('\t')
                    ref_name = toks[2].partition('|')[0]
                    matching = float(toks[5].split('M')[0])
                    seqlen = len(toks[9])
                except ValueError:
                    continue

                if observed_mismatches / seqlen <= d_identity and matching / seqlen >= overlap:
                    name = toks[0]
                    print(name, ref_name, sep=',', file=hits_file)
                    reference_hits.update([ref_name])

    return reference_hits


def reference_contamination_check(fastq, stats_file, hits_file, references, threads=8, overlap=0.95, identity=0.99):
    """Align reads against all references, flagging contaminant reads,
    and generating a stats table of:
    Sample,Reference1,Reference2
    sample1,0,10

    Args:
        fastq (str): fastq file paths
        stats_file (str): Alignment stats per reference as CSV
        hits_file (str): Text file of READNAME:REFERENCE name per passing alignment
        references (list): list of reference fasta file paths
        threads (Optional[int]): number of threads to use during alignment
        overlap (Optional[float]): fraction of overlap required when mapping sequence to reference
        identity (Optional[float]): fraction of matching bases in passing alignment

    Returns:
        tuple: path of stats_file, path of hits_file
    """
    fastq = os.path.abspath(fastq)
    logger.debug('Running reference contamination check on %s' % fastq)
    reference_hits = bwa_to_small_reference(fastq, references, hits_file, threads, overlap, identity)
    sample_name = os.path.basename(fastq).partition('_')[0]
    df = pd.DataFrame(reference_hits, index=[sample_name])
    df.to_csv(stats_file, index_label='Sample')
    return (stats_file, hits_file)