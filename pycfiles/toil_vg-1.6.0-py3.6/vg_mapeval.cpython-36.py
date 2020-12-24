# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_mapeval.py
# Compiled at: 2020-04-30 13:47:21
# Size of source mod 2**32: 146660 bytes
"""
vg_mapeval.py: Compare alignment positions from gam or bam to a truth set
that was created with vg sim --gam

"""
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, struct, socket, threading, string, math, getpass, pdb, gzip, logging, copy
from collections import Counter
from math import ceil
from subprocess import Popen, PIPE
from functools import reduce
try:
    import numpy as np
    from sklearn.metrics import roc_auc_score, average_precision_score, r2_score, roc_curve
    have_sklearn = True
except:
    have_sklearn = False

import tsv
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import require, make_url, remove_ext, add_common_vg_parse_args, add_container_tool_parse_args, get_vg_script, run_concat_lists, parse_plot_sets, title_to_filename, ensure_disk, run_concat_files, AsyncImporter, set_r_cran_url
from toil_vg.vg_map import map_parse_args, run_split_reads_if_needed, run_mapping
from toil_vg.vg_index import run_indexing, run_bwa_index, run_minimap2_index
from toil_vg.context import Context, run_write_info_to_outstore
logger = logging.getLogger(__name__)

def mapeval_subparser(parser):
    """
    Create a subparser for mapeval.  Should pass in results of subparsers.add_parser()
    """
    Job.Runner.addToilOptions(parser)
    parser.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    add_mapeval_options(parser)
    add_container_tool_parse_args(parser)


def add_mapeval_options(parser):
    """
    Add the mapeval options to the given argparse parser.
    """
    parser.add_argument('--truth', type=make_url, default=None, help='list of true positions of reads as output by toil-vg sim (by default positions extracted from --gam_input_reads or --bam_input_reads)')
    parser.add_argument('--skip-eval', action='store_true', help='skip evaluation, ignore --truth, and just map reads')
    parser.add_argument('--gams', nargs='+', type=make_url, default=[], help='aligned reads to compare to truth.  specify xg index locations with --index-bases')
    parser.add_argument('--index-bases', nargs='+', type=make_url, default=[], help='use in place of gams to perform alignment.  will expect <index-base>.gcsa, <index-base>.lcp and <index-base>.xg to exist.Provide a comma-separated pair to use the first index for alignment and the second (.xg only) for annotation in the comparison')
    parser.add_argument('--use-gbwt', action='store_true', help='Use the GBWT during alignment with map or mpmap, if available')
    parser.add_argument('--gbwt-penalties', nargs='+', type=float, default=[], help='when using the GBWT, try all of the given recombination penalties instead of the default')
    parser.add_argument('--strip-gbwt', action='store_true', help='run gbwt-free control runs')
    parser.add_argument('--use-snarls', action='store_true', help='also import <index-base>.snarls and use it during multipath alignment')
    parser.add_argument('--strip-snarls', action='store_true', help='run snarls-free control runs')
    parser.add_argument('--vg-graphs', nargs='+', type=make_url, default=[], help='vg graphs to use in place of gams or indexes.  indexes will be built as required')
    parser.add_argument('--gam-names', nargs='+', default=[], help='a name for each gam passed in --gams/graphs/index-bases')
    parser.add_argument('--bams', nargs='+', type=make_url, default=[], help='aligned reads to compare to truth in BAM format')
    parser.add_argument('--bam-names', nargs='+', default=[], help='a name for each bam passed in with --bams')
    parser.add_argument('--pe-bams', nargs='+', type=make_url, default=[], help='paired end aligned reads to compare to truth in BAM format')
    parser.add_argument('--pe-bam-names', nargs='+', default=[], help='a name for each bam passed in with --pe-bams')
    parser.add_argument('--paired-only', action='store_true', help='only do paired-end alignment (default is to do single and paired)')
    parser.add_argument('--single-only', action='store_true', help='only do single-end alignment (default is to do single and paired)')
    parser.add_argument('--mapeval-threshold', type=int, default=200, help='distance between alignment and true position to be called correct')
    parser.add_argument('--bwa', action='store_true', help='run bwa mem on the reads, and add to comparison')
    parser.add_argument('--bwa-opts', type=str, help='arguments for bwa mem (wrapped in "").')
    parser.add_argument('--minimap2', action='store_true', help='run minimap2 on the reads, and add to comparison')
    parser.add_argument('--minimap2-opts', type=str, help='arguments for minimap2 (wrapped in "").')
    parser.add_argument('--fasta', type=make_url, default=None, help='fasta sequence file (required for bwa or minimap2. If .fa.* indexes exists for this file, they will be used)')
    parser.add_argument('--compare-gam-scores', default=None, help='compare scores against those in the given named GAM')
    parser.add_argument('--gbwt-baseline', default=None, help='use GBWT scoring status in the given named GAM like snp1kg-gbwt5.0-mp-pe as a tag on all reads')
    parser.add_argument('--downsample', type=float, default=None, help='downsample alignment files to the given portion of reads for evaluation')
    parser.add_argument('--ignore-quals', action='store_true', help='never use quality adjusted alignment. necessary if using mpmap on reads not from trained simulator')
    parser.add_argument('--mappers', nargs='+', default=['map'], choices=['map', 'mpmap', 'gaffe'], help='run the specified mappers, from "map", "mpmap", and "gaffe"')
    parser.add_argument('--multipath', action='store_const', dest='mappers', const=['map', 'mpmap'], help='run mpmap and map')
    parser.add_argument('--multipath-only', action='store_const', dest='mappers', const=['mpmap'], help='run only mpmap')
    parser.add_argument('--more-mpmap-opts', nargs='+', default=[], help='additional batches of mpmap options to try')
    parser.add_argument('--gam-input-xg', type=make_url, default=None, help='If extracting truth positions from --gam_input_reads, specify corresponding xg for annotation')
    parser.add_argument('--plot-sets', nargs='+', default=[], help='comma-separated lists of condition-tagged GAM names (primary-mp-pe, etc.) with colon-separated title prefixes')
    map_parse_args(parser)
    add_common_vg_parse_args(parser)


def get_default_mapeval_options():
    """
    Return an argparse Namespace populated with the default mapeval option
    values.
    
    Requires the required positional truth file argument.
    
    Can be modified and then passed to make_mapeval_plan(), so you can use
    mapeval as part of a larger program.
    
    """
    parser = argparse.ArgumentParser()
    add_mapeval_options(parser)
    return parser.parse_args([])


def validate_options(options):
    """
    Throw an error if an invalid combination of options has been selected.
    """
    input_count = sum([x is not None for x in [options.gam_input_reads, options.bam_input_reads, options.fastq]])
    require(input_count <= 1, 'no more than one of --gam_input_reads, --fastq, or --bam_input_reads allowed for input')
    require(options.gams != [] or input_count > 0, 'either --gams must be specified with pre-aligned GAM files, or one of --gam_input_reads, --fastq, or --bam_input_reads must give reads to align')
    require(not options.fastq or options.truth or options.skip_eval, '--truth (or --skip-eval) required with --fastq input')
    require(not options.fastq or len(options.fastq) in (1, 2), 'only 1 or two fastqs accepted with --fatsq')
    require(not options.fastq or all([x.endswith('.gz') for x in options.fastq]), 'only gzipped fastqs (ending with .gz) accepted by --fastq')
    if options.bwa:
        require(options.fasta, '--fasta required for bwa')
    if options.minimap2:
        require(options.fasta, '--fasta required for minimap2')
    if options.bams:
        require(options.bam_names and len(options.bams) == len(options.bam_names), '--bams and --bam-names must have same number of inputs')
    if options.pe_bams:
        require(options.pe_bam_names and len(options.pe_bams) == len(options.pe_bam_names), '--pe-bams and --pe-bam-names must have same number of inputs')
    require(not options.interleaved, '--interleaved disabled in toil-vg mapeval; a single --fastq is always assumed interleaved and two are always assumed paired')
    require(options.gams or options.index_bases or options.vg_graphs, 'one of --vg-graphs, --index-bases or --gams must be used to specifiy vg input')
    require(not options.gbwt_penalties or len(set(options.gbwt_penalties)) == len(options.gbwt_penalties), '--gbwt-penalties valuses must be unique')
    if options.use_snarls:
        require('mpmap' in options.mappers, '--use-snarls only affects the mpmap mapper')
    if options.strip_snarls:
        require(options.use_snarls, '--strip-snarls only makes sense with --use-snarls')
    if options.gams:
        require(len(options.index_bases) == len(options.gams), '--index-bases must be used along with --gams to specify xg locations')
    if options.vg_graphs:
        require(not options.gams and not options.index_bases, 'if --vg-graphs specified, --gams and --index-bases must not be used')
        require('gaffe' not in options.mappers, '--vg-graphs cannot be used with gaffe because gaffe needs a GBWT')
    if options.gams:
        require(options.gam_names and len(options.gams) == len(options.gam_names), '--gams and --gam-names must have same number of inputs')
    if options.vg_graphs:
        require(options.gam_names and len(options.vg_graphs) == len(options.gam_names), '--vg-graphs and --gam-names must have same number of inputs')
    if options.index_bases:
        require(options.gam_names and len(options.index_bases) == len(options.gam_names), '--index-bases and --gam-names must have same number of inputs')
    names = []
    if options.bam_names:
        names += options.bam_names
    if options.pe_bam_names:
        names += options.pe_bam_names
    if options.gam_names:
        names += options.gam_names
    require(len(names) == len(set(names)), 'all names must be unique')
    require(options.gam_input_reads is None or options.bam_input_reads is None, '--gam_input_reads and --bam_input_reads cannot both be specified')
    require(options.truth or options.skip_eval or options.bam_input_reads or options.gam_input_xg, '--gam-input-xg must be provided to annotate reads, or reads must be input in BAM format or with associated truth')
    require(options.gbwt_baseline is None or options.downsample is None or options.downsample == 1.0, '--gam-baseline cannot be used with --downsample until downsampling is properly deterministic')


def parse_int(value):
    """
    Parse an int, interpreting an empty string as 0.
    """
    if value.strip() != '':
        return int(value)
    else:
        return 0


def run_bam_to_fastq(job, context, bam_file_id, paired_mode, add_paired_suffix=False):
    """
    convert a bam to fastq (or pair of fastqs).  add_suffix will stick a _1 or _2 on
    paired reads (needed for vg, but not bwa or minimap2)
    
    Note that even turning off paired_mode may not dissuade minimap2 from pairing up your reads.
    """
    RealtimeLogger.info('Make FASTQ from BAM id {}'.format(bam_file_id))
    work_dir = job.fileStore.getLocalTempDir()
    bam_file = os.path.join(work_dir, 'input.bam')
    job.fileStore.readGlobalFile(bam_file_id, bam_file)
    if paired_mode:
        sim_fq_files = [
         os.path.join(work_dir, 'sim_1{}.fq'.format('s' if add_paired_suffix else '')),
         os.path.join(work_dir, 'sim_2{}.fq'.format('s' if add_paired_suffix else ''))]
        cmd = ['samtools', 'fastq', os.path.basename(bam_file),
         '-1', os.path.basename(sim_fq_files[0]),
         '-2', os.path.basename(sim_fq_files[1])]
        if add_paired_suffix:
            cmd += ['-N']
        else:
            cmd += ['-n']
        context.runner.call(job, cmd, work_dir=work_dir)
        gzip_cmd = [
         [
          'sed', os.path.basename(sim_fq_files[0]), '-e', 's/\\/1/_1/g'], ['gzip', '-c']]
        with open(sim_fq_files[0] + '.gz', 'wb') as (gz_file):
            context.runner.call(job, gzip_cmd, work_dir=work_dir, outfile=gz_file)
        gzip_cmd = [
         [
          'sed', os.path.basename(sim_fq_files[1]), '-e', 's/\\/2/_2/g'], ['gzip', '-c']]
        with open(sim_fq_files[1] + '.gz', 'wb') as (gz_file):
            context.runner.call(job, gzip_cmd, work_dir=work_dir, outfile=gz_file)
        return [context.write_intermediate_file(job, sim_fq_files[0] + '.gz'),
         context.write_intermediate_file(job, sim_fq_files[1] + '.gz')]
    else:
        sim_fq_file = os.path.join(work_dir, 'sim.fq.gz')
        cmd = [['samtools', 'fastq', os.path.basename(bam_file), '-N']]
        cmd.append(['sed', '-e', 's/\\/1/_1/g', '-e', 's/\\/2/_2/g'])
        cmd.append(['gzip'])
        with open(sim_fq_file, 'wb') as (sim_file):
            context.runner.call(job, cmd, work_dir=work_dir, outfile=sim_file)
        return [
         context.write_intermediate_file(job, sim_fq_file)]


def run_gam_to_fastq(job, context, gam_file_id, paired_mode, add_paired_suffix=False, out_name='sim', out_store=False):
    """
    convert a gam to fastq (or pair of fastqs)
    """
    RealtimeLogger.info('Make FASTQ from GAM id {}'.format(gam_file_id))
    work_dir = job.fileStore.getLocalTempDir()
    gam_file = os.path.join(work_dir, 'input.gam')
    job.fileStore.readGlobalFile(gam_file_id, gam_file)
    write_fn = context.write_output_file if out_store else context.write_intermediate_file
    if paired_mode:
        json_file = gam_file + '.json'
        cmd = ['vg', 'view', '-a', os.path.basename(gam_file)]
        with open(json_file, 'wb') as (out_json):
            context.runner.call(job, cmd, work_dir=work_dir, outfile=out_json)
        sim_fq_files = [None, os.path.join(work_dir, '{}_1{}.fq.gz'.format(out_name, 's' if add_paired_suffix else '')),
         os.path.join(work_dir, '{}_2{}.fq.gz'.format(out_name, 's' if add_paired_suffix else ''))]
        for i in (1, 2):
            cmd = [
             'jq', '-cr', 'select(.name | test("_{}$"))'.format(i),
             os.path.basename(json_file)]
            end_file = json_file + '.{}'.format(i)
            with open(end_file, 'wb') as (end_out):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=end_out)
            cmd = [['vg', 'view', '-JaG', os.path.basename(end_file)]]
            cmd.append(['vg', 'view', '-X', '-'])
            if not add_paired_suffix:
                cmd.append(['sed', 's/_{}$//'.format(i)])
            cmd.append(['gzip'])
            with open(sim_fq_files[i], 'wb') as (sim_out):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=sim_out)
            os.remove(end_file)

        return [
         write_fn(job, sim_fq_files[1]), write_fn(job, sim_fq_files[2])]
    else:
        extracted_reads_file = os.path.join(work_dir, '{}.fq.gz'.format(out_name))
        cmd = [['vg', 'view', '-X', os.path.basename(gam_file)]]
        cmd.append(['gzip'])
        with open(extracted_reads_file, 'wb') as (out_ext):
            context.runner.call(job, cmd, work_dir=work_dir, outfile=out_ext)
        return [write_fn(job, extracted_reads_file)]


def run_concat_fastqs(job, context, fq_reads_ids):
    """ concatenate some fastq files
    """
    RealtimeLogger.info('Concatenate {} FASTQs'.format(len(fq_reads_ids)))
    work_dir = job.fileStore.getLocalTempDir()
    assert len(fq_reads_ids) == 2
    fq_file_names = [os.path.join(work_dir, 'reads-{}.fq.gz'.format(i)) for i in range(len(fq_reads_ids))]
    for fq_id, fq_name in zip(fq_reads_ids, fq_file_names):
        job.fileStore.readGlobalFile(fq_id, fq_name, mutable=(fq_name == fq_file_names[0]))

    with open(fq_file_names[0], 'a') as (out_file):
        for fq_name in fq_file_names[1:]:
            with open(fq_name) as (fq_file):
                shutil.copyfileobj(fq_file, out_file)

    return context.write_intermediate_file(job, fq_file_names[0])


def run_strip_fq_ext(job, context, fq_reads_ids):
    """ bwa can't read reads with _1 _2 extensions for paired end alignment.  strip here
    """
    RealtimeLogger.info('Remove read numbers from {} FASTQs'.format(len(fq_reads_ids)))
    work_dir = job.fileStore.getLocalTempDir()
    fq_file_names = [os.path.join(work_dir, 'reads-{}.fq.gz'.format(i)) for i in range(len(fq_reads_ids))]
    out_file_names = [os.path.join(work_dir, 'reads-strip-{}.fq.gz'.format(i)) for i in range(len(fq_reads_ids))]
    out_ids = []
    for fq_id, fq_name, out_name in zip(fq_reads_ids, fq_file_names, out_file_names):
        job.fileStore.readGlobalFile(fq_id, fq_name, mutable=(fq_name == fq_file_names[0]))
        cmd = [['pigz', '-dc', os.path.basename(fq_name)]]
        cmd.append(['sed', '-e', 's/_1$\\|_2$//g'])
        cmd.append(['pigz', '-c', '-p', str(max(1, job.cores))])
        with open(out_name, 'wb') as (out_file):
            context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
        out_ids.append(context.write_intermediate_file(job, out_name))

    return out_ids


def run_bwa_mem(job, context, fq_reads_ids, bwa_index_ids, paired_mode):
    """ run bwa-mem on reads in a fastq.  optionally run in paired mode
    return id of bam file
    """
    RealtimeLogger.info('Run BWA MEM on {} FASTQs'.format(len(fq_reads_ids)))
    requeue_promise = ensure_disk(job, run_bwa_mem, [context, fq_reads_ids, bwa_index_ids, paired_mode], {}, itertools.chain(fq_reads_ids, list(bwa_index_ids.values())))
    if requeue_promise is not None:
        return requeue_promise
    else:
        work_dir = job.fileStore.getLocalTempDir()
        fq_file_names = []
        for i, fq_reads_id in enumerate(fq_reads_ids):
            fq_file_names.append(os.path.join(work_dir, 'reads{}.fq.gz'.format(i)))
            job.fileStore.readGlobalFile(fq_reads_id, fq_file_names[(-1)])

        fasta_file = os.path.join(work_dir, 'reference.fa')
        for suf, idx_id in list(bwa_index_ids.items()):
            job.fileStore.readGlobalFile(idx_id, '{}{}'.format(fasta_file, suf))

        bam_file = os.path.join(work_dir, 'bwa-mem')
        if paired_mode:
            bam_file += '-pe'
        bam_file += '.bam'
        if paired_mode:
            start_time = timeit.default_timer()
            cmd = ['bwa', 'mem', '-t', str(context.config.alignment_cores), os.path.basename(fasta_file),
             os.path.basename(fq_file_names[0])]
            if len(fq_file_names) == 2:
                cmd += [os.path.basename(fq_file_names[1])]
            else:
                cmd += ['-p']
            cmd += context.config.bwa_opts
            with open(bam_file + '.sam', 'wb') as (out_sam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_sam)
            end_time = timeit.default_timer()
            run_time = end_time - start_time
            RealtimeLogger.info('Aligned aligned-linear_0.gam. Process took {} seconds with paired-end bwa-mem'.format(run_time))
            cmd = [
             'samtools', 'view', '-1', '-F', '2304', os.path.basename(bam_file + '.sam')]
            with open(bam_file, 'wb') as (out_bam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_bam)
        else:
            assert len(fq_file_names) == 1
            start_time = timeit.default_timer()
            cmd = ['bwa', 'mem', '-t', str(context.config.alignment_cores), os.path.basename(fasta_file),
             os.path.basename(fq_file_names[0])] + context.config.bwa_opts
            with open(bam_file + '.sam', 'wb') as (out_sam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_sam)
            end_time = timeit.default_timer()
            run_time = end_time - start_time
            RealtimeLogger.info('Aligned aligned-linear_0.gam. Process took {} seconds with single-end bwa-mem'.format(run_time))
            cmd = [
             'samtools', 'view', '-1', '-F', '2304', os.path.basename(bam_file + '.sam')]
            with open(bam_file, 'wb') as (out_bam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_bam)
        bam_file_id = context.write_output_file(job, bam_file)
        return (
         bam_file_id, run_time)


def run_minimap2(job, context, fq_reads_ids, fasta_id, minimap2_index_id=None, paired_mode=True):
    """
    Run minimap2 on reads in one or two fastq files. Always pairs up reads if
    two files or passed, or if one file is passed and reads are correctly named
    and interleaved; paired_mode just controlls output naming. Returns a BAM
    file ID and the runtime.
    
    Automatically converts minimap2's SAM output to BAM.
    """
    RealtimeLogger.info('Run minimap2 on {} FASTQs'.format(len(fq_reads_ids)))
    requeue_promise = ensure_disk(job, run_minimap2, [context, fq_reads_ids, fasta_id], {'minimap2_index_id':minimap2_index_id, 
     'paired_mode':paired_mode}, itertools.chain(fq_reads_ids, [minimap2_index_id] if minimap2_index_id is not None else [fasta_id]))
    if requeue_promise is not None:
        return requeue_promise
    else:
        work_dir = job.fileStore.getLocalTempDir()
        fq_file_names = []
        for i, fq_reads_id in enumerate(fq_reads_ids):
            fq_file_names.append(os.path.join(work_dir, 'reads{}.fq.gz'.format(i)))
            job.fileStore.readGlobalFile(fq_reads_id, fq_file_names[(-1)])

        ref_filename = None
        if minimap2_index_id is not None:
            index_file = os.path.join(work_dir, 'reference.fa.mmi')
            job.fileStore.readGlobalFile(minimap2_index_id, index_file)
            ref_filename = index_file
        else:
            fasta_file = os.path.join(work_dir, 'reference.fa')
            job.fileStore.readGlobalFile(fasta_id, fasta_file)
            ref_filename = fasta_file
        bam_file = os.path.join(work_dir, 'minimap2')
        if paired_mode:
            bam_file += '-pe'
        bam_file += '.bam'
        if paired_mode:
            start_time = timeit.default_timer()
            cmd = [
             'minimap2', '-t', str(context.config.alignment_cores)] + context.config.minimap2_opts + [
             os.path.basename(ref_filename), os.path.basename(fq_file_names[0])]
            if len(fq_file_names) == 2:
                cmd.append(os.path.basename(fq_file_names[1]))
            with open(bam_file + '.sam', 'wb') as (out_sam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_sam)
            end_time = timeit.default_timer()
            run_time = end_time - start_time
            RealtimeLogger.info('Aligned {}. Process took {} seconds with paired-end minimap2'.format(bam_file, run_time))
            cmd = [
             'samtools', 'view', '-1', '-F', '2304', os.path.basename(bam_file + '.sam')]
            with open(bam_file, 'wb') as (out_bam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_bam)
        else:
            assert len(fq_file_names) == 1
            start_time = timeit.default_timer()
            cmd = [
             'minimap2', '-t', str(context.config.alignment_cores)] + context.config.minimap2_opts + [
             os.path.basename(ref_filename), os.path.basename(fq_file_names[0])]
            with open(bam_file + '.sam', 'wb') as (out_sam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_sam)
            end_time = timeit.default_timer()
            run_time = end_time - start_time
            RealtimeLogger.info('Aligned {}. Process took {} seconds with single-end bwa-mem'.format(bam_file, run_time))
            cmd = [
             'samtools', 'view', '-1', '-F', '2304', os.path.basename(bam_file + '.sam')]
            with open(bam_file, 'wb') as (out_bam):
                context.runner.call(job, cmd, work_dir=work_dir, outfile=out_bam)
        bam_file_id = context.write_output_file(job, bam_file)
        return (
         bam_file_id, run_time)


def downsample_bam(job, context, bam_file_id, fraction):
    """
    Extract the given fraction of reads from the given BAM file. Return the
    file ID for the new BAM file.
    """
    RealtimeLogger.info('Downasmple BAM id {} to {}'.format(bam_file_id, fraction))
    work_dir = job.fileStore.getLocalTempDir()
    in_file = os.path.join(work_dir, 'full.bam')
    out_file = os.path.join(work_dir, 'downsampled.bam')
    job.fileStore.readGlobalFile(bam_file_id, in_file)
    cmd = [
     'samtools', 'view', '-b', '-s', str(fraction), os.path.basename(in_file)]
    with open(out_file, 'wb') as (out_bam):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_bam)
    return context.write_intermediate_file(job, out_file)


def downsample_gam(job, context, gam_file_id, fraction):
    """
    Extract the given fraction of reads from the given GAM file. Return the
    file ID for the new GAM file.
    """
    RealtimeLogger.info('Downasmple GAM id {} to {}'.format(gam_file_id, fraction))
    work_dir = job.fileStore.getLocalTempDir()
    in_file = os.path.join(work_dir, 'full.gam')
    out_file = os.path.join(work_dir, 'downsampled.gam')
    job.fileStore.readGlobalFile(gam_file_id, in_file)
    cmd = [
     'vg', 'filter', '-t', str(job.cores), '--downsample', str(fraction), os.path.basename(in_file)]
    with open(out_file, 'wb') as (out_gam):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_gam)
    return context.write_intermediate_file(job, out_file)


def extract_bam_read_stats(job, context, name, bam_file_id, paired, sep='_'):
    """
    extract positions, scores, and MAPQs from bam, return id of read stats file
    (lots of duplicated code with vg_sim, should merge?)
    
    Produces a read stats TSV of the format:
    read name, read tags (or '.'), [contig aligned to, alignment position,]* score, MAPQ
    
    TODO: Currently scores are not extracted and a score of 0 is always
    returned.
    
    TODO: Tags are also always '.'.

    """
    RealtimeLogger.info('Extract BAM read stats from {} id {}'.format(name, bam_file_id))
    work_dir = job.fileStore.getLocalTempDir()
    bam_file = os.path.join(work_dir, name)
    job.fileStore.readGlobalFile(bam_file_id, bam_file)
    out_pos_file = bam_file + '.tsv'
    cmd = [
     [
      'samtools', 'view', os.path.basename(bam_file), '-F', '2304']]
    cmd.append(['grep', '-v', '^@'])
    if paired:
        cmd.append(['perl', '-ne', '@val = split("\t", $_); print @val[0] . "{}" . (@val[1] & 64 ? "1" : @val[1] & 128 ? "2" : "?"), "\t.\t" . @val[2] . "\t" . (@val[3] +  int(length(@val[9]) / 2)) . "\t0\t" . @val[4] . "\n";'.format(sep)])
    else:
        cmd.append(['perl', '-ne', '@val = split("\t", $_); print @val[0] . "\t.\t" . @val[2] . "\t" . (@val[3] +  int(length(@val[9]) / 2)) . "\t0\t" . @val[4] . "\n";'])
    cmd.append(['sort'])
    with open(out_pos_file, 'wb') as (out_pos):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_pos)
    stats_file_id = context.write_intermediate_file(job, out_pos_file)
    return stats_file_id


def annotate_gam(job, context, xg_file_id, gam_file_id):
    """
    Annotate the given GAM file with positions from the given XG file.
    """
    RealtimeLogger.info('Annotate GAM id {} with XG id {}'.format(gam_file_id, xg_file_id))
    work_dir = job.fileStore.getLocalTempDir()
    RealtimeLogger.info('Download XG from file {}'.format(xg_file_id))
    xg_file = os.path.join(work_dir, 'index.xg')
    job.fileStore.readGlobalFile(xg_file_id, xg_file)
    gam_file = os.path.join(work_dir, 'reads.gam')
    job.fileStore.readGlobalFile(gam_file_id, gam_file)
    annotated_gam_file = os.path.join(work_dir, 'annotated.gam')
    cmd = [
     [
      'vg', 'annotate', '-p', '-a', os.path.basename(gam_file), '-x', os.path.basename(xg_file)]]
    with open(annotated_gam_file, 'wb') as (out_file):
        try:
            context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
        except:
            logging.error('GAM annotation failed. Dumping files.')
            context.write_output_file(job, gam_file)
            context.write_output_file(job, xg_file)
            raise

    return context.write_intermediate_file(job, annotated_gam_file)


def extract_gam_read_stats(job, context, name, gam_file_id, generate_tags=[]):
    """
    extract positions, scores, and MAPQs for reads from a gam, and return the id
    of the resulting read stats file
    
    The read stats file may also be used as a truth file; the two kinds of files are the same format.
    
    Produces a read stats TSV of the format:
    read name, read tags (or '.'), [contig aligned to, alignment position,]* score, MAPQ
    
    If generate_tags is specified, it is a list of boolean GAM annotation names
    that will be turned into tags, in addition to the contents of the features
    annotation.
    
    If the GAM is not annotated with alignment positions, contig and position
    will both contain only "0" values.

    """
    RealtimeLogger.info('Extract GAM read stats from {}'.format(name))
    work_dir = job.fileStore.getLocalTempDir()
    gam_file = os.path.join(work_dir, name)
    job.fileStore.readGlobalFile(gam_file_id, gam_file)
    out_pos_file = gam_file + '.tsv'
    gam_annot_json = gam_file + '.json'
    cmd = [['vg', 'view', '-aj', os.path.basename(gam_file)]]
    with open(gam_annot_json, 'wb') as (output_annot_json):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=output_annot_json)
    tag_generation = ''
    for annotation_name in generate_tags:
        tag_generation += '.annotation.features = (if (.annotation.features | length) > 0 then .annotation.features else [] end + if .annotation.' + annotation_name + ' then ["' + annotation_name + '"] else [] end) | '

    jq_cmd = [
     'jq', '-c', '-r', tag_generation + '[.name] + if (.annotation.features | length) > 0 then [.annotation.features | join(",")] else ["."] end + if .refpos != null then [.refpos[] | .name, if .offset != null then .offset else 0 end] else ["",""] end + if .score == null then [0] else [.score] end + if .mapping_quality == null then [0] else [.mapping_quality] end | @tsv',
     os.path.basename(gam_annot_json)]
    jq_pipe = [
     jq_cmd, ['sed', '-e', 's/null/0/g', '-e', 's/\\/1/_1/g', '-e', 's/\\/2/_2/g']]
    with open(out_pos_file + '.unsorted', 'wb') as (out_pos):
        context.runner.call(job, jq_pipe, work_dir=work_dir, outfile=out_pos)
    os.remove(gam_annot_json)
    sort_cmd = [
     'sort', os.path.basename(out_pos_file) + '.unsorted']
    with open(out_pos_file, 'wb') as (out_pos):
        context.runner.call(job, sort_cmd, work_dir=work_dir, outfile=out_pos)
    out_stats_file_id = context.write_intermediate_file(job, out_pos_file)
    return out_stats_file_id


def compare_positions(job, context, truth_file_id, name, stats_file_id, mapeval_threshold):
    """
    Compares positions from two TSV files. Both files have the format:
    read name, comma-separated tag list (or '.'), [contig touched, true position]*, score, MAPQ
    
    The truth file will have the base tag list, while the stats file will
    have the cannonical score and MAPQ, as well as additional tags to add.
    
    The input files must be in lexicographically sorted order by name, but may
    not contain the same number of entries each. The stats file may be a subset
    of the truth.
    
    Produces a TSV of the form:
    read name, correctness flag (0/1), MAPQ, comma-separated tag list (or '.')

    Returns output file ID, and exports it as <name>.compare.positions.
    
    mapeval_threshold is the distance within which a mapping is held to have hit
    the correct position.

    TODO: Replace with a vg mapeval call.
    
    """
    RealtimeLogger.info('Compare mapping positions for {}'.format(name))
    work_dir = job.fileStore.getLocalTempDir()
    true_read_stats_file = os.path.join(work_dir, 'true.tsv')
    job.fileStore.readGlobalFile(truth_file_id, true_read_stats_file)
    test_read_stats_file = os.path.join(work_dir, name + '.tsv')
    job.fileStore.readGlobalFile(stats_file_id, test_read_stats_file)
    out_file = os.path.join(work_dir, name + '.compare.positions')

    def list_or_none(l):
        if l is None:
            return l
        else:
            return list(l)

    with open(true_read_stats_file) as (truth):
        with open(test_read_stats_file) as (test):
            with open(out_file, 'w') as (out_stream):
                out = tsv.TsvWriter(out_stream)
                truth_reader = iter(tsv.TsvReader(truth))
                test_reader = iter(tsv.TsvReader(test))
                true_fields = list_or_none(next(truth_reader, None))
                test_fields = list_or_none(next(test_reader, None))
                true_line = 1
                test_line = 1
                while true_fields is not None and test_fields is not None:
                    if len(true_fields) < 6:
                        raise RuntimeError('Incorrect (<6) true field count on line {}: {}'.format(true_line, true_fields))
                    if len(test_fields) < 4:
                        raise RuntimeError('Incorrect (<4) test field count on line {}: {}'.format(test_line, test_fields))
                    true_read_name = true_fields[0]
                    aln_read_name = test_fields[0]
                    if true_read_name < aln_read_name:
                        true_fields = list_or_none(next(truth_reader, None))
                        true_line += 1
                        if not (true_fields == None or true_fields[0] > true_read_name):
                            raise AssertionError
                            continue
                    elif aln_read_name < true_read_name:
                        test_fields = list_or_none(next(test_reader, None))
                        test_line += 1
                        if not (test_fields == None or test_fields[0] > aln_read_name):
                            raise AssertionError
                            continue
                    else:
                        if not aln_read_name == true_read_name:
                            raise AssertionError
                        else:
                            aln_tags = true_fields[1]
                            if aln_tags == '':
                                aln_tags = '.'
                            aln_extra_tags = test_fields[1]
                            if aln_extra_tags == '':
                                aln_extra_tags = '.'
                            combined_tags = set(aln_tags.split(',')) | set(aln_extra_tags.split(','))
                            combined_tags -= {'.'}
                            combined_tags_string = ','.join(sorted(combined_tags)) if len(combined_tags) > 0 else '.'
                            true_pos_dict = dict(list(zip(true_fields[2:-2:2], list(map(parse_int, true_fields[3:-2:2])))))
                            aln_pos_dict = dict(list(zip(test_fields[2:-2:2], list(map(parse_int, test_fields[3:-2:2])))))
                            assert len(true_pos_dict) > 0
                        aln_mapq = parse_int(test_fields[(-1)])
                        aln_correct = 0
                        for aln_chr, aln_pos in list(aln_pos_dict.items()):
                            if aln_chr in true_pos_dict and abs(true_pos_dict[aln_chr] - aln_pos) < mapeval_threshold:
                                aln_correct = 1
                                break

                        out.line(aln_read_name, aln_correct, aln_mapq, combined_tags_string)
                        true_fields = list_or_none(next(truth_reader, None))
                        true_line += 1
                        test_fields = list_or_none(next(test_reader, None))
                        test_line += 1

    out_file_id = context.write_output_file(job, out_file)
    return out_file_id


def compare_scores(job, context, baseline_name, baseline_file_id, name, score_file_id):
    """ Compares scores from TSV files. The baseline and file under test both
    have the format: read name, contig aligned to, alignment position,
    alignment score, MAPQ
    
    Both must be in lexicographical order by read name, but they need not have
    the same length. The score file may be a subset of the baseline.
    
    Produces a CSV (NOT TSV) of the form: read name, score difference, aligned
    score, baseline score
    
    If saved to the out store it will be: <condition name>.compare.<baseline
    name>.scores
    
    Uses the given (condition) name as a file base name for the file under
    test.
    
    """
    RealtimeLogger.info('Compare mapping scores for {}'.format(name))
    work_dir = job.fileStore.getLocalTempDir()
    baseline_read_stats_file = os.path.join(work_dir, 'baseline.tsv')
    job.fileStore.readGlobalFile(baseline_file_id, baseline_read_stats_file)
    test_read_stats_file = os.path.join(work_dir, name + '.tsv')
    job.fileStore.readGlobalFile(score_file_id, test_read_stats_file)
    out_file = os.path.join(work_dir, '{}.compare.{}.scores'.format(name, baseline_name))

    def list_or_none(l):
        if l is None:
            return l
        else:
            return list(l)

    with open(baseline_read_stats_file) as (baseline):
        with open(test_read_stats_file) as (test):
            with open(out_file, 'w') as (out):
                baseline_reader = iter(tsv.TsvReader(baseline))
                test_reader = iter(tsv.TsvReader(test))
                baseline_fields = list_or_none(next(baseline_reader, None))
                test_fields = list_or_none(next(test_reader, None))
                baseline_line = 1
                test_line = 1
                while baseline_fields is not None and test_fields is not None:
                    if len(baseline_fields) < 5:
                        raise RuntimeError('Incorrect (<5) baseline field count on line {}: {}'.format(baseline_line, baseline_fields))
                    if len(test_fields) < 5:
                        raise RuntimeError('Incorrect (<5) test field count on line {}: {}'.format(test_line, test_fields))
                    baseline_read_name = baseline_fields[0]
                    aln_read_name = test_fields[0]
                    if baseline_read_name < aln_read_name:
                        baseline_fields = list_or_none(next(baseline_reader, None))
                        baseline_line += 1
                        continue
                    elif aln_read_name < baseline_read_name:
                        test_fields = list_or_none(next(test_reader, None))
                        test_line += 1
                        continue
                    else:
                        aligned_score = test_fields[(-2)]
                        baseline_score = baseline_fields[(-2)]
                        score_diff = parse_int(aligned_score) - parse_int(baseline_score)
                        out.write('{}, {}, {}, {}\n'.format(baseline_fields[0], score_diff, aligned_score, baseline_score))
                        baseline_fields = list_or_none(next(baseline_reader, None))
                        baseline_line += 1
                        test_fields = list_or_none(next(test_reader, None))
                        test_line += 1

    out_file_id = context.write_intermediate_file(job, out_file)
    return out_file_id


def run_map_eval_index(job, context, xg_file_ids, gcsa_file_ids, gbwt_file_ids, minimizer_file_ids, distance_file_ids, id_range_file_ids, snarl_file_ids, vg_file_ids):
    """ 
    Index the given vg files.
    
    If no vg files are provided, pass through the given indexes. Indexes are
    lists of index IDs, one per graph, except gcsa_file_ids, which is tuples of
    GCSA and LCP file IDs, one tuple per graph. Index types which are not used
    should have falsey values instead of lists.
    
    Returns a list of dicts from index type name to index file ID, as used by
    run_indexing in vg_index.py, holding file IDs for different index
    components.
    
    """
    RealtimeLogger.info('Compute graph indexes')
    index_ids = []
    if vg_file_ids:
        for vg_file_id in vg_file_ids:
            index_job = job.addChildJobFn(run_indexing, context, [vg_file_id], ['default.vg'], 'index',
              ['default'], wanted=(set(['xg', 'gcsa', 'id_ranges', 'snarls'])),
              cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            index_ids.append(index_job.rv())

    else:
        for i, xg_id in enumerate(xg_file_ids):
            indexes = {}
            indexes['xg'] = xg_id
            if gcsa_file_ids:
                if gcsa_file_ids[i] is not None:
                    indexes['gcsa'], indexes['lcp'] = gcsa_file_ids[i]
            if gbwt_file_ids:
                if gbwt_file_ids[i] is not None:
                    indexes['gbwt'] = gbwt_file_ids[i]
            if minimizer_file_ids:
                if minimizer_file_ids[i] is not None:
                    indexes['minimizer'] = minimizer_file_ids[i]
            if distance_file_ids and distance_file_ids[i] is not None:
                indexes['distance'] = distance_file_ids[i]
            if id_range_file_ids:
                if id_range_file_ids[i] is not None:
                    indexes['id_ranges'] = id_range_file_ids[i]
            if snarl_file_ids:
                if snarl_file_ids[i] is not None:
                    indexes['snarls'] = snarl_file_ids[i]
            index_ids.append(indexes)

    return index_ids


def run_map_eval_align(job, context, index_ids, xg_comparison_ids, gam_names, gam_file_ids, reads_fastq_single_ids, reads_fastq_paired_ids, reads_fastq_paired_for_vg_ids, fasta_file_id, matrix, bwa_index_ids=[], minimap2_index_id=None, ignore_quals=False, surject=False, validate=False):
    """
    
    Run alignments, if alignment files have not already been provided.
    
    Returns a dict from output condition name (with condition tags added) to
    dicts, each of which may have "gam", "bam", "xg", "paired", and "runtime".
    "gam" is the alligned GAM fiel ID if computed, "bam" is the alligned or
    surjected BAM file ID if present, and "xg" is the XG index aligned against,
    if applicable. "paired" is True or False depending on if paired-end mapping
    was used. "runtime" is the running time of the alignment in seconds,
    without toil-vg overhead. Note that right now surjected BAMs live in their
    own conditions with their own names.
    
    We synthesize paired-end versions of existing entries, supplementing the
    input GAM name and index lists.
    
    Determines what conditions and combinations of conditions to run by looking
    at the "matrix" parameter, which is a dict from string variable name to a
    list of values for that variable. All sensible combinations of the variable
    values from the matrix are run as conditions.
    
    Variables to be used in the matrix are:
    
    "aligner": ["vg", "bwa", "minimap2"]
    
    "mapper": ["map", "mpmap", "gaffe"]
    
    "paired": [True, False]
    
    "gbwt": [False, True, <float log recombination penalty override>, ...]
    
    "snarls": [True, False] (only affects mpmap)
   
    Additionally, mpmap_opts and more_mpmap_opts from the context's config are
    consulted, doubling the mpmap runs if more_mpmap_opts is set.
   
    If gam_file_ids are specified, passes those through instead of doing any vg
    mapping, but still does bwa mapping if requested.
    
    """
    RealtimeLogger.info('Input GAM names: {}'.format(gam_names))
    if not len(set(gam_names)) == len(gam_names):
        raise AssertionError
    else:
        results_dict = collections.defaultdict(dict)
        xg_ids = [index_id['xg'] for index_id in index_ids]
        if xg_comparison_ids:
            assert len(xg_comparison_ids) == len(xg_ids)
            overridden = 0
            for item in xg_comparison_ids:
                if item not in xg_ids:
                    overridden += 1

            xg_ids = xg_comparison_ids
            for index_id, comparison_xg_id in zip(index_ids, xg_comparison_ids):
                index_id['xg-surject'] = comparison_xg_id

            RealtimeLogger.info('Applied {} xg overrides'.format(overridden))
        else:
            RealtimeLogger.info('No xg overrides applied')
    mpmap_opts_list = [context.config.mpmap_opts]
    if context.config.more_mpmap_opts:
        mpmap_opts_list += context.config.more_mpmap_opts
    if ignore_quals:
        for mpmap_opts in mpmap_opts_list:
            if '-A' not in mpmap_opts and '--no-qual-adjust' not in mpmap_opts:
                mpmap_opts.append('-A')

        context.config.map_opts = [o for o in context.config.map_opts if o not in ('-A',
                                                                                   '--qual-adjust')]

    def fq_names(fq_reads_ids):
        return ['input{}.fq.gz'.format(i) for i in range(len(fq_reads_ids))]

    def aligner_conditions(conditions_in):
        for condition in conditions_in:
            for aligner in matrix['aligner']:
                extended = dict(condition)
                extended.update({'aligner': aligner})
                yield extended

    def mapper_conditions(conditions_in):
        for condition in conditions_in:
            if condition['aligner'] == 'vg':
                for mapper in matrix['mapper']:
                    extended = dict(condition)
                    extended.update({'mapper': mapper})
                    yield extended

            else:
                yield condition

    def multipath_opts_conditions(conditions_in):
        for condition in conditions_in:
            if condition['aligner'] == 'vg' and condition['mapper'] == 'mpmap':
                for opt_num in range(len(mpmap_opts_list)):
                    extended = dict(condition)
                    extended.update({'opt_num': opt_num})
                    yield extended

            else:
                yield condition

    def paired_conditions(conditions_in):
        for condition in conditions_in:
            for paired in matrix['paired']:
                if condition['aligner'] == 'minimap2':
                    if not paired:
                        continue
                extended = dict(condition)
                extended.update({'paired': paired})
                yield extended

    def gbwt_conditions(conditions_in):
        for condition in conditions_in:
            if condition['aligner'] == 'vg' and condition['mapper'] in ('map', 'mpmap'):
                for gbwt in matrix['gbwt']:
                    extended = dict(condition)
                    extended.update({'gbwt': gbwt})
                    yield extended

            else:
                yield condition

    def snarls_conditions(conditions_in):
        for condition in conditions_in:
            if condition['aligner'] == 'vg' and condition['mapper'] == 'mpmap':
                for use_snarls in matrix['snarls']:
                    extended = dict(condition)
                    extended.update({'snarls': use_snarls})
                    yield extended

            else:
                yield condition

    def compose_two_generators(gen1, gen2):

        def composed_generator(x):
            return gen2(gen1(x))

        return composed_generator

    condition_steps = [
     aligner_conditions,
     mapper_conditions,
     multipath_opts_conditions,
     paired_conditions,
     gbwt_conditions,
     snarls_conditions]
    condition_generator = reduce(compose_two_generators, condition_steps)
    do_vg_mapping = not gam_file_ids
    gam_file_ids = gam_file_ids or []
    bwa_bam_file_ids, bwa_mem_times = [
     None, None], [None, None]
    bwa_start_job = None
    minimap2_start_job = None
    read_chunk_jobs = {}
    used_tag_strings = set()
    RealtimeLogger.info('Condition matrix: {}'.format(matrix))
    condition_number = 0
    if not do_vg_mapping:
        for name, gam_id, xg_id in zip(gam_names, gam_file_ids, xg_ids):
            results_dict[name]['gam'] = gam_id
            results_dict[name]['runtime'] = 0
            results_dict[name]['xg'] = xg_id

    for condition in condition_generator([{}]):
        RealtimeLogger.info('Condition {}: {}'.format(condition_number, condition))
        condition_number += 1
        if condition['aligner'] == 'vg':
            if do_vg_mapping:
                tag_string = ''
                if condition.get('gbwt', False):
                    if condition['gbwt'] == True:
                        tag_string += '-gbwt'
                    else:
                        tag_string += '-gbwt{}'.format(condition['gbwt'])
                if condition['mapper'] == 'mpmap':
                    if not condition['snarls']:
                        if True in matrix['snarls']:
                            tag_string += '-nosnarls'
                    tag_string += '-mp'
                    tag_string += str(condition['opt_num']) if condition['opt_num'] > 0 else ''
                    mapping_context = copy.deepcopy(context)
                    mapping_context.config.mpmap_opts = mpmap_opts_list[condition['opt_num']]
                else:
                    if condition['mapper'] == 'gaffe':
                        tag_string += '-gaffe'
                    mapping_context = context
                if condition['paired']:
                    tag_string += '-pe'
                    assert reads_fastq_paired_for_vg_ids
                    fastq_ids = reads_fastq_paired_for_vg_ids
                    interleaved = len(reads_fastq_paired_for_vg_ids) == 1
                    if not interleaved:
                        assert len(reads_fastq_paired_for_vg_ids) == 2
                else:
                    if not reads_fastq_single_ids:
                        raise AssertionError
                    elif not len(reads_fastq_single_ids) == 1:
                        raise AssertionError
                    fastq_ids = reads_fastq_single_ids
                    interleaved = False
                RealtimeLogger.info('Condition {} produced tag string {}'.format(condition, tag_string))
                if tag_string in used_tag_strings:
                    raise RuntimeError('Duplicate tag string {}'.format(tag_string))
                else:
                    used_tag_strings.add(tag_string)
                gbwt_penalty = None
                if condition.get('gbwt'):
                    if condition['gbwt'] != True:
                        gbwt_penalty = condition['gbwt']
                map_jobs = []
                for i, indexes in enumerate(index_ids):
                    if condition.get('gbwt'):
                        if indexes.get('gbwt') is None:
                            continue
                        if not condition.get('gbwt', True):
                            if condition.get('mapper') in ('map', 'mpmap'):
                                indexes = dict(indexes)
                                if 'gbwt' in indexes:
                                    del indexes['gbwt']
                    else:
                        if not condition.get('snarls', True):
                            indexes = dict(indexes)
                            if 'snarls' in indexes:
                                del indexes['snarls']
                        if tuple(fastq_ids) not in read_chunk_jobs:
                            read_chunk_jobs[tuple(fastq_ids)] = job.addChildJobFn(run_split_reads_if_needed, context, (fq_names(fastq_ids)), None,
                              None, fastq_ids, cores=(context.config.misc_cores),
                              memory=(context.config.misc_mem),
                              disk=(context.config.misc_disk))
                    read_chunk_job = read_chunk_jobs[tuple(fastq_ids)]
                    map_jobs.append(read_chunk_job.addFollowOnJobFn(run_mapping, mapping_context, (fq_names(fastq_ids)), None,
                      None, ('aligned-{}{}'.format(gam_names[i], tag_string)), interleaved,
                      (condition['mapper']), indexes, reads_chunk_ids=(read_chunk_job.rv()),
                      bam_output=False,
                      surject=surject,
                      gbwt_penalty=gbwt_penalty,
                      validate=validate,
                      cores=(mapping_context.config.misc_cores),
                      memory=(mapping_context.config.misc_mem),
                      disk=(mapping_context.config.misc_disk)))

                for i, map_job in enumerate(map_jobs):
                    tagged_name = gam_names[i] + tag_string
                    results_dict[tagged_name]['gam'] = map_job.rv(0)
                    results_dict[tagged_name]['runtime'] = map_job.rv(1)
                    results_dict[tagged_name]['xg'] = xg_ids[i]
                    results_dict[tagged_name]['paired'] = condition['paired']
                    if surject:
                        surjected_name = tagged_name + '-surject'
                        results_dict[surjected_name]['bam'] = map_job.rv(2)
                        results_dict[surjected_name]['paired'] = condition['paired']
                        results_dict[surjected_name]['runtime'] = map_job.rv(1)

        if condition['aligner'] == 'bwa':
            tag_string = ''
            if bwa_start_job is None:
                bwa_start_job = Job()
                job.addChild(bwa_start_job)
                bwa_index_job = bwa_start_job.addChildJobFn(run_bwa_index, context, fasta_file_id,
                  bwa_index_ids=bwa_index_ids,
                  intermediate=True,
                  cores=(context.config.bwa_index_cores),
                  memory=(context.config.bwa_index_mem),
                  disk=(context.config.bwa_index_disk))
                bwa_index_ids = bwa_index_job.rv()
            if condition['paired']:
                assert reads_fastq_paired_ids
                tag_string += '-pe'
                bwa_mem_job = bwa_start_job.addFollowOnJobFn(run_bwa_mem, context, reads_fastq_paired_ids, bwa_index_ids, True, cores=(context.config.alignment_cores),
                  memory=(context.config.alignment_mem),
                  disk=(context.config.alignment_disk))
            else:
                assert reads_fastq_single_ids
                bwa_mem_job = bwa_start_job.addFollowOnJobFn(run_bwa_mem, context, reads_fastq_single_ids, bwa_index_ids, False, cores=(context.config.alignment_cores),
                  memory=(context.config.alignment_mem),
                  disk=(context.config.alignment_disk))
            tagged_name = 'bwa-mem' + tag_string
            results_dict[tagged_name]['bam'] = bwa_mem_job.rv(0)
            results_dict[tagged_name]['runtime'] = bwa_mem_job.rv(1)
            results_dict[tagged_name]['paired'] = condition['paired']
        else:
            if condition['aligner'] == 'minimap2':
                tag_string = ''
                if minimap2_start_job is None:
                    minimap2_start_job = Job()
                    job.addChild(minimap2_start_job)
                    minimap2_index_job = minimap2_start_job.addChildJobFn(run_minimap2_index, context, fasta_file_id,
                      minimap2_index_id=minimap2_index_id,
                      intermediate=True,
                      cores=(context.config.minimap2_index_cores),
                      memory=(context.config.minimap2_index_mem),
                      disk=(context.config.minimap2_index_disk))
                    minimap2_index_id = minimap2_index_job.rv()
                if condition['paired']:
                    assert reads_fastq_paired_ids
                    tag_string += '-pe'
                    minimap2_job = minimap2_start_job.addFollowOnJobFn(run_minimap2, context, reads_fastq_paired_ids, fasta_file_id, minimap2_index_id,
                      True, cores=(context.config.alignment_cores),
                      memory=(context.config.alignment_mem),
                      disk=(context.config.alignment_disk))
                else:
                    assert reads_fastq_single_ids
                    minimap2_job = minimap2_start_job.addFollowOnJobFn(run_minimap2, context, reads_fastq_single_ids, fasta_file_id, minimap2_index_id,
                      False, cores=(context.config.alignment_cores),
                      memory=(context.config.alignment_mem),
                      disk=(context.config.alignment_disk))
                tagged_name = 'minimap2' + tag_string
                results_dict[tagged_name]['bam'] = minimap2_job.rv(0)
                results_dict[tagged_name]['runtime'] = minimap2_job.rv(1)
                results_dict[tagged_name]['paired'] = condition['paired']

    RealtimeLogger.info('Processed {} total conditions'.format(condition_number))
    return results_dict


def run_map_eval_comparison(job, context, mapping_condition_dict, true_read_stats_file_id, mapeval_threshold, score_baseline_name=None, original_read_gam=None, downsample_portion=None, gbwt_usage_tag_gam_name=None):
    """
    run the mapping comparison.  Dump some tables into the outstore.
    
    Takes a dict from condition name to condition dict, with some subset of
    "gam", "bam", "xg", "paired", a file of true read positions, and a
    correctness comparison threshold distance.
    
    Returns a pair of the position comparison results and the score comparison
    results.
    
    The score comparison results are a dict from baseline name to comparison
    against that baseline. Each comparison's data is a tuple of a list of
    individual per-graph comparison file IDs and an overall stats file for that
    comparison.
    
    If score_baseline_name is specified, all GAMs have their scores compared
    against the scores from the GAM with that name as a baseline.
    
    If original_read_gam is specified, all GAMs have their scores compared
    against that GAM's scores as a baseline.
    
    Each result set is itself a pair, consisting of a list of per-graph file
    IDs, and an overall statistics file ID.
    
    If downsample_portion is specified, the comparison runs on a downsampled
    porton of the reads.
    
    If gbwt_usage_tag_gam_name is set, tags for that GAM's reads' GBWT usage
    annotations will be generated for the GAM with that name, and propagated to
    all the other conditions nin the combined stats file.
    
    """
    RealtimeLogger.info('Comparing mapping results')
    stats_jobs = []
    for condition_number, (name, condition) in enumerate(mapping_condition_dict.items()):
        if 'bam' in condition:
            bam_id = condition['bam']
            parent_job = job
            if downsample_portion is not None:
                if downsample_portion != 1.0:
                    parent_job = job.addChildJobFn(downsample_bam, context, bam_id, downsample_portion, cores=(context.config.misc_cores),
                      memory=(context.config.misc_mem),
                      disk=(bam_id.size * 2))
                    bam_id = parent_job.rv()
            bam_filename = '{}-{}.bam'.format(name, condition_number)
            stats_jobs.append(parent_job.addChildJobFn(extract_bam_read_stats, context, bam_filename, bam_id, (condition['paired']), cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.alignment_disk)))
            condition['stats'] = stats_jobs[(-1)].rv()
        else:
            if 'gam' in condition:
                gam_filename = '{}-{}.gam'.format(name, condition_number)
                gam_id = condition['gam']
                if type(gam_id) is list:
                    assert len(gam_id) == 1
                    gam_id = gam_id[0]
                parent_job = job
                if downsample_portion is not None:
                    if downsample_portion != 1.0:
                        parent_job = job.addChildJobFn(downsample_gam, context, gam_id, downsample_portion, cores=(context.config.misc_cores),
                          memory=(context.config.misc_mem),
                          disk=(gam_id.size * 2))
                        gam_id = parent_job.rv()
                annotate_job = parent_job.addChildJobFn(annotate_gam, context, (condition['xg']), gam_id, cores=(context.config.misc_cores),
                  memory=(context.config.alignment_mem),
                  disk=(context.config.alignment_disk))
                generate_tags = []
                if name == gbwt_usage_tag_gam_name:
                    generate_tags.append('haplotype_score_used')
                stats_jobs.append(annotate_job.addFollowOnJobFn(extract_gam_read_stats, context, gam_filename,
                  (annotate_job.rv()), generate_tags=generate_tags,
                  cores=(context.config.misc_cores),
                  memory=(context.config.misc_mem),
                  disk=(context.config.alignment_disk)))
                condition['stats'] = stats_jobs[(-1)].rv()

    position_comparison_job = job.addChildJobFn(run_map_eval_compare_positions, context, true_read_stats_file_id,
      mapping_condition_dict, mapeval_threshold,
      gbwt_usage_tag_gam_name=gbwt_usage_tag_gam_name, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk))
    for dependency in stats_jobs:
        dependency.addFollowOn(position_comparison_job)

    position_comparison_results = position_comparison_job.rv()
    score_comparisons = {}
    if score_baseline_name is not None:
        baseline_stats_id = mapping_condition_dict[score_baseline_name]['stats']
        score_comp_job = job.addChildJobFn(run_map_eval_compare_scores, context, score_baseline_name, baseline_stats_id, mapping_condition_dict,
          cores=(context.config.misc_cores), memory=(context.config.misc_mem),
          disk=(context.config.misc_disk))
        for dependency in stats_jobs:
            dependency.addFollowOn(score_comp_job)

        score_comparisons[score_baseline_name] = score_comp_job.rv()
    if original_read_gam is not None:
        stats_job = job.addChildJobFn(extract_gam_read_stats, context, 'input.gam',
          original_read_gam, cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.alignment_disk))
        score_comp_job = stats_job.addFollowOnJobFn(run_map_eval_compare_scores, context, 'input', (stats_job.rv()), mapping_condition_dict,
          cores=(context.config.misc_cores), memory=(context.config.misc_mem),
          disk=(context.config.misc_disk))
        for dependency in stats_jobs:
            dependency.addFollowOn(score_comp_job)

        score_comparisons['input'] = score_comp_job.rv()
    return (
     position_comparison_results, score_comparisons)


def run_map_eval_compare_positions(job, context, true_read_stats_file_id, mapping_condition_dict, mapeval_threshold, gbwt_usage_tag_gam_name=None):
    """
    Compare the read positions for each read across the different aligmment
    methods.
    
    Takes a stats file for the true read positions, and a dict of conditions by
    name, each of which may have a "stats" stats file.
    
    Produces a bunch of individual comparison files against the truth (in TSV
    format), a combined "positions.results.tsv" across all aligners, and a
    statistics file "stats.tsv" in the out_store.
    
    If gbwt_usage_tag_gam_name is set, propagates the GBWT usage tag from the
    stats file for that GAM to the stats files for all the other conditions.
    
    Returns a dict of comparison file IDs by condition name, and the stats file ID.
    """
    RealtimeLogger.info('Comparing positions')
    root = job
    if gbwt_usage_tag_gam_name is not None:
        tag_stats_id = mapping_condition_dict[gbwt_usage_tag_gam_name]['stats']
        for name, condition in list(mapping_condition_dict.items()):
            if 'stats' in condition:
                propagate_job = job.addChildJobFn(propagate_tag, context, tag_stats_id, (condition['stats']), 'haplotype_score_used', cores=(context.config.misc_cores),
                  memory=(context.config.misc_mem),
                  disk=(context.config.alignment_disk))
                condition['stats'] = propagate_job.rv()

        root = Job()
        job.addFollowOn(root)
    compare_ids = {}
    for name, condition in list(mapping_condition_dict.items()):
        compare_ids[name] = root.addChildJobFn(compare_positions, context, true_read_stats_file_id, name, (condition['stats']),
          mapeval_threshold, cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.alignment_disk)).rv()

    position_comp_file_id = root.addFollowOnJobFn(run_process_position_comparisons, context, compare_ids, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.alignment_disk)).rv(1)
    return (
     compare_ids, position_comp_file_id)


def propagate_tag(job, context, from_id, to_id, tag_name):
    """
    Given two positiuon stats TSVs, of the format:
    
    read name, read tags (or '.'), [contig aligned to, alignment position,]* score, MAPQ
    
    Copies the tag of the given name, if present, from the from file to the to file for corresponding reads.
    
    Works even if files are not sorted by read name.
    
    Returns the ID of the modified to file.
    
    """
    RealtimeLogger.info('Propagating tag {} from GAM id {} to GAM id {}'.format(tag_name, from_id, to_id))
    if from_id == to_id:
        return to_id
    else:
        work_dir = job.fileStore.getLocalTempDir()
        from_stats_file = os.path.join(work_dir, 'from.tsv')
        job.fileStore.readGlobalFile(from_id, from_stats_file, mutable=True)
        to_stats_file = os.path.join(work_dir, 'to.tsv')
        job.fileStore.readGlobalFile(to_id, to_stats_file, mutable=True)
        from_stats_sorted = from_stats_file + '.sorted'
        to_stats_sorted = to_stats_file + '.sorted'
        cmd = ['sort', os.path.basename(from_stats_file), '-k', '1', '-o', os.path.basename(from_stats_sorted)]
        context.runner.call(job, cmd, work_dir=work_dir)
        cmd = ['sort', os.path.basename(to_stats_file), '-k', '1', '-o', os.path.basename(to_stats_sorted)]
        context.runner.call(job, cmd, work_dir=work_dir)
        with open(from_stats_sorted) as (from_stream):
            with open(to_stats_sorted) as (to_stream):
                with job.fileStore.writeGlobalFileStream() as (out_stream, out_id):
                    from_reader = iter(tsv.TsvReader(from_stream))
                    to_reader = iter(tsv.TsvReader(to_stream))
                    out_writer = tsv.TsvWriter(out_stream)
                    from_fields = next(from_reader, None)
                    to_fields = next(to_reader, None)
                    from_line = 1
                    to_line = 1
                    try:
                        while from_fields is not None and to_fields is not None:
                            if len(from_fields) < 4:
                                raise RuntimeError('Incorrect (<6) source field count on line {}: {}'.format(from_line, from_fields))
                            else:
                                if len(to_fields) < 4:
                                    raise RuntimeError('Incorrect (<4) destination field count on line {}: {}'.format(to_line, to_fields))
                                else:
                                    from_read_name = from_fields[0]
                                    to_read_name = to_fields[0]
                                    if from_read_name != to_read_name:
                                        raise RuntimeError('Name {} on line {} does not match {} on line {}'.format(from_read_name, from_line, to_read_name, to_line))
                                    from_tags = from_fields[1]
                                    if from_tags in ('', '.'):
                                        from_tags = set()
                                    else:
                                        from_tags = set(from_tags.split(','))
                                    to_tags = to_fields[1]
                                    if to_tags in ('', '.'):
                                        to_tags = set()
                                    else:
                                        to_tags = set(to_tags.split(','))
                                    if tag_name in from_tags:
                                        if tag_name not in to_tags:
                                            to_tags.add(tag_name)
                                    if tag_name not in from_tags:
                                        if tag_name in to_tags:
                                            to_tags.remove(tag_name)
                                if len(to_tags) == 0:
                                    to_tags = '.'
                                else:
                                    to_tags = ','.join(to_tags)
                            to_fields[1] = to_tags
                            out_writer.list_line(to_fields)
                            from_fields = next(from_reader, None)
                            from_line += 1
                            to_fields = next(to_reader, None)
                            to_line += 1

                    except:
                        logging.error('Tag propagation failed. Dumping files.')
                        context.write_output_file(job, from_stats_sorted)
                        context.write_output_file(job, to_stats_sorted)
                        raise

        return out_id


def run_process_position_comparisons(job, context, compare_ids):
    """
    Write some raw tables of position comparisons to the output. Compute some
    stats for each graph.
    
    Takes a dict from condition name to position comparison results file ID. Those input files have the format:
    
    read name, correct flag, mapq, tags

    The position results file we produce is a TSV of:
    correct flag, mapping quality, tag list (or '.'), method name, read name (or '.'), weight (or 1)
    
    The position results file has a header.
    
    Returns (the stats file's file ID, the position results file's ID)
    """
    map_stats = {}
    results_files = []
    RealtimeLogger.info('Processing position comparisons for conditions: {}'.format(list(compare_ids.keys())))
    for name, compare_id in list(compare_ids.items()):
        results_files.append(job.addChildJobFn(run_summarize_position_comparison, context, compare_id, name, cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.misc_disk)).rv())
        map_stats[name] = [
         job.addChildJobFn(run_acc, context, name, compare_id, cores=(context.config.misc_cores), memory=(context.config.misc_mem),
           disk=(context.config.misc_disk)).rv(),
         job.addChildJobFn(run_auc, context, name, compare_id, cores=(context.config.misc_cores), memory=(context.config.misc_mem),
           disk=(context.config.misc_disk)).rv(),
         job.addChildJobFn(run_qq, context, name, compare_id, cores=(context.config.misc_cores), memory=(context.config.misc_mem),
           disk=(context.config.misc_disk)).rv(),
         job.addChildJobFn(run_max_f1, context, name, compare_id, cores=(context.config.misc_cores), memory=(context.config.misc_mem),
           disk=(context.config.misc_disk)).rv()]

    return (
     job.addFollowOnJobFn(run_write_position_stats, context, map_stats).rv(),
     job.addFollowOnJobFn(run_concat_files, context, results_files, dest_name='position.results.tsv',
       header=('\t'.join(['correct', 'mq', 'tags', 'aligner', 'read', 'count']))).rv())


def run_summarize_position_comparison(job, context, compare_id, aligner_name):
    """
    Takes a position comparison results file ID. The file is a TSV with
    format:
    
    read name, correct flag, mapq, tags
    
    Compresses into a position results file, without header, where correct
    reads are summarized and only wrong reads appear individually.

    The position results file format is a TSV of: correct flag, mapping
    quality, tag list (or '.'), aligner name, read name (or '.'), weight (or 1)

    """
    requeue_promise = ensure_disk(job, run_summarize_position_comparison, [context, compare_id, aligner_name], {}, [
     compare_id],
      factor=2)
    if requeue_promise is not None:
        return requeue_promise
    else:
        RealtimeLogger.info('Summarizing position comparisons for {}'.format(aligner_name))
        work_dir = job.fileStore.getLocalTempDir()
        out_filename = os.path.join(work_dir, 'position.results.{}.tsv'.format(aligner_name))
        with open(out_filename, 'w') as (out_stream):
            writer = tsv.TsvWriter(out_stream)
            compare_file_path = os.path.join(work_dir, 'compare-file')
            job.fileStore.readGlobalFile(compare_id, compare_file_path)
            with open(compare_file_path, 'r') as (in_stream):
                reader = tsv.TsvReader(in_stream)
                summary_counts = Counter()
                for toks in reader:
                    read = dict(list(zip(['name', 'correct', 'mapq', 'tags'], list(toks))))
                    if read['correct'] == '1':
                        summary_counts[(read['correct'], read['mapq'], read.get('tags', '.'), aligner_name)] += 1
                    else:
                        writer.line(read['correct'], read['mapq'], read.get('tags', '.'), aligner_name, read['name'], 1)

                for parts, count in list(summary_counts.items()):
                    writer.list_line(list(parts) + ['.', count])

        return context.write_intermediate_file(job, out_filename)


def run_write_position_stats(job, context, map_stats):
    """
    write the position comparison statistics as tsv, both to the Toil fileStore
    and to the out_store as "stats.tsv".
    
    Takes a dict from condition name to stats list of accuracy, AUC, QQ, and F1.
    
    Returns the ID of the file written.
    
    This is different than the stats TSV format used internally, for read stats.
    """
    RealtimeLogger.info('Writing position statistics summary')
    work_dir = job.fileStore.getLocalTempDir()
    stats_file = os.path.join(work_dir, 'stats.tsv')
    with open(stats_file, 'w') as (stats_out):
        stats_out.write('aligner\tcount\tacc\tauc\tqq-r\tmax-f1\n')
        for name, stats in list(map_stats.items()):
            stats_out.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(name, stats[0][0], stats[0][1], stats[1][0], stats[2], stats[3]))

    stats_file_id = context.write_output_file(job, stats_file)
    return stats_file_id


def run_acc(job, context, name, compare_id):
    """
    Percentage of correctly aligned reads (ignore quality)

    Comparison file input must be TSV with one row per read, column 0 unused
    and column 1 as the correct flag.
    """
    RealtimeLogger.info('Computing accuracy')
    work_dir = job.fileStore.getLocalTempDir()
    compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)
    total = 0
    correct = 0
    with open(compare_file) as (compare_f):
        for toks in tsv.TsvReader(compare_f):
            total += 1
            if list(toks)[1] == '1':
                correct += 1

    acc = float(correct) / float(total) if total > 0 else 0
    return (total, acc)


def run_auc(job, context, name, compare_id):
    """
    AUC of roc plot.
    
    ROC plot is defined with mismapped reads being negatives, correctly-mapped
    reads being positives, and AUC expressing how good of a classifier of
    correctly-mapped-ness the MAPQ score is. It says nothing about how well the
    reads are actually mapped.

    Comparison file input must be TSV with one row per read, column 0 unused,
    column 1 as the correct flag, and column 2 as the MAPQ.
    
    """
    RealtimeLogger.info('Computing AUC')
    if not have_sklearn:
        return ['sklearn_not_installed'] * 2
    else:
        work_dir = job.fileStore.getLocalTempDir()
        compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
        job.fileStore.readGlobalFile(compare_id, compare_file)
        try:
            data = np.loadtxt(compare_file, dtype=(np.int), delimiter='\t', usecols=(1,
                                                                                     2)).T
            auc = roc_auc_score(data[0], data[1])
            aupr = average_precision_score(data[0], data[1])
        except:
            auc, aupr = (0, 0)

        return (auc, aupr)


def run_max_f1(job, context, name, compare_id):
    """
    Compute and return maximum F1 score for correctly mapping reads, using MAPQ as a confidence.
    
    The problem is that read mapping is a multi-class classification problem with ~ 1 class per genome base, and F1 is a 2-class classification statistic. So we squish the concept a bit.
    
    For a given MAPQ threshold, we define a fake confusion matrix:
    
    TP = reads meeting threshold mapped correctly
    FP = reads meeting threshold mapped incorrectly
    TN = reads that didn't come from the target graph and didn't meet the threshold (i.e. 0 reads)
    FN = reads that weren't both correctly mapped and assigned a MAPQ meeting the threshold
    
    Then we calculate precision = TP / (TP + FP) and recall = TP / (TP + FN), and from those calculate an F1.
    Then we calculate the best F1 across all the MAPQ values.

    Comparison file input must be TSV with one row per read, column 0 unused,
    column 1 as the correct flag, and column 2 as the MAPQ.
    
    """
    RealtimeLogger.info('Computing max F1')
    if not have_sklearn:
        return 'sklearn_not_installed'
    else:
        work_dir = job.fileStore.getLocalTempDir()
        compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
        job.fileStore.readGlobalFile(compare_id, compare_file)
        data = np.loadtxt(compare_file, dtype=(np.int), delimiter='\t', usecols=(1,
                                                                                 2))
        data = data[data[:, 1].argsort()[::-1]]
        last_mapq = None
        tp = 0
        fp = 0
        tn = 0
        fn = len(data)
        max_f1 = 0

        def emit_f1():
            if tp > 0 or fp > 0 and fn > 0:
                precision = float(tp) / (tp + fp)
                recall = float(tp) / (tp + fn)
                if precision > 0 or recall > 0:
                    f1 = 2 * (precision * recall) / (precision + recall)
                    return max(max_f1, f1)
            return max_f1

        for correct, score in data:
            if score != last_mapq:
                max_f1 = emit_f1()
            else:
                if correct:
                    tp += 1
                else:
                    fp += 1
            fn -= 1

        max_f1 = emit_f1()
        return max_f1


def run_qq(job, context, name, compare_id):
    """
    some measure of qq consistency

    Comparison file input must be TSV with one row per read, column 0 unused,
    column 1 as the correct flag, and column 2 as the MAPQ.
    """
    RealtimeLogger.info('Computing QQ information')
    if not have_sklearn:
        return 'sklearn_not_installed'
    else:
        work_dir = job.fileStore.getLocalTempDir()
        compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
        job.fileStore.readGlobalFile(compare_id, compare_file)
        try:
            data = np.loadtxt(compare_file, dtype=(np.int), delimiter='\t', usecols=(1,
                                                                                     2))
            correct = Counter()
            total = Counter()
            for row in data:
                correct[row[1]] += row[0]
                total[row[1]] += 1

            qual_scores = []
            qual_observed = []
            for qual, cor in list(correct.items()):
                qual_scores.append(qual)
                p_err = max(1.0 - float(cor) / float(total[qual]), sys.float_info.epsilon)
                observed_score = -10.0 * math.log10(p_err)
                qual_observed.append(observed_score)

            r2 = r2_score(qual_observed, qual_scores)
        except:
            r2 = 'fail'

        return r2


def run_map_eval_compare_scores(job, context, baseline_name, baseline_stats_file_id, mapping_condition_dict):
    """
    Compare scores in the given stats files in the lists to those in the given
    baseline stats file.
    
    Takes a dict from condition name to condition results dict, containing a
    'stats' file for each condition.
    
    Stats file format is a TSV of:
    read name, contig name, contig offset, score, mapping quality
    
    Will save the output to the outstore, as a CSV of read name and score
    difference, named <GAM/BAM name>.compare.<baseline name>.scores.
    
    Will also save a concatenated TSV file, with score difference and quoted
    aligner/condition name, as score.results.<baseline_name>.tsv
    
    Returns a dict from condition name to comparison file ID, and the overall
    score results file ID.
    
    For now, just ignores BAMs because we don't pull in pysam to parse out their
    scores.
    
    """
    RealtimeLogger.info('Comparing scores against baseline')
    compare_ids = {}
    for name, condition in list(mapping_condition_dict.items()):
        if 'gam' not in condition:
            pass
        else:
            compare_ids[name] = job.addChildJobFn(compare_scores, context, baseline_name, baseline_stats_file_id, name,
              (condition['stats']), cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.misc_disk)).rv()

    stats_job = job.addFollowOnJobFn(run_process_score_comparisons, context, baseline_name, compare_ids, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk))
    return (
     compare_ids, stats_job.rv())


def run_process_score_comparisons(job, context, baseline_name, compare_ids):
    """
    Write some raw tables of score comparisons against the given baseline to the
    output.  Compute some stats for each graph.
    
    Takes a baseline condition name, and a dict from condition name to score
    comparison file ID.
    
    Returns the file ID of the overall stats file "score.stats.<baseline name>.tsv".
    """
    RealtimeLogger.info('Processing score comparisons')
    work_dir = job.fileStore.getLocalTempDir()
    map_stats = {}
    results_file = os.path.join(work_dir, 'score.{}.results.tsv'.format(baseline_name))
    with open(results_file, 'w') as (out_results_file):
        out_results = tsv.TsvWriter(out_results_file)
        out_results.comment('diff\taligner')

        def write_tsv(comp_file, a):
            with open(comp_file) as (comp_in):
                for line in comp_in:
                    content = line.rstrip()
                    if content != '':
                        toks = content.split(', ')
                        if len(toks) < 2:
                            raise RuntimeError('Invalid comparison file line ' + content)
                        out_results.line(toks[1], a)

        for name, compare_id in list(compare_ids.items()):
            compare_file = os.path.join(work_dir, '{}.compare.{}.scores'.format(name, baseline_name))
            job.fileStore.readGlobalFile(compare_id, compare_file)
            context.write_output_file(job, compare_file)
            write_tsv(compare_file, name)
            map_stats[name] = [
             job.addChildJobFn(run_portion_worse, context, name, compare_id, cores=(context.config.misc_cores),
               memory=(context.config.misc_mem),
               disk=(context.config.misc_disk)).rv()]

    context.write_output_file(job, results_file)
    return job.addFollowOnJobFn(run_write_score_stats, context, baseline_name, map_stats).rv()


def run_write_score_stats(job, context, baseline_name, map_stats):
    """
    write the score comparison statistics against the baseline with the given
    name as tsv named "score.stats.<baseline name>.tsv".
    
    Returns the file ID for that file.
    
    This is different than the stats TSV format used internally, for read stats.
    """
    RealtimeLogger.info('Writing score statistics summary')
    work_dir = job.fileStore.getLocalTempDir()
    stats_file = os.path.join(work_dir, 'score.stats.{}.tsv'.format(baseline_name))
    with open(stats_file, 'w') as (stats_out_file):
        stats_out = tsv.TsvWriter(stats_out_file)
        stats_out.comment('aligner\tcount\tworse')
        for name, stats in list(map_stats.items()):
            stats_out.line(name, stats[0][0], stats[0][1])

    return context.write_output_file(job, stats_file)


def run_portion_worse(job, context, name, compare_id):
    """
    Compute percentage of reads that get worse from the baseline graph.
    Return total reads and portion that got worse.
    """
    RealtimeLogger.info('Computing portion worse than baseline')
    work_dir = job.fileStore.getLocalTempDir()
    compare_file = os.path.join(work_dir, '{}.compare.scores'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)
    total = 0
    worse = 0
    with open(compare_file) as (compare_f):
        for line in compare_f:
            toks = line.split(', ')
            total += 1
            if int(toks[1]) < 0:
                worse += 1

    portion = float(worse) / float(total) if total > 0 else 0
    return (total, portion)


def run_mapeval(job, context, options, xg_file_ids, xg_comparison_ids, gcsa_file_ids, gbwt_file_ids, minimizer_file_ids, distance_file_ids, id_range_file_ids, snarl_file_ids, vg_file_ids, gam_file_ids, reads_gam_file_id, reads_xg_file_id, reads_bam_file_id, reads_fastq_file_ids, fasta_file_id, bwa_index_ids, minimap2_index_id, bam_file_ids, pe_bam_file_ids, true_read_stats_file_id):
    """
    Main Toil job, and main entrypoint for use of vg_mapeval as a library.
    
    Run the analysis on the given files.
    
    TODO: Refactor to use a list of dicts/dict of lists for the indexes.
    
    Returns a pair of the position comparison results and the score comparison
    results.
    
    Each result set is itself a pair, consisting of a list of per-graph file
    IDs, and an overall statistics file ID.

    If evaluation is skipped (options.skip_eval is True), returns None instead
    and just runs the mapping.
    
    """
    RealtimeLogger.info('Running toil-vg mapeval')
    index_job = job.addChildJobFn(run_map_eval_index, context,
      xg_file_ids,
      gcsa_file_ids,
      gbwt_file_ids,
      minimizer_file_ids,
      distance_file_ids,
      id_range_file_ids,
      snarl_file_ids,
      vg_file_ids,
      cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk))
    if not true_read_stats_file_id:
        if reads_gam_file_id:
            annotate_job = index_job.addChildJobFn(annotate_gam, context, reads_xg_file_id, reads_gam_file_id, memory=(context.config.alignment_mem),
              disk=(context.config.alignment_disk))
            true_read_stats_file_id = annotate_job.addFollowOnJobFn(extract_gam_read_stats, context,
              'truth', (annotate_job.rv()), disk=(context.config.alignment_disk)).rv()
    if not true_read_stats_file_id:
        if reads_bam_file_id:
            true_read_stats_file_id = index_job.addChildJobFn(extract_bam_read_stats, context,
              'truth', reads_bam_file_id, True, disk=(context.config.alignment_disk)).rv()
    fq_reads_ids_bwa = reads_fastq_file_ids
    if reads_fastq_file_ids:
        if options.bwa:
            fq_reads_ids_bwa = index_job.addChildJobFn(run_strip_fq_ext, context, reads_fastq_file_ids, disk=(context.config.alignment_disk),
              cores=(context.config.alignment_cores)).rv()
    fastq_fn = run_gam_to_fastq if reads_gam_file_id else run_bam_to_fastq
    fq_reads_ids, fq_paired_reads_ids, fq_paired_reads_for_vg_ids = reads_fastq_file_ids, fq_reads_ids_bwa, reads_fastq_file_ids
    if len(fq_reads_ids) == 2:
        if not options.paired_only:
            fq_reads_ids = [
             index_job.addChildJobFn(run_concat_fastqs, context, fq_reads_ids, disk=(context.config.alignment_disk)).rv()]
    if reads_gam_file_id or reads_bam_file_id:
        if not options.paired_only:
            if not fq_reads_ids:
                fq_reads_ids = index_job.addChildJobFn(fastq_fn, context, (reads_gam_file_id if reads_gam_file_id else reads_bam_file_id),
                  False,
                  disk=(context.config.alignment_disk)).rv()
        if not options.single_only:
            if not fq_paired_reads_ids:
                fq_paired_reads_ids = index_job.addChildJobFn(fastq_fn, context, (reads_gam_file_id if reads_gam_file_id else reads_bam_file_id),
                  True,
                  disk=(context.config.alignment_disk)).rv()
                fq_paired_reads_for_vg_ids = index_job.addChildJobFn(fastq_fn, context, (reads_gam_file_id if reads_gam_file_id else reads_bam_file_id),
                  True,
                  True, disk=(context.config.alignment_disk)).rv()
    matrix = {'aligner':['vg'],  'paired':[],  'mapper':options.mappers, 
     'gbwt':[],  'snarls':[]}
    if not options.paired_only:
        matrix['paired'].append(False)
    if not options.single_only:
        matrix['paired'].append(True)
    if gbwt_file_ids:
        if options.use_gbwt:
            for gbwt_penalty in options.gbwt_penalties:
                matrix['gbwt'].append(gbwt_penalty)

            if len(options.gbwt_penalties) == 0:
                matrix['gbwt'].append(True)
    if not gbwt_file_ids or options.strip_gbwt or not options.use_gbwt:
        matrix['gbwt'].append(False)
    if snarl_file_ids:
        matrix['snarls'].append(True)
    if not snarl_file_ids or options.strip_snarls:
        matrix['snarls'].append(False)
    if options.bwa:
        matrix['aligner'].append('bwa')
    if options.minimap2:
        matrix['aligner'].append('minimap2')
    alignment_job = index_job.addFollowOnJobFn(run_map_eval_align, context, (index_job.rv()), xg_comparison_ids,
      (options.gam_names),
      gam_file_ids, fq_reads_ids,
      fq_paired_reads_ids, fq_paired_reads_for_vg_ids, fasta_file_id,
      matrix, bwa_index_ids=bwa_index_ids,
      minimap2_index_id=minimap2_index_id,
      ignore_quals=(options.ignore_quals),
      surject=(options.surject),
      validate=(options.validate))
    mapping_condition_dict = alignment_job.rv()
    comparison_parent_job = Job()
    alignment_job.addFollowOn(comparison_parent_job)
    comparison_parent_job.addChildJobFn(run_write_map_times, context, mapping_condition_dict)
    if options.skip_eval:
        return
    else:
        comparison_job = comparison_parent_job.addChildJobFn(run_map_eval_comparison, context, mapping_condition_dict, true_read_stats_file_id,
          (options.mapeval_threshold), (options.compare_gam_scores), reads_gam_file_id, downsample_portion=(options.downsample),
          gbwt_usage_tag_gam_name=(options.gbwt_baseline),
          cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.misc_disk))
        plot_sets = parse_plot_sets(options.plot_sets)
        lookup_job = comparison_parent_job.addFollowOnJobFn(lookup_key_path, comparison_job.rv(), [0, 1])
        position_stats_file_id = lookup_job.rv()
        summarize_job = lookup_job.addFollowOnJobFn(run_map_eval_summarize, context, position_stats_file_id, plot_sets, cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.misc_disk))
        return comparison_job.rv()


def lookup_key_path(job, obj, path):
    """
    
    Get the item at the given path of keys by repeated [] lookups in obj.
    
    Work around https://github.com/BD2KGenomics/toil/issues/2214
    
    """
    for key in path:
        obj = obj[key]

    return obj


def run_map_eval_summarize(job, context, position_stats_file_id, plot_sets):
    """
    
    Make the summary plots and tables, based on a single combined position
    stats TSV in position_stats_file_id.
    
    Returns a list of file name and file ID pairs for plots and tables.
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets. The first condition in each
    plot set is used as the comparison baseline.
    
    """
    RealtimeLogger.info('Running summary for {}'.format(plot_sets))
    plot_job = job.addChildJobFn(run_map_eval_plot, context, position_stats_file_id, plot_sets, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk))
    table_job = job.addChildJobFn(run_map_eval_table, context, position_stats_file_id, plot_sets, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk))
    merge_job = plot_job.addFollowOnJobFn(run_concat_lists, (plot_job.rv()), (table_job.rv()), cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk))
    table_job.addFollowOn(merge_job)
    return merge_job.rv()


def run_map_eval_plot(job, context, position_stats_file_id, plot_sets):
    """
    
    Make the PR and QQ plots with R, based on a single combined position stats
    TSV in position_stats_file_id.
    
    The combined position stats TSV has one header line, and format:
    
    correct flag, mapping quality, tag list (or '.'), method name, read name (or '.'), weight (or 1)
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets.
    
    outputs plots/plot-pr.svg, plots/plot-qq.svg, and plots/plot-roc.svg for
    the first set, and plots/plot-pr-1.svg, etc. for subsequent sets.
    
    Returns a list of pairs of tuples of plot basename, plot file ID, and plot file path.
    
    """
    RealtimeLogger.info('Starting plotting...')
    work_dir = job.fileStore.getLocalTempDir()
    position_stats_path = os.path.join(work_dir, 'position_stats.tsv')
    job.fileStore.readGlobalFile(position_stats_file_id, position_stats_path)
    out_plot_tuples = []
    for i, plot_set in enumerate(plot_sets):
        plot_title, plot_conditions = plot_set
        for rscript in ('pr', 'qq', 'roc'):
            RealtimeLogger.info('Plotting {} for plot set {}'.format(rscript, i))
            plot_filename = title_to_filename('plot-{}'.format(rscript), i, plot_title, 'svg')
            script_path = get_vg_script(job, context.runner, 'plot-{}.R'.format(rscript), work_dir)
            set_r_cran_url(script_path)
            cmd = ['Rscript', os.path.basename(script_path), os.path.basename(position_stats_path),
             plot_filename]
            if plot_conditions is not None:
                cmd.append(','.join(plot_conditions))
                if plot_title is not None:
                    cmd.append(plot_title)
            try:
                context.runner.call(job, cmd, work_dir=work_dir)
                out_plot_tuples.append((plot_filename,
                 context.write_output_file(job, os.path.join(work_dir, plot_filename), os.path.join('plots', plot_filename))))
            except Exception as e:
                if rscript == 'roc':
                    RealtimeLogger.warning('plot-roc.R failed: {}'.format(str(e)))
                else:
                    raise e

    RealtimeLogger.info('Plotting complete')
    return out_plot_tuples


def run_map_eval_table(job, context, position_stats_file_id, plot_sets):
    """
    
    Make table TSVs of wrong/correct/improved read counts.
    
    The combined position stats TSV has one header line, and format:
    
    correct flag, mapping quality, tag list (or '.'), method name, read name (or '.'), weight (or 1)
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets. The first condition in each
    plot set is used as the comparison baseline.
    
    outputs plots/table.tsv for the first set, and plots/table-1.svg, etc. for
    subsequent sets.
    
    Returns a list of pairs of table file name and table file ID.
    
    """
    RealtimeLogger.info('Downloading mapeval stats for table...')
    work_dir = job.fileStore.getLocalTempDir()
    position_stats_path = os.path.join(work_dir, 'position_stats.tsv')
    job.fileStore.readGlobalFile(position_stats_file_id, position_stats_path)
    RealtimeLogger.info('Making mapeval summary table...')
    dict_for_condition = lambda : {'wrong':0, 
     'wrongTagged':collections.Counter(), 
     'wrong60':0, 
     'wrong0':0, 
     'wrong>0':0, 
     'correct':0, 
     'correctTagged':collections.Counter(), 
     'correct0':0, 
     'correctMapqTotal':0, 
     'wrongNames':set()}
    condition_stats = collections.defaultdict(dict_for_condition)
    known_tags = set()
    line_num = 0
    with open(position_stats_path) as (stats_stream):
        for line in tsv.TsvReader(stats_stream):
            line = list(line)
            if line_num == 0:
                line_num += 1
                continue
            line_num += 1
            if line_num % 1000000 == 0:
                RealtimeLogger.info('Processed {} alignments for table in {} conditions'.format(line_num, len(condition_stats)))
            if len(line) == 0:
                pass
            else:
                if not len(line) >= 6:
                    raise AssertionError
                else:
                    correct, mapq, tags, condition, read, count = line[0:6]
                    correct = correct == '1'
                    mapq = int(mapq)
                    tags = [] if tags == '.' else tags.split(',')
                    count = int(count)
                    if tags == []:
                        known_tags.add(None)
                    else:
                        for tag in tags:
                            known_tags.add(tag)

                stats = condition_stats[condition]
                if correct:
                    stats['correct'] += count
                    stats['correct0'] += (mapq == 0) * count
                    stats['correctMapqTotal'] += mapq * count
                    if tags == []:
                        stats['correctTagged'][None] += count
                    else:
                        for tag in tags:
                            stats['correctTagged'][tag] += count

                else:
                    stats['wrong'] += count
                    stats['wrong60'] += (mapq == 60) * count
                    stats['wrong0'] += (mapq == 0) * count
                    stats['wrong>0'] += (mapq > 0) * count
                    stats['wrongNames'].add(read)
                    if tags == []:
                        stats['wrongTagged'][None] += count
                    else:
                        for tag in tags:
                            stats['wrongTagged'][tag] += count

    known_tags = sorted(list(known_tags))
    if len(known_tags) == 1:
        known_tags = []
    out_name_id_pairs = []
    for i, plot_set in enumerate(plot_sets):
        RealtimeLogger.info('Create table for plot set {}'.format(i))
        plot_title, plot_conditions = plot_set
        table_filename = title_to_filename('table', i, plot_title, 'tsv')
        if plot_conditions is None:
            plot_conditions = list(condition_stats.keys())
        assert len(plot_conditions) > 0
        baseline_condition = plot_conditions[0]
        writer = tsv.TsvWriter(open(os.path.join(work_dir, table_filename), 'w'))
        header = ['Condition', 'Precision']
        for tag in known_tags:
            header.append('+{}'.format(tag))
            header.append('-{}'.format(tag))

        header.append('Reads')
        for tag in known_tags:
            header.append('+{}'.format(tag))
            header.append('-{}'.format(tag))

        header.append('Wrong')
        for tag in known_tags:
            header.append('+{}'.format(tag))
            header.append('-{}'.format(tag))

        header += ['at MAPQ 60', 'at MAPQ 0', 'at MAPQ >0', 'new vs. ' + baseline_condition, 'fixed vs. ' + baseline_condition,
         'Avg. Correct MAPQ', 'Correct MAPQ 0']
        writer.list_line(header)
        for condition in plot_conditions:
            stats = condition_stats[condition]
            line = [
             condition]
            try:
                line.append(float(stats['correct']) / (stats['wrong'] + stats['correct']))
            except ZeroDivisionError:
                line.append('NaN')

            for tag in known_tags:
                try:
                    line.append(float(stats['correctTagged'][tag]) / (stats['wrongTagged'][tag] + stats['correctTagged'][tag]))
                except ZeroDivisionError:
                    line.append('NaN')

                try:
                    line.append(float(stats['correct'] - stats['correctTagged'][tag]) / (stats['wrong'] - stats['wrongTagged'][tag] + (stats['correct'] - stats['correctTagged'][tag])))
                except ZeroDivisionError:
                    line.append('NaN')

            line.append(stats['wrong'] + stats['correct'])
            for tag in known_tags:
                line.append(stats['wrongTagged'][tag] + stats['correctTagged'][tag])
                line.append(stats['wrong'] - stats['wrongTagged'][tag] + (stats['correct'] - stats['correctTagged'][tag]))

            line.append(stats['wrong'])
            for tag in known_tags:
                line.append(stats['wrongTagged'][tag])
                line.append(stats['wrong'] - stats['wrongTagged'][tag])

            line.append(stats['wrong60'])
            line.append(stats['wrong0'])
            line.append(stats['wrong>0'])
            new_vs_baseline = 0
            for read in stats['wrongNames']:
                if read not in condition_stats[baseline_condition]['wrongNames']:
                    new_vs_baseline += 1

            line.append(new_vs_baseline)
            fixed_vs_baseline = 0
            for read in condition_stats[baseline_condition]['wrongNames']:
                if read not in stats['wrongNames']:
                    fixed_vs_baseline += 1

            line.append(fixed_vs_baseline)
            if stats['correct'] != 0:
                avg_correct_mapq = float(stats['correctMapqTotal']) / stats['correct']
            else:
                avg_correct_mapq = None
            line.append(avg_correct_mapq)
            line.append(stats['correct0'])
            writer.list_line(line)

        writer.close()
        out_name_id_pairs.append((table_filename,
         context.write_output_file(job, os.path.join(work_dir, table_filename), os.path.join('plots', table_filename))))

    RealtimeLogger.info('Tables complete')
    return out_name_id_pairs


def run_write_map_times(job, context, mapping_condition_dict):
    """
    Make a table of running times (in seconds) for mapping.  These times do not include 
    toil-vg overhead like downloading and chunking
    
    Takes in a dict by mapped condition name of condition dicts, each may have
    a "runtime" key with a float runtime in seconds.
    """
    RealtimeLogger.info('Writing mapping times')
    work_dir = job.fileStore.getLocalTempDir()
    times_path = os.path.join(work_dir, 'map_times.tsv')
    with open(times_path, 'w') as (times_file):
        times_file.write('aligner\tmap time (s)\n')
        for name, results in list(mapping_condition_dict.items()):
            if results.get('runtime') is not None:
                times_file.write('{}\t{}\n'.format(name, round(results.get('runtime'), 5)))

    context.write_output_file(job, times_path)


def make_mapeval_plan(toil, options):
    """
    Import all the necessary files form options into Toil.
    
    Keep the IDs under names in an argparse namespace that functions as a "plan"
    for the workflow.
    
    """
    plan = argparse.Namespace()
    importer = AsyncImporter(toil)
    plan.gam_file_ids = []
    if options.gams:
        for gam in options.gams:
            plan.gam_file_ids.append(importer.load(gam))

    plan.vg_file_ids = []
    if options.vg_graphs:
        for graph in options.vg_graphs:
            plan.vg_file_ids.append(importer.load(graph))

    plan.xg_file_ids = []
    plan.xg_comparison_ids = []
    plan.gcsa_file_ids = []
    plan.gbwt_file_ids = []
    plan.minimizer_file_ids = []
    plan.distance_file_ids = []
    plan.id_range_file_ids = []
    plan.snarl_file_ids = []
    imported_xgs = {}
    if options.index_bases:
        for ib in options.index_bases:
            if ',' in ib:
                ib, cib = ib.split(',')[0], make_url(ib.split(',')[1])
            else:
                cib = ib
            imported_xgs[ib + '.xg'] = importer.load(ib + '.xg')
            plan.xg_file_ids.append(imported_xgs[(ib + '.xg')])
            if cib:
                if cib + '.xg' not in imported_xgs:
                    imported_xgs[cib + '.xg'] = importer.load(cib + '.xg')
                plan.xg_comparison_ids.append(imported_xgs[(cib + '.xg')])
                if not options.gams:
                    if 'map' in options.mappers or 'mpmap' in options.mappers:
                        plan.gcsa_file_ids.append((
                         importer.load(ib + '.gcsa'),
                         importer.load(ib + '.gcsa.lcp')))
                    try:
                        plan.gbwt_file_ids.append(toil.importFile(ib + '.gbwt'))
                    except:
                        if 'gaffe' not in options.mappers:
                            plan.gbwt_file_ids.append(None)
                        else:
                            raise

                    if 'gaffe' in options.mappers:
                        plan.minimizer_file_ids.append(importer.load(ib + '.min'))
                        plan.distance_file_ids.append(importer.load(ib + '.dist'))
                    if options.use_snarls:
                        try:
                            plan.snarl_file_ids.append(toil.importFile(ib + '.snarls'))
                        except:
                            plan.snarl_file_ids.append(None)

    else:
        plan.reads_xg_file_id = None
        if options.gam_input_xg:
            if options.gam_input_xg in imported_xgs:
                plan.reads_xg_file_id = imported_xgs[options.gam_input_xg]
            else:
                plan.reads_xg_file_id = importer.load(options.gam_input_xg)
        if options.gam_input_reads:
            plan.reads_gam_file_id = importer.load(options.gam_input_reads)
        else:
            plan.reads_gam_file_id = None
        if options.bam_input_reads:
            plan.reads_bam_file_id = importer.load(options.bam_input_reads)
        else:
            plan.reads_bam_file_id = None
    plan.reads_fastq_file_ids = []
    if options.fastq:
        for sample_reads in options.fastq:
            plan.reads_fastq_file_ids.append(importer.load(sample_reads))

    plan.bam_file_ids = []
    if options.bams:
        for bam in options.bams:
            plan.bam_file_ids.append(importer.load(bam))

    plan.pe_bam_file_ids = []
    if options.pe_bams:
        for bam in options.pe_bams:
            plan.pe_bam_file_ids.append(importer.load(bam))

    else:
        plan.fasta_file_id = None
        plan.bwa_index_ids = None
        plan.minimap2_index_id = None
        if options.fasta:
            plan.fasta_file_id = importer.load(options.fasta)
            plan.bwa_index_ids = dict()
            for suf in ('.amb', '.ann', '.bwt', '.pac', '.sa'):
                fidx = '{}{}'.format(options.fasta, suf)
                try:
                    plan.bwa_index_ids[suf] = toil.importFile(fidx)
                except:
                    logger.info('No bwa index found for {}, will regenerate if needed'.format(options.fasta))
                    plan.bwa_index_ids = None
                    break

            try:
                plan.minimap2_index_id = toil.importFile('{}{}'.format(options.fasta, '.mmi'))
            except:
                logger.info('No minimap2 index found for {}, will regenerate if needed'.format(options.fasta))

        if options.truth:
            plan.true_read_stats_file_id = importer.load(options.truth)
        else:
            plan.true_read_stats_file_id = None
    importer.wait()
    return importer.resolve(plan)


def mapeval_main(context, options):
    """
    Run the mapeval workflow.
    """
    validate_options(options)
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    t = copy.deepcopy(context)
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            plan = make_mapeval_plan(toil, options)
            main_job = Job.wrapJobFn(run_mapeval, context, options, plan.xg_file_ids, plan.xg_comparison_ids, plan.gcsa_file_ids, plan.gbwt_file_ids, plan.minimizer_file_ids, plan.distance_file_ids, plan.id_range_file_ids, plan.snarl_file_ids, plan.vg_file_ids, plan.gam_file_ids, plan.reads_gam_file_id, plan.reads_xg_file_id, plan.reads_bam_file_id, plan.reads_fastq_file_ids, plan.fasta_file_id, plan.bwa_index_ids, plan.minimap2_index_id, plan.bam_file_ids, plan.pe_bam_file_ids, plan.true_read_stats_file_id)
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, (sys.argv), memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            init_job.addFollowOn(main_job)
            toil.start(init_job)
        else:
            toil.restart()
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
    logger.info('All jobs completed successfully. Pipeline took {} seconds.'.format(run_time_pipeline))