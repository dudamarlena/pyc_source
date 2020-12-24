# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_surject.py
# Compiled at: 2020-04-30 13:47:21
# Size of source mod 2**32: 11194 bytes
"""
vg_surject.py: chunked surject of gam file

"""
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, struct, socket, threading, string, getpass, pdb, gzip, logging
from math import ceil
from subprocess import Popen, PIPE
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import *
from toil_vg.context import Context, run_write_info_to_outstore
from toil_vg.vg_map import *
logger = logging.getLogger(__name__)

def surject_subparser(parser):
    """
    Create a subparser for surjecting.  Should pass in results of subparsers.add_parser()
    """
    Job.Runner.addToilOptions(parser)
    parser.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    parser.add_argument('--xg_index', type=make_url, required=True, help='Path to xg index')
    parser.add_argument('--paths', nargs='+', default=[], help='list of path names to surject to (default: all in xg)')
    parser.add_argument('--interleaved', action='store_true', default=False, help='treat gam as interleaved read pairs.  overrides map-args')
    parser.add_argument('--gam_input_reads', type=make_url, required=True, help='Input reads in GAM format')
    parser.add_argument('--single_reads_chunk', action='store_true', default=False, help='do not split reads into chunks')
    parser.add_argument('--reads_per_chunk', type=int, help='number of reads for each mapping job')
    parser.add_argument('--alignment_cores', type=int, help='number of threads during the alignment step')
    add_common_vg_parse_args(parser)
    add_container_tool_parse_args(parser)


def run_surjecting(job, context, gam_input_reads_id, output_name, interleaved, xg_file_id, paths):
    """ split the fastq, then surject each chunk.  returns outputgams, paired with total surject time
    (excluding toil-vg overhead such as transferring and splitting files )"""
    child_job = Job()
    job.addChild(child_job)
    if not context.config.single_reads_chunk:
        reads_chunk_ids = child_job.addChildJobFn(run_split_reads, context, None, 'aln.gam', None, [
         gam_input_reads_id],
          cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.misc_disk)).rv()
    else:
        RealtimeLogger.info('Bypassing reads splitting because --single_reads_chunk enabled')
        reads_chunk_ids = [[r] for r in [gam_input_reads_id]]
    return child_job.addFollowOnJobFn(run_whole_surject, context, reads_chunk_ids, output_name, interleaved,
      xg_file_id, paths, cores=(context.config.misc_cores), memory=(context.config.misc_mem),
      disk=(context.config.misc_disk)).rv()


def run_whole_surject(job, context, reads_chunk_ids, output_name, interleaved, xg_file_id, paths):
    """
    Surject all gam chunks in parallel.
    
    surject all the GAM file IDs in read_chunk_ids, saving the merged BAM as output_name.
    
    If interleaved is true, expects paired-interleaved GAM input and writes paired BAM output.
    
    Surjects against the given collection of paths in the given XG file.
    
    """
    RealtimeLogger.info('Surjecting read chunks {} to BAM'.format(reads_chunk_ids))
    bam_chunk_file_ids = []
    bam_chunk_running_times = []
    child_job = Job()
    job.addChild(child_job)
    for chunk_id, chunk_filename_ids in enumerate(zip(*reads_chunk_ids)):
        chunk_surject_job = child_job.addChildJobFn(run_chunk_surject, context, interleaved, xg_file_id, paths,
          chunk_filename_ids, ('{}_chunk{}'.format(output_name, chunk_id)), cores=(context.config.alignment_cores),
          memory=(context.config.alignment_mem),
          disk=(context.config.alignment_disk))
        bam_chunk_file_ids.append(chunk_surject_job.rv(0))
        bam_chunk_running_times.append(chunk_surject_job.rv(1))

    return child_job.addFollowOnJobFn(run_merge_bams, output_name, context, bam_chunk_file_ids, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk)).rv()


def run_chunk_surject(job, context, interleaved, xg_file_id, paths, chunk_filename_ids, chunk_id):
    """ run surject on a chunk.  interface mostly copied from run_chunk_alignment.
    
    Takes an xg file and path colleciton to surject against, a list of chunk
    file IDs (must be just one possibly-interleaved chunk for now), and an
    identifying name/number/string (chunk_id) for the chunk.
    
    If interleaved is true, expects paired-interleaved GAM input and writes paired BAM output.
    
    Returns a single-element list of the resulting BAM file ID, and the run time in seconds.
    
    """
    assert len(chunk_filename_ids) == 1
    run_time = None
    work_dir = job.fileStore.getLocalTempDir()
    xg_file = os.path.join(work_dir, 'index.xg')
    job.fileStore.readGlobalFile(xg_file_id, xg_file)
    gam_files = []
    reads_ext = 'gam'
    for j, chunk_filename_id in enumerate(chunk_filename_ids):
        gam_file = os.path.join(work_dir, 'reads_chunk_{}_{}.{}'.format(chunk_id, j, reads_ext))
        job.fileStore.readGlobalFile(chunk_filename_id, gam_file)
        gam_files.append(gam_file)

    output_file = os.path.join(work_dir, 'surject_{}.bam'.format(chunk_id))
    with open(output_file, 'wb') as (surject_file):
        cmd = ['vg', 'surject', os.path.basename(gam_files[0]), '--bam-output']
        if interleaved:
            cmd += ['--interleaved']
        cmd += ['-x', os.path.basename(xg_file)]
        for surject_path in paths:
            cmd += ['--into-path', surject_path]

        cmd += ['-t', str(context.config.alignment_cores)]
        start_time = timeit.default_timer()
        try:
            context.runner.call(job, cmd, work_dir=work_dir, outfile=surject_file)
        except:
            logging.error('Surjection failed. Dumping files.')
            context.write_output_file(job, xg_file)
            for gam_file in gam_files:
                context.write_output_file(job, gam_file)

            raise

        end_time = timeit.default_timer()
        run_time = end_time - start_time
    return ([context.write_intermediate_file(job, output_file)], run_time)


def run_merge_bams(job, output_name, context, bam_chunk_file_ids):
    """
    Merge together bams.
    
    Takes a list of lists of BAM file IDs to merge.
    
    TODO: Context ought to always be the second argument, after job.
    """
    flat_ids = [x for l in bam_chunk_file_ids for x in l]
    requeue_promise = ensure_disk(job, run_merge_bams, [output_name, context, bam_chunk_file_ids], {}, flat_ids,
      factor=2)
    if requeue_promise is not None:
        return requeue_promise
    else:
        work_dir = job.fileStore.getLocalTempDir()
        chunk_paths = [os.path.join(work_dir, 'chunk_{}.bam'.format(i)) for i in range(len(flat_ids))]
        for i, bam_chunk_file_id in enumerate(flat_ids):
            job.fileStore.readGlobalFile(bam_chunk_file_id, chunk_paths[i])

        surject_path = os.path.join(work_dir, '{}.bam'.format(output_name))
        cmd = [
         'samtools', 'cat'] + [os.path.basename(chunk_path) for chunk_path in chunk_paths]
        cmd += ['-o', os.path.basename(surject_path)]
        context.runner.call(job, cmd, work_dir=work_dir)
        return context.write_output_file(job, surject_path)


def surject_main(context, options):
    """
    Wrapper for vg surject. 
    """
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            importer = AsyncImporter(toil)
            inputXGFileID = importer.load(options.xg_index)
            inputGAMFileID = importer.load(options.gam_input_reads)
            importer.wait()
            root_job = Job.wrapJobFn(run_surjecting, context, (importer.resolve(inputGAMFileID)), 'surject', (options.interleaved),
              (importer.resolve(inputXGFileID)),
              (options.paths), cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, (sys.argv), memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            init_job.addFollowOn(root_job)
            toil.start(init_job)
        else:
            toil.restart()
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
    logger.info('All jobs completed successfully. Pipeline took {} seconds.'.format(run_time_pipeline))