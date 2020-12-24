# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_toil.py
# Compiled at: 2020-04-30 13:47:21
# Size of source mod 2**32: 25345 bytes
"""
vg_toil.py: Run the mapping and variant calling on all the servers in
parallel using the vg framework.

old docker vg tool=1.4.0--4cbd3aa6d2c0449730975517fc542775f74910f3
new docker vg tool=latest

chr_length_list obtained from Mike Lin's vg dnanexus pipeline configuration
    chr_label_list = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X","Y"]
    chr_length_list = [249250621,243199373,198022430,191154276,180915260,171115067,159138663,146364022,141213431,135534747,135006516,133851895,115169878,107349540,102531392,90354753,81195210,78077248,59128983,63025520,48129895,51304566,155270560,59373566]
"""
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, struct, socket, threading, string, getpass, logging, pkg_resources
from math import ceil
from subprocess import Popen, PIPE
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
try:
    from version import version
except:
    version = None

from toil_vg.vg_common import *
from toil_vg.vg_call import *
from toil_vg.vg_index import *
from toil_vg.vg_map import *
from toil_vg.vg_vcfeval import *
from toil_vg.vg_config import *
from toil_vg.vg_sim import *
from toil_vg.vg_mapeval import *
from toil_vg.vg_calleval import *
from toil_vg.vg_plot import plot_subparser, plot_main
from toil_vg.context import Context, run_write_info_to_outstore
from toil_vg.vg_construct import *
from toil_vg.vg_surject import *
from toil_vg.vg_msga import *
from toil_vg.vg_chunk import *
from toil_vg.vg_augment import *
logger = logging.getLogger(__name__)

def parse_args(args=None):
    """
    Takes in the command-line arguments list (args), and returns a nice argparse
    result with fields for all the options.
    
    Borrows heavily from the argparse documentation examples:
    <http://docs.python.org/library/argparse.html>
    """
    parser = argparse.ArgumentParser(prog='toil-vg', description=(main.__doc__), formatter_class=(argparse.RawDescriptionHelpFormatter))
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    parser_config = subparsers.add_parser('generate-config', help='Prints default config file')
    config_subparser(parser_config)
    parser_run = subparsers.add_parser('run', help='Runs the Toil VG DNA-seq pipeline')
    pipeline_subparser(parser_run)
    parser_index = subparsers.add_parser('index', help='Runs only the vg indexing')
    index_subparser(parser_index)
    parser_map = subparsers.add_parser('map', help='Runs only the vg mapping')
    map_subparser(parser_map)
    parser_call = subparsers.add_parser('call', help='Runs only the vg calling')
    call_subparser(parser_call)
    parser_vcfeval = subparsers.add_parser('vcfeval', help='Compare two VCFs wit rtg vcfeval')
    vcfeval_subparser(parser_vcfeval)
    parser_sim = subparsers.add_parser('sim', help='Simulate reads and alignments')
    sim_subparser(parser_sim)
    parser_mapeval = subparsers.add_parser('mapeval', help='Compare mapping results')
    mapeval_subparser(parser_mapeval)
    parser_calleval = subparsers.add_parser('calleval', help='Compare calling results')
    calleval_subparser(parser_calleval)
    parser_construct = subparsers.add_parser('construct', help='Construct graphs from VCF')
    construct_subparser(parser_construct)
    parser_surject = subparsers.add_parser('surject', help='Surject GAM to BAM')
    surject_subparser(parser_surject)
    parser_plot = subparsers.add_parser('plot', help='Plot the results of mapping and calling experiments')
    plot_subparser(parser_plot)
    parser_msga = subparsers.add_parser('msga', help='Align fasta sequences to a graph')
    msga_subparser(parser_msga)
    parser_chunk = subparsers.add_parser('chunk', help='Split a graph into components')
    chunk_subparser(parser_chunk)
    parser_augment = subparsers.add_parser('augment', help='Augment a graph with variation from a GAM')
    augment_subparser(parser_augment)
    parser_version = subparsers.add_parser('version', help='Print version')
    return parser.parse_args(args)


def pipeline_subparser(parser_run):
    Job.Runner.addToilOptions(parser_run)
    parser_run.add_argument('sample_name', type=str, help='sample name (ex NA12878)')
    parser_run.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    parser_run.add_argument('--graphs', nargs='+', type=make_url, help='input graph(s). one per chromosome (separated by space)')
    parser_run.add_argument('--chroms', nargs='+', help='Name(s) of reference path in graph(s) (separated by space).  If --graphs  has multiple elements, must be same length/order as --chroms')
    add_common_vg_parse_args(parser_run)
    index_parse_args(parser_run)
    map_parse_args(parser_run)
    map_parse_index_args(parser_run)
    chunk_parse_args(parser_run, path_components=False)
    augment_parse_args(parser_run)
    call_parse_args(parser_run)
    vcfeval_parse_args(parser_run)
    add_container_tool_parse_args(parser_run)


def validate_pipeline_options(options):
    """
    Throw an error if an invalid combination of options has been selected.
    """
    if options.graphs:
        require(len(options.chroms) == len(options.graphs), '--chroms and --graphs must have same number of arguments')
    if not options.xg_index or not options.gcsa_index or not options.id_ranges:
        require(options.graphs and options.chroms, '--chroms and --graphs must be specified unless --xg_index --gcsa_index and --id_ranges used')
    require(options.fastq is None or len(options.fastq) in (1, 2), 'Exacty 1 or 2 files must be passed with --fastq')
    require(options.interleaved == False or options.fastq is None or len(options.fastq) == 1, '--interleaved cannot be used when > 1 fastq given')
    require(sum([1 if x else 0 for x in [options.fastq, options.gam_input_reads, options.bam_input_reads]]) == 1, 'reads must be speficied with either --fastq or --gam_input_reads or --bam_input_reads')
    require(options.mapper != 'gaffe', 'gaffe mapper is not yet supported by toil-vg run')


def run_pipeline_index(job, context, options, inputGraphFileIDs, inputReadsFileIDs, inputXGFileID, inputGCSAFileID, inputLCPFileID, inputGBWTFileID, inputIDRangesFileID, inputVCFFileID, inputTBIFileID, inputFastaFileID, inputBeDFileID, inputPhasingVCFFileIDs, inputPhasingTBIFileIDs):
    """
    All indexing.  result is a tarball in thie output store.  Will also do the fastq
    splitting, which doesn't depend on indexing. 
    """
    wanted = set()
    if inputXGFileID is None:
        wanted.add('xg')
    else:
        if inputGCSAFileID is None:
            wanted.add('gcsa')
        else:
            graph_names = list(map(os.path.basename, options.graphs))
            vcf_ids = [] if not inputVCFFileID else [inputVCFFileID]
            tbi_ids = [] if not inputTBIFileID else [inputTBIFileID]
            index_job = job.addChildJobFn(run_indexing, context, inputGraphFileIDs, graph_names,
              (options.index_name), (options.chroms), vcf_phasing_file_ids=inputPhasingVCFFileIDs,
              tbi_phasing_file_ids=inputPhasingTBIFileIDs,
              wanted=wanted,
              cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            input_indexes = {}
            if inputXGFileID is not None:
                input_indexes['xg'] = inputXGFileID
            if inputGCSAFileID is not None:
                input_indexes['gcsa'] = inputGCSAFileID
                input_indexes['lcp'] = inputLCPFileID
            if inputGBWTFileID is not None:
                input_indexes['gbwt'] = inputGBWTFileID
            if inputIDRangesFileID is not None:
                input_indexes['id_ranges'] = inputIDRangesFileID
        index_merge_job = index_job.addFollowOnJobFn(merge_dicts, (index_job.rv()), input_indexes, cores=(context.config.misc_cores),
          memory=(context.config.misc_mem),
          disk=(context.config.misc_disk))
        if not options.single_reads_chunk:
            fastq_chunk_ids = job.addChildJobFn(run_split_reads, context, (options.fastq), (options.gam_input_reads),
              (options.bam_input_reads), inputReadsFileIDs, cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.misc_disk)).rv()
        else:
            RealtimeLogger.info('Bypassing reads splitting because --single_reads_chunk enabled')
        fastq_chunk_ids = [
         inputReadsFileIDs]
    return job.addFollowOnJobFn(run_pipeline_map, context, options, (index_merge_job.rv()), fastq_chunk_ids, inputVCFFileID,
      inputTBIFileID, inputFastaFileID, inputBeDFileID, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk)).rv()


def merge_dicts(job, dict1, dict2):
    """
    Merge two dicts together as a Toil job.
    """
    dict1.update(dict2)
    return dict1


def run_pipeline_map(job, context, options, indexes, fastq_chunk_ids, baseline_vcf_id, baseline_tbi_id, fasta_id, bed_id):
    """ All mapping, then gam merging.  fastq is split in above step"""
    chr_gam_ids = job.addChildJobFn(run_whole_alignment, context, (options.fastq),
      (options.gam_input_reads), (options.bam_input_reads), (options.sample_name),
      (options.interleaved), (options.mapper), indexes,
      fastq_chunk_ids, bam_output=(options.bam_output),
      surject=(options.surject),
      cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk)).rv(0)
    return job.addFollowOnJobFn(run_pipeline_call, context, options, (indexes['xg']), (indexes.get('id_ranges')), chr_gam_ids,
      baseline_vcf_id, baseline_tbi_id, fasta_id,
      bed_id, cores=(context.config.misc_cores), memory=(context.config.misc_mem), disk=(context.config.misc_disk)).rv()


def run_pipeline_call(job, context, options, xg_file_id, id_ranges_file_id, chr_gam_ids, baseline_vcf_id, baseline_tbi_id, fasta_id, bed_id):
    """ Run variant calling on the chromosomes in parallel """
    if id_ranges_file_id:
        chroms = [x[0] for x in parse_id_ranges(job, id_ranges_file_id)]
    else:
        chroms = options.chroms
    if options.vcf_offsets:
        vcf_offset_dict = {}
        for ref_path_name, vcf_offset in zip(options.chroms, options.vcf_offsets):
            vcf_offset_dict[ref_path_name] = vcf_offset

        options.vcf_offsets = vcf_offset_dict
    else:
        if not len(chr_gam_ids) == 1:
            raise AssertionError
        else:
            if context.config.filter_opts:
                filter_job = Job.wrapJobFn(run_filtering, context, graph_id=xg_file_id,
                  graph_basename='graph.xg',
                  gam_id=(chr_gam_ids[0]),
                  gam_basename='reasd1.gam',
                  filter_opts=(context.config.filter_opts),
                  cores=(context.config.calling_cores),
                  memory=(context.config.calling_mem),
                  disk=(context.config.calling_disk))
                gam_id = filter_job.rv()
            else:
                gam_id = chr_gam_ids[0]
                filter_job = None
        call_job = Job.wrapJobFn(run_chunked_calling, context, graph_id=xg_file_id,
          graph_basename='graph.xg',
          gam_id=gam_id,
          gam_basename='reads1.gam',
          batch_input=None,
          genotype_vcf_id=None,
          genotype_tbi_id=None,
          sample=(options.sample_name),
          augment=(not options.recall),
          output_format=(options.output_format),
          min_augment_coverage=(options.min_augment_coverage),
          expected_coverage=(options.expected_coverage),
          min_mapq=(options.min_mapq),
          min_baseq=(options.min_baseq),
          ref_paths=chroms,
          ref_path_chunking=(options.ref_path_chunking),
          min_call_support=(options.min_call_support),
          vcf_offsets=(options.vcf_offsets))
        if filter_job:
            job.addChild(filter_job)
            filter_job.addFollowOn(call_job)
        else:
            job.addChild(call_job)
    vcf_tbi_wg_id_pair = (
     call_job.rv(0), call_job.rv(1))
    if baseline_vcf_id is not None:
        return job.addFollowOnJobFn(run_vcfeval, context, (options.sample_name), vcf_tbi_wg_id_pair,
          baseline_vcf_id, baseline_tbi_id, (options.vcfeval_fasta),
          fasta_id, bed_id, cores=(options.vcfeval_cores),
          memory=(options.vcfeval_mem),
          disk=(options.vcfeval_disk)).rv()


def main():
    r"""
    Computational Genomics Lab, Genomics Institute, UC Santa Cruz
    Toil vg DNA-seq pipeline
    
    DNA-seq fastqs are split, aligned to an indexed vg reference graph, and variant-called using
    the vg toolset.
    
    General usage:
    1. Type "toil-vg generate-config": Produce an editable config file in the current working directory.
    2. Type "toil-vg run": Given input graphs (one per chromosome) and reads (fastq file), produce a graph index (index can also be input), graph alignment (GAM), VCF variant calls, and (optionally) VCF comparison results.
    3. Type "toil-vg index": Produce an index from input graph(s).
    4. Type "toil-vg map": Produce graph alignment (gam) for each chromosome from input reads and index
    5. Type "toil-vg call": Produce VCF from input index and chromosome gam(s)

    Please read the README.md located in the source directory for more documentation

    Structure of vg DNA-Seq Pipeline (per sample)
                  
                  
                       > 3 ---->    > 5 ---->
                      / ..      |  / ..     |
                     /  ..      v /  ..     v
        0 --> 1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7
                     \  ..      ^ \  ..     ^
                      \ ..      |  \ ..     | 
                       > 3 ---->    > 5 --->

    0 = Upload local input files to remote input fileStore
    1 = Index input vg reference graph
    2 = Shard Reads
    3 = Align reads to reference graph
    4 = Merge read alignments
    5 = Run vg variant calls on chromosome-chunked .gam alignment
    6 = Merge variant call files
    7 = Download output files from remote output fileStore to local output directory
    ================================================================================
    """
    args = parse_args(sys.argv[1:])
    if args.command == 'generate-config':
        config_main(args)
        return
    elif args.command == 'version':
        try:
            print(pkg_resources.get_distribution('toil-vg').version)
        except:
            print('Version gathered from toil-vg.version: ' + version)

        return
    else:
        context = Context(args.out_store, args)
        if args.command == 'vcfeval':
            vcfeval_main(context, args)
        else:
            if args.command == 'run':
                pipeline_main(context, context.to_options(args))
            else:
                if args.command == 'index':
                    index_main(context, args)
                else:
                    if args.command == 'map':
                        map_main(context, args)
                    else:
                        if args.command == 'call':
                            call_main(context, args)
                        else:
                            if args.command == 'sim':
                                sim_main(context, args)
                            else:
                                if args.command == 'mapeval':
                                    mapeval_main(context, args)
                                else:
                                    if args.command == 'calleval':
                                        calleval_main(context, args)
                                    else:
                                        if args.command == 'construct':
                                            construct_main(context, args)
                                        else:
                                            if args.command == 'surject':
                                                surject_main(context, args)
                                            else:
                                                if args.command == 'plot':
                                                    plot_main(context, args)
                                                else:
                                                    if args.command == 'msga':
                                                        msga_main(context, args)
                                                    else:
                                                        if args.command == 'chunk':
                                                            chunk_main(context, args)
                                                        else:
                                                            if args.command == 'augment':
                                                                augment_main(context, args)
                                                            else:
                                                                raise RuntimeError('Unimplemented subcommand {}'.format(args.command))


def pipeline_main(context, options):
    """
    toil-vg run
    """
    validate_pipeline_options(options)
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            importer = AsyncImporter(toil)
            inputGraphFileIDs = []
            if options.graphs:
                for graph in options.graphs:
                    inputGraphFileIDs.append(importer.load(graph))

            inputReadsFileIDs = []
            if options.fastq:
                for sample_reads in options.fastq:
                    inputReadsFileIDs.append(importer.load(sample_reads))

            else:
                if options.gam_input_reads:
                    inputReadsFileIDs.append(importer.load(options.gam_input_reads))
                else:
                    assert options.bam_input_reads
                    inputReadsFileIDs.append(importer.load(options.bam_input_reads))
                if options.xg_index:
                    inputXGFileID = importer.load(options.xg_index)
                else:
                    inputXGFileID = None
                if options.gcsa_index:
                    inputGCSAFileID = importer.load(options.gcsa_index)
                    inputLCPFileID = importer.load(options.gcsa_index + '.lcp')
                else:
                    inputGCSAFileID = None
                    inputLCPFileID = None
                if options.gbwt_index:
                    inputGBWTFileID = importer.load(options.gbwt_index)
                else:
                    inputGBWTFileID = None
                if options.id_ranges:
                    inputIDRangesFileID = importer.load(options.id_ranges)
                else:
                    inputIDRangesFileID = None
                if options.vcfeval_baseline is not None:
                    if not options.vcfeval_baseline.endswith('.vcf.gz'):
                        raise AssertionError
                    elif not options.vcfeval_fasta is not None:
                        raise AssertionError
                    inputVCFFileID = importer.load(options.vcfeval_baseline)
                    inputTBIFileID = importer.load((options.vcfeval_baseline + '.tbi'), wait_on=inputVCFFileID)
                    inputFastaFileID = importer.load(options.vcfeval_fasta)
                    inputBedFileID = importer.load(options.vcfeval_bed_regions) if options.vcfeval_bed_regions is not None else None
                else:
                    inputVCFFileID = None
                    inputTBIFileID = None
                    inputFastaFileID = None
                    inputBedFileID = None
            inputPhasingVCFFileIDs = []
            inputPhasingTBIFileIDs = []
            for vcf in options.vcf_phasing:
                inputPhasingVCFFileIDs.append(importer.load(vcf))
                inputPhasingTBIFileIDs.append(importer.load((vcf + '.tbi'), wait_on=(inputPhasingTBIFileIDs[(-1)])))

            importer.wait()
            root_job = Job.wrapJobFn(run_pipeline_index, context, options, (importer.resolve(inputGraphFileIDs)),
              (importer.resolve(inputReadsFileIDs)),
              (importer.resolve(inputXGFileID)),
              (importer.resolve(inputGCSAFileID)),
              (importer.resolve(inputLCPFileID)),
              (importer.resolve(inputGBWTFileID)),
              (importer.resolve(inputIDRangesFileID)),
              (importer.resolve(inputVCFFileID)),
              (importer.resolve(inputTBIFileID)),
              (importer.resolve(inputFastaFileID)),
              (importer.resolve(inputBedFileID)),
              (importer.resolve(inputPhasingVCFFileIDs)),
              (importer.resolve(inputPhasingTBIFileIDs)),
              cores=(context.config.misc_cores),
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


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print((e.message), file=(sys.stderr))
        sys.exit(1)