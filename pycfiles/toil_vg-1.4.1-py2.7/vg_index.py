# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_index.py
# Compiled at: 2018-11-03 15:09:40
"""
vg_index.py: index a graph so it can be mapped to

"""
from __future__ import print_function
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, SocketServer, struct, socket, threading, string, urlparse, getpass, pdb, logging
from math import ceil
from subprocess import Popen, PIPE
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import *
from toil_vg.context import Context, run_write_info_to_outstore
logger = logging.getLogger(__name__)

def index_subparser(parser):
    """
    Create a subparser for indexing.  Should pass in results of subparsers.add_parser()
    """
    Job.Runner.addToilOptions(parser)
    parser.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    parser.add_argument('--graphs', nargs='+', default=[], type=make_url, help='input graph(s). one per chromosome (separated by space)')
    parser.add_argument('--chroms', nargs='+', help='name(s) of reference path in graph(s) (separated by space).  If --graphs  has multiple elements, must be same length/order as --chroms (not needed for xg_index)')
    parser.add_argument('--node_mapping', type=make_url, help='node mapping file required for gbwt pruning. Created by toil-vg construct (or vg ids -j)')
    parser.add_argument('--bwa_index_fasta', type=make_url, help='index the given FASTA for BWA MEM alignment')
    add_common_vg_parse_args(parser)
    index_toggle_parse_args(parser)
    index_parse_args(parser)
    add_container_tool_parse_args(parser)


def index_toggle_parse_args(parser):
    """
    Common args we do not want to share with toil-vg run, and which toggle
    different index types on and off.
    
    Safe to use in toil-vg construct without having to import any files.
    """
    parser.add_argument('--gcsa_index', action='store_true', help='Make a gcsa index for each output graph')
    parser.add_argument('--xg_index', action='store_true', help='Make an xg index for each output graph')
    parser.add_argument('--gbwt_index', action='store_true', help='Make a GBWT index alongside the xg index for each output graph')
    parser.add_argument('--snarls_index', action='store_true', help='Make an snarls file for each output graph')
    parser.add_argument('--id_ranges_index', action='store_true', help='Make chromosome id ranges tables (so toil-vg map can optionally split output by chromosome)')
    parser.add_argument('--all_index', action='store_true', help='Equivalent to --gcsa_index --xg_index --gbwt_index --snarls_index --id_ranges_index')


def index_parse_args(parser):
    """
    Indexing parameters which can be part of the main toil-vg run pipeline.
    """
    parser.add_argument('--gcsa_index_cores', type=int, help='number of threads during the gcsa indexing step')
    parser.add_argument('--xg_index_cores', type=int, help='number of threads during the xg indexing step')
    parser.add_argument('--gbwt_index_cores', type=int, help='number of threads during the gbwt indexing step')
    parser.add_argument('--index_name', type=str, default='index', help='name of index files. <name>.xg, <name>.gcsa etc.')
    parser.add_argument('--gcsa_opts', type=str, help='Options to pass to gcsa indexing.')
    parser.add_argument('--vcf_phasing', nargs='+', type=make_url, default=[], help='Import phasing information from VCF(s) into xg (or GBWT with --gbwt_index)')
    parser.add_argument('--vcf_phasing_regions', nargs='+', default=[], help='Hint the relevant chrom:start-end regions to the GBWT indexer, for subregion graphs')
    parser.add_argument('--gbwt_input', type=make_url, help='Use given GBWT for GCSA2 pruning')
    parser.add_argument('--gbwt_prune', action='store_true', help='Use gbwt for gcsa pruning')


def validate_index_options(options):
    """
    Throw an error if an invalid combination of options has been selected.
    """
    if any([options.gcsa_index, options.snarls_index,
     options.id_ranges_index, options.gbwt_index, options.all_index]):
        require(len(options.graphs) == 0 or options.chroms, '--chroms must be specified for --graphs')
        require(len(options.graphs) == 1 or len(options.chroms) == len(options.graphs), '--chroms and --graphs must have same number of arguments if more than one graph specified if doing anything but xg indexing')
    require(any([options.xg_index, options.gcsa_index, options.snarls_index,
     options.id_ranges_index, options.gbwt_index, options.all_index, options.bwa_index_fasta]), 'one of --xg_index, --gcsa_index, --snarls_index, --id_ranged_index, --gbwt_index, --all_index, or --bwa_index_fasta is required')
    require(not options.gbwt_prune or options.node_mapping, '--node_mapping required with --gbwt_prune')
    if options.vcf_phasing:
        require(all([ vcf.endswith('.vcf.gz') for vcf in options.vcf_phasing ]), 'input phasing files must end with .vcf.gz')
    if options.gbwt_index:
        require(options.vcf_phasing, 'generating a GBWT requires a VCF with phasing information')
    if options.gbwt_prune:
        require(options.gbwt_index or options.gbwt_input, '--gbwt_index or --gbwt_input required for --gbwt_prune')
        require(options.gcsa_index or options.all_index, '--gbwt_prune requires gbwt indexing')
    require(not options.gbwt_index or not options.gbwt_input, 'only one of --gbwt_index and --gbwt_input can be used at a time')
    if options.gbwt_input:
        require(options.gbwt_prune == 'gbwt', '--gbwt_prune required with --gbwt_input')
    if options.vcf_phasing_regions:
        require(options.gbwt_index, 'cannot hint regions to GBWT indexer without building a GBWT index')


def run_gcsa_prune(job, context, graph_name, input_graph_id, gbwt_id, mapping_id):
    """
    Make a pruned graph using vg prune.  If unfold_mapping_id is provided, use -u, else -r
    """
    RealtimeLogger.info(('Starting GCSA graph-pruning {}...').format('using GBWT' if gbwt_id else ''))
    start_time = timeit.default_timer()
    work_dir = job.fileStore.getLocalTempDir()
    restored_filename = os.path.join(work_dir, ('restored_{}').format(graph_name))
    pruned_filename = os.path.join(work_dir, ('unfolded_{}').format(graph_name))
    mapping_filename = os.path.join(work_dir, 'node_mapping')
    graph_filename = os.path.join(work_dir, graph_name)
    job.fileStore.readGlobalFile(input_graph_id, graph_filename)
    gbwt_filename = graph_filename + '.gbwt'
    if gbwt_id:
        job.fileStore.readGlobalFile(gbwt_id, gbwt_filename)
    if mapping_id:
        job.fileStore.readGlobalFile(mapping_id, mapping_filename, mutable=True)
    cmd = ['vg', 'prune', os.path.basename(graph_filename), '--threads', str(job.cores)]
    if context.config.prune_opts:
        cmd += context.config.prune_opts
    if gbwt_id:
        cmd += ['--append-mapping', '--mapping', os.path.basename(mapping_filename), '--unfold-paths']
        cmd += ['--gbwt-name', os.path.basename(gbwt_filename)]
    else:
        cmd += ['--restore-paths']
    with open(pruned_filename, 'w') as (pruned_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=pruned_file)
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info(('Finished GCSA pruning. Process took {} seconds.').format(run_time))
    pruned_graph_id = context.write_intermediate_file(job, pruned_filename)
    if gbwt_id:
        mapping_id = context.write_intermediate_file(job, mapping_filename)
    else:
        mapping_id = None
    return (pruned_graph_id, mapping_id)


def run_gcsa_prep(job, context, input_graph_ids, graph_names, index_name, chroms, chrom_gbwt_ids, node_mapping_id, skip_pruning=False):
    """
    Do all the preprocessing for gcsa indexing (pruning)
    Then launch the indexing as follow-on
    """
    RealtimeLogger.info('Starting gcsa preprocessing...')
    start_time = timeit.default_timer()
    assert chrom_gbwt_ids and len(chrom_gbwt_ids) <= len(input_graph_ids)
    child_job = Job()
    job.addChild(child_job)
    prune_root_job = Job()
    child_job.addChild(prune_root_job)
    prune_jobs = []
    mapping_ids = [node_mapping_id] if node_mapping_id and chrom_gbwt_ids else []
    prune_ids = []
    for graph_i, input_graph_id in enumerate(input_graph_ids):
        gbwt_id = chrom_gbwt_ids[graph_i] if chrom_gbwt_ids else None
        mapping_id = mapping_ids[(-1)] if mapping_ids else None
        prev_job = prune_jobs[(-1)] if prune_jobs and gbwt_id else prune_root_job
        if not skip_pruning:
            prune_job = prev_job.addFollowOnJobFn(run_gcsa_prune, context, graph_names[graph_i], input_graph_id, gbwt_id, mapping_id, cores=context.config.prune_cores, memory=context.config.prune_mem, disk=context.config.prune_disk)
            prune_id = prune_job.rv(0)
            if gbwt_id:
                prune_jobs.append(prune_job)
                mapping_ids.append(prune_job.rv(1))
        else:
            prune_id = input_graph_id
        prune_ids.append(prune_id)

    return child_job.addFollowOnJobFn(run_gcsa_indexing, context, prune_ids, graph_names, index_name, mapping_ids[(-1)] if mapping_ids else None, cores=context.config.gcsa_index_cores, memory=context.config.gcsa_index_mem, disk=context.config.gcsa_index_disk, preemptable=context.config.gcsa_index_preemptable).rv()


def run_gcsa_indexing(job, context, prune_ids, graph_names, index_name, mapping_id):
    """
    Make the gcsa2 index. Return its store id
    """
    RealtimeLogger.info('Starting gcsa indexing...')
    start_time = timeit.default_timer()
    work_dir = job.fileStore.getLocalTempDir()
    index_temp_dir = os.path.join(work_dir, 'index-temp')
    os.makedirs(index_temp_dir)
    prune_filenames = []
    for graph_i, prune_id in enumerate(prune_ids):
        prune_filename = os.path.join(work_dir, os.path.basename(graph_names[graph_i]) + '.prune')
        job.fileStore.readGlobalFile(prune_id, prune_filename)
        prune_filenames.append(prune_filename)

    mapping_filename = None
    if mapping_id:
        mapping_filename = os.path.join(work_dir, 'node_mapping')
        job.fileStore.readGlobalFile(mapping_id, mapping_filename)
    gcsa_filename = ('{}.gcsa').format(index_name)
    command = [
     'vg', 'index', '--gcsa-name', os.path.basename(gcsa_filename)] + context.config.gcsa_opts
    command += ['--threads', str(job.cores)]
    command += ['--temp-dir', os.path.join('.', os.path.basename(index_temp_dir))]
    if mapping_id:
        command += ['--mapping', os.path.basename(mapping_filename)]
    for prune_filename in prune_filenames:
        command += [os.path.basename(prune_filename)]

    context.runner.call(job, command, work_dir=work_dir)
    gcsa_file_id = context.write_output_file(job, os.path.join(work_dir, gcsa_filename))
    lcp_file_id = context.write_output_file(job, os.path.join(work_dir, gcsa_filename) + '.lcp')
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info(('Finished GCSA index. Process took {} seconds.').format(run_time))
    return (
     gcsa_file_id, lcp_file_id)


def run_concat_vcfs(job, context, vcf_ids, tbi_ids):
    """
    concatenate a list of vcfs.  we do this because vg index -v only takes one vcf, and
    we may be working with a set of chromosome vcfs. 
    """
    work_dir = job.fileStore.getLocalTempDir()
    vcf_names = [ ('chrom_{}.vcf.gz').format(i) for i in range(len(vcf_ids)) ]
    out_name = 'genome.vcf.gz'
    for vcf_id, tbi_id, vcf_name in zip(vcf_ids, tbi_ids, vcf_names):
        job.fileStore.readGlobalFile(vcf_id, os.path.join(work_dir, vcf_name))
        job.fileStore.readGlobalFile(tbi_id, os.path.join(work_dir, vcf_name + '.tbi'))

    cmd = ['bcftools', 'concat'] + [ vcf_name for vcf_name in vcf_names ] + ['-O', 'z']
    with open(os.path.join(work_dir, out_name), 'w') as (out_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
    cmd = ['tabix', '-f', '-p', 'vcf', out_name]
    context.runner.call(job, cmd, work_dir=work_dir)
    out_vcf_id = context.write_intermediate_file(job, os.path.join(work_dir, out_name))
    out_tbi_id = context.write_intermediate_file(job, os.path.join(work_dir, out_name + '.tbi'))
    return (
     out_vcf_id, out_tbi_id)


def run_concat_graphs(job, context, inputGraphFileIDs, graph_names, index_name, intermediate=False):
    """
    Concatenate a list of graph files. We do this because the haplotype index vg index
    produces can only be built for a single graph.
    
    Takes the file IDs to concatenate, the human-readable names for those
    files, and the base name of the index we are working on (which is used to
    derive the graph output name).
    
    Graph files to concatenate must already be in the same ID space.
    
    If intermediate is set to true, the concatenated graph is not written to
    the output store.
    
    """
    work_dir = job.fileStore.getLocalTempDir()
    RealtimeLogger.info('Starting VG graph concatenation...')
    start_time = timeit.default_timer()
    concatenated_basename = ('{}.cat.vg').format(index_name)

    def concat_to_stream(out_stream):
        """
        Send all the input graphs to the given file object.
        """
        for in_id in inputGraphFileIDs:
            with job.fileStore.readGlobalFileStream(in_id) as (in_stream):
                shutil.copyfileobj(in_stream, out_stream)

    concatenated_file_id = None
    if intermediate:
        with job.fileStore.writeGlobalFileStream() as (out_stream, out_id):
            concat_to_stream(out_stream)
            concatenated_file_id = out_id
    else:
        concatenated_filename = os.path.join(work_dir, concatenated_basename)
        with open(concatenated_filename, 'wb') as (out_stream):
            concat_to_stream(out_stream)
        concatenated_file_id = context.write_output_file(job, concatenated_filename)
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info(('Finished VG graph concatenation. Process took {} seconds.').format(run_time))
    return (
     concatenated_file_id, concatenated_basename)


def run_xg_indexing(job, context, inputGraphFileIDs, graph_names, index_name, vcf_phasing_file_id=None, tbi_phasing_file_id=None, make_gbwt=False, gbwt_regions=[], separate_threads=False, use_thread_dbs=None, intermediate=False):
    """

    Make the xg index and optional GBWT haplotype index.
    
    Saves the xg in the outstore as <index_name>.xg and the GBWT, if requested,
    as <index_name>.gbwt.
    
    If gbwt_regions is specified, it is a list of chrom:start-end region
    specifiers, restricting, on each specified chromosome, the region of the
    VCF that GBWT indexing will examine.
    
    If separate_threads is specified, thread names will be siphoned off to a
    separate thread DB file instead of being saved in the XG.
    
    If use_thread_dbs is not None, it must be a list of file IDs. All the
    thread DBs in the list will be considered when creating the xg index. Their
    haplotype names will be incorporated, and the maximum haplotype count in
    any of them will be used as the XG index's expected haplotype count per
    chromosome. It cannot be specified along with make_gbwt.
    
    if make_gbwt is specified *and* a phasing VCF is specified, the GBWT will
    be generated. Otherwise it won't be (for example, for single-contig graphs
    where no VCF is available).
    
    Return a tuple of file IDs, (xg_id, gbwt_id, thread_db_id). The GBWT ID
    will be None if no GBWT is generated. The thread DB ID will be None if no
    thread DB is generated.
    
    If intermediate is set to true, do not save the produced files to the
    output store.
    """
    RealtimeLogger.info('Starting xg indexing...')
    start_time = timeit.default_timer()
    work_dir = job.fileStore.getLocalTempDir()
    index_temp_dir = os.path.join(work_dir, 'index-temp')
    os.makedirs(index_temp_dir)
    RealtimeLogger.info(('inputGraphFileIDs: {}').format(str(inputGraphFileIDs)))
    RealtimeLogger.info(('graph_names: {}').format(str(graph_names)))
    RealtimeLogger.info(('separate_threads: {}').format(str(separate_threads)))
    RealtimeLogger.info(('use_thread_dbs: {}').format(str(use_thread_dbs)))
    graph_filenames = []
    for i, graph_id in enumerate(inputGraphFileIDs):
        graph_filename = os.path.join(work_dir, graph_names[i])
        job.fileStore.readGlobalFile(graph_id, graph_filename)
        graph_filenames.append(os.path.basename(graph_filename))

    gbwt_filename = os.path.join(work_dir, ('{}.gbwt').format(index_name))
    thread_db_filename = os.path.join(work_dir, ('{}.threads').format(index_name))
    if vcf_phasing_file_id:
        phasing_file = os.path.join(work_dir, 'phasing.vcf.gz')
        job.fileStore.readGlobalFile(vcf_phasing_file_id, phasing_file)
        job.fileStore.readGlobalFile(tbi_phasing_file_id, phasing_file + '.tbi')
        phasing_opts = ['-v', os.path.basename(phasing_file)]
        if make_gbwt:
            phasing_opts += ['--gbwt-name', os.path.basename(gbwt_filename)]
            if separate_threads:
                RealtimeLogger.info('Making XG with separate thread database')
                phasing_opts += ['--thread-db', os.path.basename(thread_db_filename)]
            else:
                RealtimeLogger.info('Making XG with integrated thread database')
            for region in gbwt_regions:
                phasing_opts += ['--region', region]

    else:
        phasing_opts = []
    if use_thread_dbs is not None:
        assert not make_gbwt
        for i, file_id in enumerate(use_thread_dbs):
            assert file_id is not None
            file_name = os.path.join(work_dir, ('threads{}.threads').format(i))
            job.fileStore.readGlobalFile(file_id, file_name)
            phasing_opts += ['--thread-db', os.path.basename(file_name)]

    xg_filename = ('{}.xg').format(index_name)
    RealtimeLogger.info(('XG Indexing {}').format(str(graph_filenames)))
    command = [
     'vg', 'index', '--threads', str(job.cores), '--xg-name', os.path.basename(xg_filename)]
    command += phasing_opts + graph_filenames
    command += ['--temp-dir', os.path.join('.', os.path.basename(index_temp_dir))]
    try:
        context.runner.call(job, command, work_dir=work_dir)
    except:
        logging.error('XG indexing failed. Dumping files.')
        for graph_filename in graph_filenames:
            context.write_output_file(job, os.path.join(work_dir, graph_filename))

        if vcf_phasing_file_id:
            context.write_output_file(job, phasing_file)
            context.write_output_file(job, phasing_file + '.tbi')
        if use_thread_dbs is not None:
            for i, file_id in enumerate(use_thread_dbs):
                file_name = os.path.join(work_dir, ('threads{}.threads').format(i))
                context.write_output_file(job, file_name)

        raise

    write_function = context.write_intermediate_file if intermediate else context.write_output_file
    xg_file_id = write_function(job, os.path.join(work_dir, xg_filename))
    gbwt_file_id = None
    thread_db_file_id = None
    if make_gbwt and vcf_phasing_file_id:
        gbwt_file_id = write_function(job, gbwt_filename)
        if separate_threads:
            thread_db_file_id = write_function(job, thread_db_filename)
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info(('Finished XG index. Process took {} seconds.').format(run_time))
    return (
     xg_file_id, gbwt_file_id, thread_db_file_id)


def run_cat_xg_indexing(job, context, inputGraphFileIDs, graph_names, index_name, vcf_phasing_file_id=None, tbi_phasing_file_id=None, make_gbwt=False, gbwt_regions=[], separate_threads=False, use_thread_dbs=None, intermediate=False, intermediate_cat=True):
    """
    Encapsulates run_concat_graphs and run_xg_indexing job functions.
    Can be used for ease of programming in job functions that require running only
    during runs of the run_xg_indexing job function.

    Note: the resources assigned to indexing come from those assigned to this parent job
    (as they can get toggled between xg and gbwt modes in the caller)
    
    If intermediate is set to True, do not save the final .xg to the output store.
    
    If intermediate_cat is False and intermediate is also False, save the .cat.vg to the output store.
    """
    child_job = Job()
    job.addChild(child_job)
    vg_concat_job = child_job.addChildJobFn(run_concat_graphs, context, inputGraphFileIDs, graph_names, index_name, intermediate=intermediate or intermediate_cat)
    return child_job.addFollowOnJobFn(run_xg_indexing, context, [vg_concat_job.rv(0)], [
     vg_concat_job.rv(1)], index_name, vcf_phasing_file_id, tbi_phasing_file_id, make_gbwt=make_gbwt, gbwt_regions=gbwt_regions, separate_threads=separate_threads, use_thread_dbs=use_thread_dbs, intermediate=intermediate, cores=job.cores, memory=job.memory, disk=job.disk, preemptable=job.preemptable).rv()


def run_concat_files(job, context, file_ids, name=None):
    """
    Utility job to concatenate some files. Returns the concatenated file ID.
    If given a name, writes the result to the out store with the given name.
    """
    work_dir = job.fileStore.getLocalTempDir()
    file_names = [ job.fileStore.readGlobalFile(file_id) for file_id in file_ids ]
    out_name = os.path.join(work_dir, 'output.dat')
    with open(out_name, 'w') as (out_file):
        for file_name in file_names:
            with open(file_name) as (in_file):
                shutil.copyfileobj(in_file, out_file)

    if name is None:
        return context.write_intermediate_file(job, out_name)
    else:
        return context.write_output_file(job, out_name, name)
        return


def run_snarl_indexing(job, context, inputGraphFileIDs, graph_names, index_name=None):
    """
    Compute the snarls of the graph.
    
    Saves the snarls file in the outstore as <index_name>.snarls, unless index_name is None.
    
    Removes trivial snarls, which are not really useful and which snarl cutting
    in mpmap can go overboard with.
    
    Return the file ID of the snarls file.
    """
    assert len(inputGraphFileIDs) == len(graph_names)
    if len(inputGraphFileIDs) > 1:
        RealtimeLogger.info(('Breaking up snarl computation for {}').format(str(graph_names)))
        snarl_jobs = []
        for file_id, file_name in itertools.izip(inputGraphFileIDs, graph_names):
            snarl_jobs.append(job.addChildJobFn(run_snarl_indexing, context, [file_id], [file_name], cores=context.config.snarl_index_cores, memory=context.config.snarl_index_mem, disk=context.config.snarl_index_disk))

        concat_job = snarl_jobs[0].addFollowOnJobFn(run_concat_files, context, [ job.rv() for job in snarl_jobs ], index_name + '.snarls' if index_name is not None else None, cores=context.config.snarl_index_cores, memory=context.config.snarl_index_mem, disk=context.config.snarl_index_disk)
        for i in xrange(1, len(snarl_jobs)):
            snarl_jobs[i].addFollowOn(concat_job)

        return concat_job.rv()
    else:
        RealtimeLogger.info('Starting snarl computation...')
        start_time = timeit.default_timer()
        work_dir = job.fileStore.getLocalTempDir()
        graph_id = inputGraphFileIDs[0]
        graph_filename = graph_names[0]
        job.fileStore.readGlobalFile(graph_id, os.path.join(work_dir, graph_filename))
        snarl_filename = os.path.join(work_dir, ('{}.snarls').format(index_name if index_name is not None else 'part'))
        RealtimeLogger.info(('Computing snarls for {}').format(graph_filename))
        cmd = [
         'vg', 'snarls', graph_filename]
        with open(snarl_filename, 'w') as (snarl_file):
            try:
                context.runner.call(job, cmd, work_dir=work_dir, outfile=snarl_file)
            except:
                logging.error('Snarl indexing failed. Dumping files.')
                context.write_output_file(job, os.path.join(work_dir, graph_filename))
                raise

        if index_name is not None:
            snarl_file_id = context.write_output_file(job, snarl_filename)
        else:
            snarl_file_id = context.write_intermediate_file(job, snarl_filename)
        end_time = timeit.default_timer()
        run_time = end_time - start_time
        RealtimeLogger.info(('Finished computing snarls. Process took {} seconds.').format(run_time))
        return snarl_file_id
        return


def run_id_ranges(job, context, inputGraphFileIDs, graph_names, index_name, chroms):
    """ Make a file of chrom_name <tab> first_id <tab> last_id covering the 
    id ranges of all chromosomes.  This is to speed up gam splitting down the road. 
    """
    RealtimeLogger.info('Starting id ranges...')
    start_time = timeit.default_timer()
    id_ranges = []
    child_job = Job()
    job.addChild(child_job)
    for graph_id, graph_name, chrom in zip(inputGraphFileIDs, graph_names, chroms):
        id_range = child_job.addChildJobFn(run_id_range, context, graph_id, graph_name, chrom, cores=context.config.prune_cores, memory=context.config.prune_mem, disk=context.config.prune_disk).rv()
        id_ranges.append(id_range)

    return child_job.addFollowOnJobFn(run_merge_id_ranges, context, id_ranges, index_name, cores=context.config.misc_cores, memory=context.config.misc_mem, disk=context.config.misc_disk).rv()
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info(('Finished id ranges. Process took {} seconds.').format(run_time))


def run_id_range(job, context, graph_id, graph_name, chrom):
    """
    Compute a node id range for a graph (which should be an entire contig/chromosome with
    contiguous id space -- see vg ids) using vg stats
    """
    work_dir = job.fileStore.getLocalTempDir()
    graph_filename = os.path.join(work_dir, graph_name)
    job.fileStore.readGlobalFile(graph_id, graph_filename)
    command = [
     'vg', 'stats', '--node-id-range', os.path.basename(graph_filename)]
    stats_out = context.runner.call(job, command, work_dir=work_dir, check_output=True).strip().split()
    assert stats_out[0] == 'node-id-range'
    first, last = stats_out[1].split(':')
    return (
     chrom, first, last)


def run_merge_id_ranges(job, context, id_ranges, index_name):
    """ create a BED-style file of id ranges
    """
    work_dir = job.fileStore.getLocalTempDir()
    id_range_filename = os.path.join(work_dir, ('{}_id_ranges.tsv').format(index_name))
    with open(id_range_filename, 'w') as (f):
        for id_range in id_ranges:
            f.write(('{}\t{}\t{}\n').format(*id_range))

    return context.write_output_file(job, id_range_filename)


def run_merge_gbwts(job, context, chrom_gbwt_ids, index_name):
    """ merge up some gbwts
    """
    work_dir = job.fileStore.getLocalTempDir()
    gbwt_chrom_filenames = []
    for i, gbwt_id in enumerate(chrom_gbwt_ids):
        if gbwt_id:
            gbwt_filename = os.path.join(work_dir, ('{}.gbwt').format(i))
            job.fileStore.readGlobalFile(gbwt_id, gbwt_filename)
            gbwt_chrom_filenames.append(gbwt_filename)

    if len(gbwt_chrom_filenames) == 0:
        return
    else:
        if len(gbwt_chrom_filenames) == 1:
            return context.write_output_file(job, gbwt_chrom_filenames[0], out_store_path=index_name + '.gbwt')
        else:
            cmd = [
             'vg', 'gbwt', '--merge', '--fast', '--output', index_name + '.gbwt']
            cmd += [ os.path.basename(f) for f in gbwt_chrom_filenames ]
            try:
                context.runner.call(job, cmd, work_dir=work_dir)
            except:
                logging.error('GBWT merge failed. Dumping files.')
                for f in gbwt_chrom_filenames:
                    context.write_output_file(job, f)

                raise

            return context.write_output_file(job, os.path.join(work_dir, index_name + '.gbwt'))

        return


def run_bwa_index(job, context, fasta_file_id, bwa_index_ids=None, intermediate=False, copy_fasta=False):
    """
    Make a bwa index for a fast sequence if not given in input.
    
    If intermediate is set to True, do not output them. Otherwise, output them
    as bwa.fa.<index type>.
    
    Returns a dict from index extension to index file ID.
    
    Note that BWA produces 'amb', 'ann',  'bwt', 'pac', and 'sa' index files.
    
    If such a nonempty dict is passed in already, return that instead (and
    don't output any files).
    
    If copy_fasta is True (and intermediate is False), also output the input FASTA to the out store.
    
    """
    if not bwa_index_ids:
        bwa_index_ids = dict()
        work_dir = job.fileStore.getLocalTempDir()
        fasta_file = os.path.join(work_dir, 'bwa.fa')
        job.fileStore.readGlobalFile(fasta_file_id, fasta_file)
        cmd = ['bwa', 'index', os.path.basename(fasta_file)]
        context.runner.call(job, cmd, work_dir=work_dir)
        write_file = context.write_intermediate_file if intermediate else context.write_output_file
        for idx_file in glob.glob(('{}.*').format(fasta_file)):
            bwa_index_ids[idx_file[len(fasta_file):]] = write_file(job, idx_file)

        if copy_fasta and not intermediate:
            context.write_output_file(job, fasta_file)
    return bwa_index_ids


def run_indexing(job, context, inputGraphFileIDs, graph_names, index_name, chroms, vcf_phasing_file_ids=[], tbi_phasing_file_ids=[], bwa_fasta_id=None, gbwt_id=None, node_mapping_id=None, skip_xg=False, skip_gcsa=False, skip_id_ranges=False, skip_snarls=False, make_gbwt=False, gbwt_prune=False, gbwt_regions=[]):
    """
    
    Run indexing logic by itself.
    
    vcf_phasing_file_ids and tbi_phasing_file_ids are phasing data VCFs. There
    can be 0 of them, 1 for all chromosomes, or one for each chromosome in
    chroms order.
    
    gbwt_regions is a list of chrom:start-end regions pecifiers to restrict, on
    those chromosomes, the regions examined in the VCF by the GBWT indexing.
    
    Return a dict from index type ('xg','chrom_xg', 'gcsa', 'lcp', 'gbwt',
    'chrom_gbwt', 'chrom_thread', 'id_ranges', 'snarls', 'bwa') to index file
    ID(s) if created.
    
    For 'chrom_xg' and 'chrom_gbwt' the value is a list of one XG or GBWT or
    thread DB per chromosome in chroms, to support `vg prune`. For
    'chrom_thread', we have a value per chromosome that actually has any
    threads (instead of padding out with Nones). For 'bwa', the result is
    itself a dict from BWA index extension to file ID. The others are all
    single file IDs.
    
    If gbwt_id is specified, and the gbwt index is not built, the passed ID is
    re-used.
    
    """
    child_job = Job()
    job.addChild(child_job)
    chrom_xg_root_job = Job()
    child_job.addChild(chrom_xg_root_job)
    xg_root_job = Job()
    chrom_xg_root_job.addFollowOn(xg_root_job)
    RealtimeLogger.debug(('Running indexing: {}.').format({'graph_names': graph_names, 
       'index_name': index_name, 
       'chroms': chroms, 
       'vcf_phasing_file_ids': vcf_phasing_file_ids, 
       'tbi_phasing_file_ids': tbi_phasing_file_ids, 
       'gbwt_id': gbwt_id, 
       'node_mapping_id': node_mapping_id, 
       'skip_xg': skip_xg, 
       'skip_gcsa': skip_gcsa, 
       'skip_id_ranges': skip_id_ranges, 
       'skip_snarls': skip_snarls, 
       'make_gbwt': make_gbwt, 
       'gbwt_prune': gbwt_prune, 
       'bwa_fasta_id': bwa_fasta_id}))
    indexes = {}
    if gbwt_id:
        indexes['gbwt'] = gbwt_id
    if not (len(vcf_phasing_file_ids) == 0 or make_gbwt):
        raise AssertionError
        if not skip_xg or not skip_gcsa:
            indexes['chrom_xg'] = []
            indexes['chrom_gbwt'] = []
            if make_gbwt:
                if not chroms or len(chroms) == 1:
                    chroms = [
                     index_name]
                indexes['chrom_xg'] = []
                indexes['chrom_gbwt'] = []
                separate_threads = len(chroms) > 1 and vcf_phasing_file_ids and make_gbwt
                if separate_threads:
                    indexes['chrom_thread'] = []
                if len(vcf_phasing_file_ids) != len(tbi_phasing_file_ids):
                    raise RuntimeError(('Found {} phasing VCFs and {} indexes; counts must match!').format(len(vcf_phasing_file_ids), len(tbi_phasing_file_ids)))
                if len(vcf_phasing_file_ids) > len(chroms):
                    RealtimeLogger.error(('Chromosomes: {}').format(chroms))
                    RealtimeLogger.error(('VCFs: {}').format(vcf_phasing_file_ids))
                    raise RuntimeError(('Found too many ({}) phasing VCFs for {} chromosomes').format(len(vcf_phasing_file_ids), len(chroms)))
                for i, chrom in enumerate(chroms):
                    if len(vcf_phasing_file_ids) == 0:
                        vcf_id = None
                        tbi_id = None
                    elif len(vcf_phasing_file_ids) == 1:
                        vcf_id = vcf_phasing_file_ids[0]
                        tbi_id = tbi_phasing_file_ids[0]
                    elif i < len(vcf_phasing_file_ids):
                        vcf_id = vcf_phasing_file_ids[i]
                        tbi_id = tbi_phasing_file_ids[i]
                    else:
                        vcf_id = None
                        tbi_id = None
                    xg_chrom_index_job = chrom_xg_root_job.addChildJobFn(run_cat_xg_indexing, context, [inputGraphFileIDs[i]], [
                     graph_names[i]], chrom, vcf_id, tbi_id, make_gbwt=make_gbwt, separate_threads=separate_threads, gbwt_regions=gbwt_regions, intermediate=len(chroms) > 1, cores=context.config.gbwt_index_cores, memory=context.config.gbwt_index_mem, disk=context.config.gbwt_index_disk, preemptable=not make_gbwt or context.config.gbwt_index_preemptable)
                    indexes['chrom_xg'].append(xg_chrom_index_job.rv(0))
                    indexes['chrom_gbwt'].append(xg_chrom_index_job.rv(1))
                    if separate_threads and vcf_id is not None:
                        indexes['chrom_thread'].append(xg_chrom_index_job.rv(2))

                if len(chroms) > 1 and vcf_phasing_file_ids and make_gbwt:
                    indexes['gbwt'] = xg_root_job.addChildJobFn(run_merge_gbwts, context, indexes['chrom_gbwt'], index_name, cores=context.config.xg_index_cores, memory=context.config.xg_index_mem, disk=context.config.xg_index_disk).rv()
            if indexes.has_key('chrom_xg') and len(indexes['chrom_xg']) == 1:
                indexes['xg'] = indexes['chrom_xg'][0]
            elif not skip_xg:
                xg_index_job = xg_root_job.addChildJobFn(run_cat_xg_indexing, context, inputGraphFileIDs, graph_names, index_name, None, None, make_gbwt=False, use_thread_dbs=indexes.get('chrom_thread'), cores=context.config.xg_index_cores, memory=context.config.xg_index_mem, disk=context.config.xg_index_disk)
                indexes['xg'] = xg_index_job.rv(0)
        gcsa_root_job = Job()
        gcsa_predecessor_job = chrom_xg_root_job if gbwt_prune else child_job
        gcsa_predecessor_job.addFollowOn(gcsa_root_job)
        if not skip_gcsa:
            if not indexes.has_key('chrom_gbwt') and indexes.has_key('gbwt'):
                indexes['chrom_gbwt'] = indexes['gbwt'] * len(inputGraphFileIDs)
            gcsa_job = gcsa_root_job.addChildJobFn(run_gcsa_prep, context, inputGraphFileIDs, graph_names, index_name, chroms, indexes['chrom_gbwt'] if gbwt_prune else [], node_mapping_id, cores=context.config.misc_cores, memory=context.config.misc_mem, disk=context.config.misc_disk)
            indexes['gcsa'] = gcsa_job.rv(0)
            indexes['lcp'] = gcsa_job.rv(1)
        if len(inputGraphFileIDs) > 1 and not skip_id_ranges:
            indexes['id_ranges'] = job.addChildJobFn(run_id_ranges, context, inputGraphFileIDs, graph_names, index_name, chroms, cores=context.config.misc_cores, memory=context.config.misc_mem, disk=context.config.misc_disk).rv()
        indexes['snarls'] = skip_snarls or job.addChildJobFn(run_snarl_indexing, context, inputGraphFileIDs, graph_names, index_name, cores=context.config.snarl_index_cores, memory=context.config.snarl_index_mem, disk=context.config.snarl_index_disk).rv()
    if bwa_fasta_id:
        indexes['bwa'] = job.addChildJobFn(run_bwa_index, context, bwa_fasta_id, cores=context.config.bwa_index_cores, memory=context.config.bwa_index_mem, disk=context.config.bwa_index_disk).rv()
    return indexes


def index_main(context, options):
    """
    Wrapper for vg indexing. 
    """
    validate_index_options(options)
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            start_time = timeit.default_timer()
            inputGraphFileIDs = []
            for graph in options.graphs:
                inputGraphFileIDs.append(toil.importFile(graph))

            inputPhasingVCFFileIDs = []
            inputPhasingTBIFileIDs = []
            for vcf in options.vcf_phasing:
                inputPhasingVCFFileIDs.append(toil.importFile(vcf))
                inputPhasingTBIFileIDs.append(toil.importFile(vcf + '.tbi'))

            if len(inputPhasingTBIFileIDs) == 1 and len(options.graphs) > 1:
                inputPhasingVCFFileIDs = [
                 inputPhasingVCFFileIDs[0]] * len(options.graphs)
                inputPhasingTBIFileIDs = [inputPhasingTBIFileIDs[0]] * len(options.graphs)
            inputGBWTID = None
            if options.gbwt_input:
                inputGBWTID = toil.importFile(options.gbwt_input)
            inputNodeMappingID = None
            if options.node_mapping:
                inputNodeMappingID = toil.importFile(options.node_mapping)
            inputBWAFastaID = None
            if options.bwa_index_fasta:
                inputBWAFastaID = toil.importFile(options.bwa_index_fasta)
            graph_names = [ os.path.basename(i) for i in options.graphs ]
            end_time = timeit.default_timer()
            logger.info(('Imported input files into Toil in {} seconds').format(end_time - start_time))
            root_job = Job.wrapJobFn(run_indexing, context, inputGraphFileIDs, graph_names, options.index_name, options.chroms, vcf_phasing_file_ids=inputPhasingVCFFileIDs, tbi_phasing_file_ids=inputPhasingTBIFileIDs, gbwt_id=inputGBWTID, node_mapping_id=inputNodeMappingID, bwa_fasta_id=inputBWAFastaID, skip_xg=not options.xg_index and not options.all_index, skip_gcsa=not options.gcsa_index and not options.all_index, skip_id_ranges=not options.id_ranges_index and not options.all_index, skip_snarls=not options.snarls_index and not options.all_index, make_gbwt=options.gbwt_index, gbwt_prune=options.gbwt_prune, gbwt_regions=options.vcf_phasing_regions, cores=context.config.misc_cores, memory=context.config.misc_mem, disk=context.config.misc_disk)
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, sys.argv)
            init_job.addFollowOn(root_job)
            index_key_and_id = toil.start(init_job)
        else:
            index_key_and_id = toil.restart()
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
    print(('All jobs completed successfully. Pipeline took {} seconds.').format(run_time_pipeline))
    return