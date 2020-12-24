# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_calleval.py
# Compiled at: 2020-04-30 13:47:21
# Size of source mod 2**32: 50190 bytes
"""
vg_calleval.py: Compare vcfs with vcfeval.  Option to make freebayes calls to use as baseline.  Can
run on vg_mapeval.py output. 
"""
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, struct, socket, threading, string, math, getpass, pdb, gzip, logging, copy
from math import ceil
from subprocess import Popen, PIPE
try:
    import numpy as np
    from sklearn.metrics import roc_auc_score, average_precision_score, r2_score, roc_curve
    have_sklearn = True
except:
    have_sklearn = False

import tsv, vcf
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import *
from toil_vg.vg_call import call_parse_args, run_chunked_calling, run_concat_vcfs, run_filtering
from toil_vg.vg_vcfeval import vcfeval_parse_args, run_vcfeval, run_vcfeval_roc_plot, run_happy, run_sv_eval
from toil_vg.context import Context, run_write_info_to_outstore
from toil_vg.vg_construct import run_unzip_fasta, run_make_control_vcfs
from toil_vg.vg_surject import run_surjecting
from toil_vg.vg_augment import augment_parse_args
from toil_vg.vg_chunk import chunk_parse_args
logger = logging.getLogger(__name__)

def calleval_subparser(parser):
    """
    Create a subparser for calleval.  Should pass in results of subparsers.add_parser()
    """
    Job.Runner.addToilOptions(parser)
    parser.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    parser.add_argument('--gams', nargs='+', type=make_url, help='GAMs to call.  Each GAM treated as separate input (and must contain all chroms)')
    add_common_vg_parse_args(parser)
    call_parse_args(parser)
    chunk_parse_args(parser, path_components=False)
    augment_parse_args(parser)
    vcfeval_parse_args(parser)
    calleval_parse_args(parser)
    add_container_tool_parse_args(parser)


def calleval_parse_args(parser):
    """
    Add the calleval options to the given argparse parser.
    """
    parser.add_argument('--gam_names', nargs='+', help='names of vg runs (corresponds to gams and xg_paths)')
    parser.add_argument('--xg_paths', nargs='+', type=make_url, help='xg indexes for the different graphs')
    parser.add_argument('--freebayes', action='store_true', help='run freebayes as a baseline')
    parser.add_argument('--caller_fasta', type=make_url, help='Use this FASTA instead of the vcfeval fasta for Freebayes. Maybe be gzipped')
    parser.add_argument('--platypus', action='store_true', help='run platypus as a baseline')
    parser.add_argument('--bam_names', nargs='+', default=[], help='names of bwa runs (corresponds to bams)')
    parser.add_argument('--bams', nargs='+', type=make_url, default=[], help='bam inputs for freebayes')
    parser.add_argument('--clip_only', action='store_true', help='only compute accuracy clipped to --vcfeval_bed_regions')
    parser.add_argument('--plot_sets', nargs='+', default=[], help='comma-separated lists of condition-tagged BAM/GAM names (primary-mp-pe, etc.) with colon-separated title prefixes')
    parser.add_argument('--call', action='store_true', help='run vg call')
    parser.add_argument('--surject', action='store_true', help='surject GAMs to BAMs, adding the latter to the comparison')
    parser.add_argument('--interleaved', action='store_true', default=False, help='assume GAM files are interleaved when surjecting')


def validate_calleval_options--- This code section failed: ---

 L. 116         0  LOAD_FAST                'options'
                2  LOAD_ATTR                gams
                4  POP_JUMP_IF_TRUE     18  'to 18'
                6  LOAD_FAST                'options'
                8  LOAD_ATTR                gam_names
               10  POP_JUMP_IF_TRUE     18  'to 18'
               12  LOAD_FAST                'options'
               14  LOAD_ATTR                xg_paths
             16_0  COME_FROM            10  '10'
             16_1  COME_FROM             4  '4'
               16  POP_JUMP_IF_FALSE   102  'to 102'

 L. 117        18  LOAD_GLOBAL              require
               20  LOAD_FAST                'options'
               22  LOAD_ATTR                gams
               24  JUMP_IF_FALSE_OR_POP    78  'to 78'
               26  LOAD_FAST                'options'
               28  LOAD_ATTR                gam_names
               30  JUMP_IF_FALSE_OR_POP    78  'to 78'
               32  LOAD_FAST                'options'
               34  LOAD_ATTR                xg_paths
               36  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L. 118        38  LOAD_GLOBAL              len
               40  LOAD_FAST                'options'
               42  LOAD_ATTR                gam_names
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  LOAD_GLOBAL              len
               48  LOAD_FAST                'options'
               50  LOAD_ATTR                xg_paths
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  DUP_TOP          
               56  ROT_THREE        
               58  COMPARE_OP               ==
               60  JUMP_IF_FALSE_OR_POP    74  'to 74'
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'options'
               66  LOAD_ATTR                gams
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  COMPARE_OP               ==
             72_0  COME_FROM            36  '36'
             72_1  COME_FROM            30  '30'
             72_2  COME_FROM            24  '24'
               72  JUMP_FORWARD         78  'to 78'
             74_0  COME_FROM            60  '60'
               74  ROT_TWO          
               76  POP_TOP          
             78_0  COME_FROM            72  '72'

 L. 119        78  LOAD_STR                 '--gam_names, --xg_paths, --gams must all contain same number of elements'
               80  CALL_FUNCTION_2       2  '2 positional arguments'
               82  POP_TOP          

 L. 120        84  LOAD_GLOBAL              require
               86  LOAD_FAST                'options'
               88  LOAD_ATTR                call
               90  JUMP_IF_TRUE_OR_POP    96  'to 96'
               92  LOAD_FAST                'options'
               94  LOAD_ATTR                surject
             96_0  COME_FROM            90  '90'

 L. 121        96  LOAD_STR                 '--call and/or and/or --surject required with --gams'
               98  CALL_FUNCTION_2       2  '2 positional arguments'
              100  POP_TOP          
            102_0  COME_FROM            16  '16'

 L. 122       102  LOAD_FAST                'options'
              104  LOAD_ATTR                freebayes
              106  POP_JUMP_IF_TRUE    114  'to 114'
              108  LOAD_FAST                'options'
              110  LOAD_ATTR                platypus
            112_0  COME_FROM           106  '106'
              112  POP_JUMP_IF_FALSE   132  'to 132'

 L. 123       114  LOAD_GLOBAL              require
              116  LOAD_FAST                'options'
              118  LOAD_ATTR                bams
              120  JUMP_IF_TRUE_OR_POP   126  'to 126'
              122  LOAD_FAST                'options'
              124  LOAD_ATTR                surject
            126_0  COME_FROM           120  '120'
              126  LOAD_STR                 '--bams and/or --surject needed with --freebayes or --platypus'
              128  CALL_FUNCTION_2       2  '2 positional arguments'
              130  POP_TOP          
            132_0  COME_FROM           112  '112'

 L. 124       132  LOAD_FAST                'options'
              134  LOAD_ATTR                bams
              136  POP_JUMP_IF_TRUE    144  'to 144'
              138  LOAD_FAST                'options'
              140  LOAD_ATTR                bam_names
            142_0  COME_FROM           136  '136'
              142  POP_JUMP_IF_FALSE   182  'to 182'

 L. 125       144  LOAD_GLOBAL              require
              146  LOAD_FAST                'options'
              148  LOAD_ATTR                bams
              150  JUMP_IF_FALSE_OR_POP   176  'to 176'
              152  LOAD_FAST                'options'
              154  LOAD_ATTR                bam_names
              156  JUMP_IF_FALSE_OR_POP   176  'to 176'
              158  LOAD_GLOBAL              len
              160  LOAD_FAST                'options'
              162  LOAD_ATTR                bams
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'options'
              170  LOAD_ATTR                bam_names
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  COMPARE_OP               ==
            176_0  COME_FROM           156  '156'
            176_1  COME_FROM           150  '150'

 L. 126       176  LOAD_STR                 '--bams and --bam_names must be same length'
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  POP_TOP          
            182_0  COME_FROM           142  '142'

 L. 127       182  LOAD_GLOBAL              require
              184  LOAD_FAST                'options'
              186  LOAD_ATTR                vcfeval_baseline
              188  LOAD_STR                 '--vcfeval_baseline required'
              190  CALL_FUNCTION_2       2  '2 positional arguments'
              192  POP_TOP          

 L. 128       194  LOAD_GLOBAL              require
              196  LOAD_FAST                'options'
              198  LOAD_ATTR                vcfeval_fasta
              200  LOAD_STR                 '--vcfeval_fasta required'
              202  CALL_FUNCTION_2       2  '2 positional arguments'
              204  POP_TOP          

 L. 129       206  LOAD_FAST                'options'
              208  LOAD_ATTR                call
              210  POP_JUMP_IF_TRUE    218  'to 218'
              212  LOAD_FAST                'options'
              214  LOAD_ATTR                surject
            216_0  COME_FROM           210  '210'
              216  POP_JUMP_IF_FALSE   230  'to 230'

 L. 130       218  LOAD_GLOBAL              require
              220  LOAD_FAST                'options'
              222  LOAD_ATTR                gams
              224  LOAD_STR                 '--gams must be given with --call and --surject'
              226  CALL_FUNCTION_2       2  '2 positional arguments'
              228  POP_TOP          
            230_0  COME_FROM           216  '216'

 L. 131       230  LOAD_GLOBAL              require
              232  LOAD_FAST                'options'
              234  LOAD_ATTR                vcfeval_bed_regions
              236  LOAD_CONST               None
              238  COMPARE_OP               is-not
              240  JUMP_IF_TRUE_OR_POP   248  'to 248'
              242  LOAD_FAST                'options'
              244  LOAD_ATTR                clip_only
              246  UNARY_NOT        
            248_0  COME_FROM           240  '240'

 L. 132       248  LOAD_STR                 '--vcfeval_bed_regions must be given with --clip_only'
              250  CALL_FUNCTION_2       2  '2 positional arguments'
              252  POP_TOP          

 L. 133       254  LOAD_FAST                'options'
              256  LOAD_ATTR                surject
              258  POP_JUMP_IF_TRUE    270  'to 270'
              262  LOAD_FAST                'options'
              264  LOAD_ATTR                bams
            266_0  COME_FROM           258  '258'
              266  POP_JUMP_IF_FALSE   290  'to 290'

 L. 134       270  LOAD_GLOBAL              require
              272  LOAD_FAST                'options'
              274  LOAD_ATTR                freebayes
              276  JUMP_IF_TRUE_OR_POP   284  'to 284'
              280  LOAD_FAST                'options'
              282  LOAD_ATTR                platypus
            284_0  COME_FROM           276  '276'

 L. 135       284  LOAD_STR                 '--freebayes and/or --platypus must be used with --bams and --surject'
              286  CALL_FUNCTION_2       2  '2 positional arguments'
              288  POP_TOP          
            290_0  COME_FROM           266  '266'

 L. 136       290  LOAD_FAST                'options'
              292  LOAD_ATTR                normalize
              294  POP_JUMP_IF_FALSE   318  'to 318'

 L. 137       298  LOAD_GLOBAL              require
              300  LOAD_FAST                'options'
              302  LOAD_ATTR                vcfeval_fasta
              304  JUMP_IF_FALSE_OR_POP   312  'to 312'
              308  LOAD_FAST                'options'
              310  LOAD_ATTR                sveval
            312_0  COME_FROM           304  '304'
              312  LOAD_STR                 '--vcfeval_fasta and --sveval required with --normalized'
              314  CALL_FUNCTION_2       2  '2 positional arguments'
              316  POP_TOP          
            318_0  COME_FROM           294  '294'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 80


def run_bam_index(job, context, bam_file_id, bam_name):
    """
    sort and index a bam.  return the sorted bam and its idx
    """
    work_dir = job.fileStore.getLocalTempDir()
    bam_path = os.path.joinwork_dirbam_name + '.bam'
    job.fileStore.readGlobalFilebam_file_idbam_path
    sort_bam_path = os.path.joinwork_dir'sort.bam'
    sort_cmd = ['samtools', 'sort', os.path.basename(bam_path), '-o',
     os.path.basename(sort_bam_path), '-O', 'BAM', '-@', max0job.cores - 1]
    context.runner.call(job, sort_cmd, work_dir=work_dir)
    bam_index_cmd = ['samtools', 'index', os.path.basename(sort_bam_path)]
    context.runner.call(job, bam_index_cmd, work_dir=work_dir)
    out_bam_id = context.write_intermediate_filejobsort_bam_path
    out_idx_id = context.write_intermediate_filejobsort_bam_path + '.bai'
    return (out_bam_id, out_idx_id)


def run_all_bam_caller(job, context, fasta_file_id, bam_file_id, bam_idx_id, sample_name, chroms, offsets, out_name, bam_caller, bam_caller_opts=[]):
    """
    run freebayes or platypus on a set of chromosomal regions.  this is done by sending each region to a 
    child job and farming off the entire input to each (ie not splitting the input)
    """
    child_job = Job()
    job.addChild(child_job)
    fb_vcf_ids = []
    fb_tbi_ids = []
    fb_timers = []
    assert chroms
    if not offsets:
        offsets = [
         None] * len(chroms)
    for chrom, offset in zipchromsoffsets:
        fb_job = child_job.addChildJobFn(run_bam_caller, context, fasta_file_id, bam_file_id, bam_idx_id, sample_name,
          chrom, offset, out_name, bam_caller, bam_caller_opts, memory=(context.config.calling_mem),
          disk=(context.config.calling_disk))
        fb_vcf_ids.append(fb_job.rv(0))
        fb_tbi_ids.append(fb_job.rv(1))
        fb_timers.append([fb_job.rv(2)])

    merge_vcf_job = child_job.addFollowOnJobFn(run_concat_vcfs, context, out_name, fb_vcf_ids, fb_tbi_ids, write_to_outstore=True,
      call_timers_lists=fb_timers)
    return merge_vcf_job.rv()


def run_bam_caller(job, context, fasta_file_id, bam_file_id, bam_idx_id, sample_name, chrom, offset, out_name, bam_caller, bam_caller_opts):
    """
    run freebayes or platypus to make a vcf
    """
    if not bam_caller in ('freebayes', 'platypus'):
        raise AssertionError
    else:
        work_dir = job.fileStore.getLocalTempDir()
        fasta_path = os.path.joinwork_dir'ref.fa'
        bam_path = os.path.joinwork_dir'alignment.bam'
        bam_idx_path = bam_path + '.bai'
        job.fileStore.readGlobalFilefasta_file_idfasta_path
        job.fileStore.readGlobalFilebam_file_idbam_path
        job.fileStore.readGlobalFilebam_idx_idbam_idx_path
        vcf_path = os.path.joinwork_dir'{}-raw.vcf'.format(out_name)
        if bam_caller == 'freebayes':
            fb_cmd = [
             'freebayes', '-f', os.path.basename(fasta_path), os.path.basename(bam_path)]
            if bam_caller_opts:
                fb_cmd += bam_caller_opts
            if chrom:
                fb_cmd += ['-r', chrom]
            timer = TimeTracker('freebayes')
            with openvcf_path'wb' as (out_vcf):
                context.runner.call(job, fb_cmd, work_dir=work_dir, outfile=out_vcf)
            timer.stop()
        else:
            if bam_caller == 'platypus':
                context.runner.call(job, ['samtools', 'faidx', 'ref.fa'], work_dir=work_dir)
                plat_cmd = ['Platypus.py', 'callVariants', '--refFile', os.path.basename(fasta_path),
                 '--bamFiles', os.path.basename(bam_path), '-o', os.path.basename(vcf_path)]
                if bam_caller_opts:
                    plat_cmd += bam_caller_opts
                if chrom:
                    plat_cmd += ['--regions', chrom]
                timer = TimeTracker('Platypus')
                context.runner.call(job, plat_cmd, work_dir=work_dir)
                timer.stop()
            else:
                assert False
        context.write_intermediate_filejobvcf_path
        vcf_fix_path = os.path.joinwork_dir'{}.vcf'.format(out_name)
        vcf_reader = vcf.Reader(open(vcf_path))
        if sample_name:
            assert len(vcf_reader.samples) == 1
            RealtimeLogger.info('Correcting Freebayes samples {} to [{}]'.formatvcf_reader.samplessample_name)
            vcf_reader.samples = [sample_name]
            vcf_reader._sample_indexes = {sample_name: 0}
        vcf_writer = vcf.Writeropenvcf_fix_path'w'vcf_reader
        have_records = False
        for record in vcf_reader:
            have_records = True
            if offset:
                record.POS += int(offset)
            vcf_writer.write_record(record)

        vcf_writer.flush()
        vcf_writer.close()
        have_records or RealtimeLogger.error('{} produced no calls. Dumping files...'.format(bam_caller))
        for dump_path in [fasta_path, bam_path, bam_idx_path]:
            if dump_path and os.path.isfile(dump_path):
                context.write_output_filejobdump_path

        raise RuntimeError('{} produced no calls'.format(bam_caller))
    context.runner.call(job, ['bgzip', os.path.basename(vcf_fix_path)], work_dir=work_dir)
    context.runner.call(job, ['tabix', '-p', 'vcf', os.path.basename(vcf_fix_path) + '.gz'], work_dir=work_dir)
    return (
     context.write_output_filejobvcf_fix_path + '.gz',
     context.write_output_filejobvcf_fix_path + '.gz.tbi',
     timer)


def run_calleval_plots(job, context, names, eval_results_dict, plot_sets):
    """
    
    Make and output calleval ROC plots.
    
    Takes a "names" list of all conditions. Condition names in the list (or in
    plot_sets) do not include an "-unclipped" tag; both clipped and unclipped
    plots are made if the data is available.
    
    Takes a nested dict by condition name, then clipping status ("clipped",
    "unclipped"), and then variant type ("snp", "non_snp", "weighted").
    Eventual entries are to ROC data file ids (.tsv.gz).
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets.
    
    Returns a list of created plot file IDs.
    
    """
    roc_plot_ids = []
    for roc_type in ('snp', 'non_snp', 'weighted'):
        for mode in ('unclipped', 'clipped'):
            roc_kind = roc_type
            if mode == 'unclipped':
                if True in ['clipped' in eval_results_dict for eval_result in eval_results_dict.values()]:
                    roc_kind += '-unclipped'
            mode_results = {name:eval_result.get(mode) for name, eval_result in list(eval_results_dict.items())}
            if None in iter(mode_results.values()):
                pass
            else:
                roc_table_ids = {name:result.get(roc_type) for name, result in list(mode_results.items())}
                for subset_number, plot_set in enumerate(plot_sets):
                    plot_title, plot_conditions = plot_set
                    if plot_conditions is None:
                        plot_conditions = names
                    if plot_title is None:
                        plot_title = roc_kind
                    else:
                        plot_title = '{} ({})'.formatplot_titleroc_kind
                    for name in plot_conditions:
                        if name not in names:
                            message = 'Condition {} not found in list of available conditions {}'.formatnamenames
                            RealtimeLogger.error(message)
                            raise RuntimeError(message)
                        if name not in roc_table_ids:
                            message = 'Condition {} has no ROC data; data only available for {}'.formatnamelist(roc_table_ids.keys())
                            RealtimeLogger.error(message)
                            raise RuntimeError(message)

                    subset_ids = [roc_table_ids[name] for name in plot_conditions]
                    roc_plot_ids.append(job.addChildJobFn(run_vcfeval_roc_plot, context, subset_ids, names=plot_conditions, kind=roc_kind,
                      number=subset_number,
                      title=plot_title).rv())

    return roc_plot_ids


def run_calleval_results(job, context, names, vcf_tbi_pairs, eval_results_dict, happy_results_dict, sveval_results_dict, timing_results, plot_sets):
    """
    
    output the calleval results
    
    Requires that, if any result in eval_results has clipped results, all
    results have clipped results, and similarly for unclipped results.

    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets.
    
    """
    RealtimeLogger.info('Handling results for conditions {} in sets {}'.formatnamesplot_sets)
    work_dir = job.fileStore.getLocalTempDir()
    stats_path = os.path.joinwork_dir'calleval_stats.tsv'
    with openstats_path'w' as (stats_file):
        for name in names:
            eval_result = eval_results_dict[name]
            happy_result = happy_results_dict[name]
            best_result = eval_result.get'clipped'eval_result.get'unclipped'None
            best_happy_result = happy_result.get'clipped'happy_result.get'unclipped'None
            if best_happy_result is not None:
                happy_snp_f1 = best_happy_result['parsed_summary']['SNP']['METRIC.F1_Score']
                happy_indel_f1 = best_happy_result['parsed_summary']['INDEL']['METRIC.F1_Score']
            else:
                happy_snp_f1, happy_indel_f1 = (-1, -1)
            sveval_result = sveval_results_dict[name]
            best_sveval_result = sveval_result.get'clipped'sveval_result.get'unclipped'None
            sveval_f1 = best_sveval_result['F1'] if best_sveval_result is not None else -1
            stats_file.write('{}\t{}\t{}\t{}\n'.format(name, best_result['f1'], happy_snp_f1, happy_indel_f1))

    roc_plot_job = job.addChildJobFn(run_calleval_plots, context, names, eval_results_dict, plot_sets)
    roc_plot_ids = roc_plot_job.rv()
    times_path = os.path.joinwork_dir'call_times.tsv'
    calling_labels = [
     'call', 'freebayes', 'platypus']
    augmenting_labels = ['call-filter-augment', 'call-augment', 'call-filter']
    all_labels = set()
    for timer in timing_results:
        for label in timer.names():
            all_labels.add(label)

    other_labels = all_labels - set(calling_labels + augmenting_labels)
    with opentimes_path'w' as (times_file):
        times_file.write('method\tcall\taugment\ttotal-other')
        for other_label in other_labels:
            times_file.write('\t{}'.format(other_label.replace'call-'''))

        times_file.write('\n')
        for name, timer in zipnamestiming_results:
            times_file.write('{}\t{}'.formatnametimer.total(calling_labels))
            times_file.write('\t{}'.format(timer.total(augmenting_labels)))
            times_file.write('\t{}'.format(timer.total(other_labels)))
            for other_label in other_labels:
                times_file.write('\t{}'.format(timer.total([other_label])))

            times_file.write('\n')

    return roc_plot_job.addFollowOnJobFn(run_concat_lists, [
     context.write_output_filejobstats_path, context.write_output_filejobtimes_path], roc_plot_ids).rv()


def run_vcf_subset(job, context, vcf_file_id, tbi_file_id, regions):
    work_dir = job.fileStore.getLocalTempDir()
    vcf_path = os.path.joinwork_dir'input.vcf.gz'
    out_vcf_path = os.path.joinwork_dir'output.vcf.gz'
    job.fileStore.readGlobalFilevcf_file_idvcf_path
    job.fileStore.readGlobalFiletbi_file_idvcf_path + '.tbi'
    cmd = [
     'bcftools', 'view', os.path.basename(vcf_path), '--regions', ','.join(regions),
     '--output-type', 'z', '--output-file', os.path.basename(out_vcf_path)]
    context.runner.call(job, cmd, work_dir=work_dir)
    context.runner.call(job, ['tabix', '--preset', 'vcf', os.path.basename(out_vcf_path)], work_dir=work_dir)
    return (context.write_intermediate_filejobout_vcf_path,
     context.write_intermediate_filejobout_vcf_path + '.tbi')


def run_calleval(job, context, xg_ids, gam_ids, gam_idx_ids, bam_ids, bam_idx_ids, gam_names, bam_names, vcfeval_baseline_id, vcfeval_baseline_tbi_id, caller_fasta_id, vcfeval_fasta_id, bed_id, clip_only, call, sample_name, chroms, vcf_offsets, vcfeval_score_field, plot_sets, surject, interleaved, freebayes, platypus, happy, sveval, recall, min_sv_len, max_sv_len, sv_overlap, sv_region_overlap, normalize, ins_ref_len, del_min_rol, ins_seq_comp, min_mapq=0, min_baseq=0, min_augment_coverage=0):
    """
    top-level call-eval function. Runs the caller on every
    gam, and freebayes on every bam. The resulting vcfs are put through
    vcfeval and the accuracies are tabulated in the output.
    
    Returns the output of run_calleval results, a list of condition names, a
    list of corresponding called VCF.gz and index ID pairs, and dicts of
    vcfeval and happy result dicts, by condition name and clipped/unclipped
    status.

    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets.
    
    """
    names = []
    vcf_tbi_id_pairs = []
    timing_results = []
    eval_results = collections.defaultdict(dict)
    happy_results = collections.defaultdict(dict)
    sveval_results = collections.defaultdict(dict)
    head_job = Job()
    job.addChild(head_job)
    child_job = Job()
    head_job.addFollowOn(child_job)
    sample_extract_job = head_job.addChildJobFn(run_make_control_vcfs, context, vcfeval_baseline_id, 'baseline.vcf.gz', vcfeval_baseline_tbi_id,
      sample_name, pos_only=True, no_filter_if_sample_not_found=True,
      cores=(context.config.vcfeval_cores),
      memory=(context.config.vcfeval_mem),
      disk=(context.config.vcfeval_disk))
    truth_vcf_id = sample_extract_job.rv(0)
    truth_vcf_tbi_id = sample_extract_job.rv(1)
    if not gam_idx_ids:
        gam_idx_ids = [
         None] * len(gam_ids)
    elif not len(gam_idx_ids) == len(gam_ids):
        raise AssertionError
    if surject:
        for xg_id, gam_name, gam_id in zip(xg_ids, gam_names, gam_ids):
            surject_job = head_job.addChildJobFn(run_surjecting, context, gam_id, (gam_name + '-surject'), interleaved,
              xg_id, chroms, cores=(context.config.misc_cores), memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            bam_ids.append(surject_job.rv())
            bam_idx_ids.append(None)
            bam_names.append(gam_name + '-surject')

    if bam_ids:
        for bam_id, bam_idx_id, bam_name in zip(bam_ids, bam_idx_ids, bam_names):
            if not bam_idx_id:
                bam_index_job = child_job.addChildJobFn(run_bam_index, context, bam_id, bam_name, cores=(context.config.calling_cores),
                  memory=(context.config.calling_mem),
                  disk=(context.config.calling_disk))
                sorted_bam_id = bam_index_job.rv(0)
                sorted_bam_idx_id = bam_index_job.rv(1)
            else:
                bam_index_job = Job()
                child_job.addChild(bam_index_job)
                sorted_bam_id = bam_id
                sorted_bam_idx_id = bam_idx_id
            bam_caller_infos = []
            if freebayes:
                bam_caller_infos.append(('freebayes', ['--genotype-qualities'], '-fb'))
            if platypus:
                bam_caller_infos.append(('platypus', ['--mergeClusteredVariants=1'], '-plat'))
            for bam_caller, bam_caller_opts, bam_caller_tag in bam_caller_infos:
                bam_caller_out_name = '{}{}'.formatbam_namebam_caller_tag
                bam_caller_job = bam_index_job.addFollowOnJobFn(run_all_bam_caller, context, caller_fasta_id, sorted_bam_id,
                  sorted_bam_idx_id, sample_name, chroms,
                  vcf_offsets, out_name=bam_caller_out_name,
                  bam_caller=bam_caller,
                  bam_caller_opts=bam_caller_opts,
                  cores=(context.config.misc_cores),
                  memory=(context.config.misc_mem),
                  disk=(context.config.misc_disk))
                bam_caller_vcf_tbi_id_pair = (bam_caller_job.rv(0), bam_caller_job.rv(1))
                timing_result = bam_caller_job.rv(2)
                if bed_id:
                    eval_results[bam_caller_out_name]['clipped'] = bam_caller_job.addFollowOnJobFn(run_vcfeval, context, sample_name, bam_caller_vcf_tbi_id_pair, truth_vcf_id,
                      truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                      bed_id, out_name=bam_caller_out_name, score_field='GQ',
                      cores=(context.config.vcfeval_cores),
                      memory=(context.config.vcfeval_mem),
                      disk=(context.config.vcfeval_disk)).rv()
                    if happy:
                        happy_results[bam_caller_out_name]['clipped'] = bam_caller_job.addFollowOnJobFn(run_happy, context, sample_name, bam_caller_vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                          bed_id, out_name=bam_caller_out_name, cores=(context.config.vcfeval_cores),
                          memory=(context.config.vcfeval_mem),
                          disk=(context.config.vcfeval_disk)).rv()
                    if sveval:
                        sveval_results[bam_caller_out_name]['clipped'] = bam_caller_job.addFollowOnJobFn(run_sv_eval, context, sample_name, bam_caller_vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, min_sv_len=min_sv_len,
                          max_sv_len=max_sv_len,
                          sv_overlap=sv_overlap,
                          sv_region_overlap=sv_region_overlap,
                          bed_id=bed_id,
                          ins_ref_len=ins_ref_len,
                          del_min_rol=del_min_rol,
                          ins_seq_comp=ins_seq_comp,
                          out_name=bam_caller_out_name,
                          fasta_path='ref.fasta',
                          fasta_id=vcfeval_fasta_id,
                          normalize=normalize,
                          cores=(context.config.vcfeval_cores),
                          memory=(context.config.vcfeval_mem),
                          disk=(context.config.vcfeval_disk)).rv()
                if not clip_only:
                    eval_results[bam_caller_out_name]['unclipped'] = bam_caller_job.addFollowOnJobFn(run_vcfeval, context, sample_name, bam_caller_vcf_tbi_id_pair, truth_vcf_id,
                      truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                      None, out_name=(bam_caller_out_name if not bed_id else bam_caller_out_name + '-unclipped'),
                      score_field='GQ',
                      cores=(context.config.vcfeval_cores),
                      memory=(context.config.vcfeval_mem),
                      disk=(context.config.vcfeval_disk)).rv()
                    if happy:
                        happy_results[bam_caller_out_name]['unclipped'] = bam_caller_job.addFollowOnJobFn(run_happy, context, sample_name, bam_caller_vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                          None, out_name=(bam_caller_out_name if not bed_id else bam_caller_out_name + '-unclipped'),
                          cores=(context.config.vcfeval_cores),
                          memory=(context.config.vcfeval_mem),
                          disk=(context.config.vcfeval_disk)).rv()
                    if sveval:
                        sveval_results[bam_caller_out_name]['unclipped'] = bam_caller_job.addFollowOnJobFn(run_sv_eval, context, sample_name, bam_caller_vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, min_sv_len=min_sv_len,
                          max_sv_len=max_sv_len,
                          sv_overlap=sv_overlap,
                          sv_region_overlap=sv_region_overlap,
                          bed_id=None,
                          ins_ref_len=ins_ref_len,
                          del_min_rol=del_min_rol,
                          ins_seq_comp=ins_seq_comp,
                          out_name=(bam_caller_out_name if not bed_id else bam_caller_out_name + '-unclipped'),
                          fasta_path='ref.fasta',
                          fasta_id=vcfeval_fasta_id,
                          normalize=normalize,
                          cores=(context.config.vcfeval_cores),
                          memory=(context.config.vcfeval_mem),
                          disk=(context.config.vcfeval_disk)).rv()
                vcf_tbi_id_pairs.append(bam_caller_vcf_tbi_id_pair)
                timing_results.append(timing_result)
                names.append(bam_caller_out_name)

    if gam_ids:
        for gam_id, gam_idx_id, gam_name, xg_id in zip(gam_ids, gam_idx_ids, gam_names, xg_ids):
            if call:
                out_name = '{}{}'.formatgam_name'-call'
                if context.config.filter_opts:
                    filter_job = Job.wrapJobFn(run_filtering, context, graph_id=xg_id,
                      graph_basename='graph.xg',
                      gam_id=gam_id,
                      gam_basename='aln.gam',
                      filter_opts=(context.config.filter_opts),
                      cores=(context.config.calling_cores),
                      memory=(context.config.calling_mem),
                      disk=(context.config.calling_disk))
                    gam_id = filter_job.rv()
                call_job = Job.wrapJobFn(run_chunked_calling, context, graph_id=xg_id,
                  graph_basename='graph.xg',
                  gam_id=gam_id,
                  gam_basename='aln.gam',
                  batch_input=None,
                  snarls_id=None,
                  genotype_vcf_id=None,
                  genotype_tbi_id=None,
                  sample=sample_name,
                  augment=(not recall),
                  connected_component_chunking=False,
                  output_format='pg',
                  min_augment_coverage=min_augment_coverage,
                  expected_coverage=None,
                  min_mapq=min_mapq,
                  min_baseq=min_baseq,
                  ref_paths=chroms,
                  ref_path_chunking=False,
                  min_call_support=None,
                  vcf_offsets=vcf_offsets,
                  cores=(context.config.misc_cores),
                  memory=(context.config.misc_mem),
                  disk=(context.config.misc_disk))
                if context.config.filter_opts:
                    child_job.addChild(filter_job)
                    filter_job.addFollowOn(call_job)
                else:
                    child_job.addChild(call_job)
                vcf_tbi_id_pair = (call_job.rv(0), call_job.rv(1))
                timing_result = TimeTracker()
                if not vcfeval_score_field:
                    score_field = 'QUAL'
                else:
                    score_field = vcfeval_score_field
                if bed_id:
                    eval_results[out_name]['clipped'] = call_job.addFollowOnJobFn(run_vcfeval, context, sample_name, vcf_tbi_id_pair, truth_vcf_id,
                      truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                      bed_id, out_name=out_name, score_field=score_field).rv()
                    if happy:
                        happy_results[out_name]['clipped'] = call_job.addFollowOnJobFn(run_happy, context, sample_name, vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                          bed_id, out_name=out_name).rv()
                    if sveval:
                        sveval_results[out_name]['clipped'] = call_job.addFollowOnJobFn(run_sv_eval, context, sample_name, vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, min_sv_len=min_sv_len,
                          max_sv_len=max_sv_len,
                          sv_overlap=sv_overlap,
                          sv_region_overlap=sv_region_overlap,
                          ins_ref_len=ins_ref_len,
                          del_min_rol=del_min_rol,
                          ins_seq_comp=ins_seq_comp,
                          bed_id=bed_id,
                          out_name=out_name,
                          fasta_path='ref.fasta',
                          fasta_id=vcfeval_fasta_id,
                          normalize=normalize).rv()
                if not clip_only:
                    eval_results[out_name]['unclipped'] = call_job.addFollowOnJobFn(run_vcfeval, context, sample_name, vcf_tbi_id_pair, truth_vcf_id,
                      truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                      None, out_name=(out_name if not bed_id else out_name + '-unclipped'),
                      score_field=score_field).rv()
                    if happy:
                        happy_results[out_name]['unclipped'] = call_job.addFollowOnJobFn(run_happy, context, sample_name, vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, 'ref.fasta', vcfeval_fasta_id,
                          None, out_name=(out_name if not bed_id else out_name + '-unclipped')).rv()
                    if sveval:
                        sveval_results[out_name]['unclipped'] = call_job.addFollowOnJobFn(run_sv_eval, context, sample_name, vcf_tbi_id_pair, truth_vcf_id,
                          truth_vcf_tbi_id, min_sv_len=min_sv_len,
                          max_sv_len=max_sv_len,
                          sv_overlap=sv_overlap,
                          sv_region_overlap=sv_region_overlap,
                          bed_id=None,
                          ins_ref_len=ins_ref_len,
                          del_min_rol=del_min_rol,
                          ins_seq_comp=ins_seq_comp,
                          out_name=(out_name if not bed_id else out_name + '-unclipped'),
                          fasta_path='ref.fasta',
                          fasta_id=vcfeval_fasta_id,
                          normalize=normalize).rv()
                vcf_tbi_id_pairs.append(vcf_tbi_id_pair)
                timing_results.append(timing_result)
                names.append(out_name)

    calleval_results = child_job.addFollowOnJobFn(run_calleval_results, context, names, vcf_tbi_id_pairs,
      eval_results, happy_results, sveval_results, timing_results,
      plot_sets, cores=(context.config.misc_cores),
      memory=(context.config.misc_mem),
      disk=(context.config.misc_disk)).rv()
    return (
     calleval_results, names, vcf_tbi_id_pairs, eval_results)


def calleval_main(context, options):
    """ entrypoint for calling """
    validate_calleval_options(options)
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            importer = AsyncImporter(toil)
            inputXGFileIDs = []
            xgToID = {}
            if options.xg_paths:
                for xg_path in options.xg_paths:
                    if xg_path not in xgToID:
                        xgToID[xg_path] = importer.load(xg_path)
                    inputXGFileIDs.append(xgToID[xg_path])

            inputGamFileIDs = []
            inputGamIdxIDs = []
            gamToID = {}
            gaiToID = {}
            if options.gams:
                for gam in options.gams:
                    if gam not in gamToID:
                        gamToID[gam] = importer.load(gam)
                    inputGamFileIDs.append(gamToID[gam])
                    gai = gam + '.gai'
                    if gai not in gaiToID:
                        try:
                            gaiToID[gai] = toil.importFile(gai)
                        except:
                            gaiToID[gai] = None

                    inputGamIdxIDs.append(gaiToID[gai])

            inputBamFileIDs = []
            inputBamIdxIds = []
            if options.bams:
                for bam in options.bams:
                    inputBamFileIDs.append(importer.load(bam))
                    try:
                        bamIdxId = toil.importFile(bam + '.bai')
                    except:
                        bamIdxId = None

                    inputBamIdxIds.append(bamIdxId)

            vcfeval_baseline_id = importer.load(options.vcfeval_baseline)
            vcfeval_baseline_tbi_id = importer.load((options.vcfeval_baseline + '.tbi'), wait_on=vcfeval_baseline_id)
            vcfeval_fasta_id = importer.load(options.vcfeval_fasta)
            bed_id = importer.load(options.vcfeval_bed_regions) if options.vcfeval_bed_regions is not None else None
            clip_only = options.clip_only
            plot_sets = parse_plot_sets(options.plot_sets)
            importer.wait()
            if options.vcf_offsets:
                vcf_offset_dict = {}
                for ref_path_name, vcf_offset in zipoptions.ref_pathsoptions.vcf_offsets:
                    vcf_offset_dict[ref_path_name] = vcf_offset

                options.vcf_offsets = vcf_offset_dict
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, (sys.argv), memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            if options.vcfeval_fasta.endswith('.gz'):
                vcfeval_fasta_id = init_job.addChildJobFn(run_unzip_fasta, context, importer.resolve(vcfeval_fasta_id), os.path.basename(options.vcfeval_fasta)).rv()
            if options.caller_fasta is not None:
                caller_fasta_id = toil.importFile(options.caller_fasta)
                if options.caller_fasta.endswith('.gz'):
                    caller_fasta_id = init_job.addChildJobFn(run_unzip_fasta, context, caller_fasta_id, os.path.basename(options.vcfeval_fasta)).rv()
            else:
                caller_fasta_id = vcfeval_fasta_id
            if options.ref_paths:
                vcf_subset_job = init_job.addChildJobFn(run_vcf_subset, context, (importer.resolve(vcfeval_baseline_id)), (importer.resolve(vcfeval_baseline_tbi_id)),
                  (options.ref_paths),
                  disk=(context.config.vcfeval_disk))
                vcfeval_baseline_id, vcfeval_baseline_tbi_id = vcf_subset_job.rv(0), vcf_subset_job.rv(1)
            if options.vcf_offsets:
                vcf_offset_dict = {}
                for ref_path_name, vcf_offset in zipoptions.ref_pathsoptions.vcf_offsets:
                    vcf_offset_dict[ref_path_name] = vcf_offset

                options.vcf_offsets = vcf_offset_dict
            root_job = Job.wrapJobFn(run_calleval, context, (importer.resolve(inputXGFileIDs)),
              (importer.resolve(inputGamFileIDs)),
              (importer.resolve(inputGamIdxIDs)),
              (importer.resolve(inputBamFileIDs)),
              (importer.resolve(inputBamIdxIds)),
              (options.gam_names),
              (options.bam_names), (importer.resolve(vcfeval_baseline_id)),
              (importer.resolve(vcfeval_baseline_tbi_id)),
              (importer.resolve(caller_fasta_id)),
              (importer.resolve(vcfeval_fasta_id)),
              (importer.resolve(bed_id)),
              clip_only, (options.call),
              (options.sample),
              (options.ref_paths),
              (options.vcf_offsets), (options.vcfeval_score_field),
              plot_sets,
              (options.surject),
              (options.interleaved),
              (options.freebayes),
              (options.platypus),
              (options.happy),
              (options.sveval),
              (options.recall),
              (options.min_sv_len),
              (options.max_sv_len),
              (options.sv_overlap),
              (options.sv_region_overlap),
              (options.normalize),
              min_mapq=(options.min_mapq),
              min_baseq=(options.min_baseq),
              min_augment_coverage=(options.min_augment_coverage),
              ins_ref_len=(options.ins_max_gap),
              del_min_rol=(options.del_min_rol),
              ins_seq_comp=(options.ins_seq_comp),
              cores=(context.config.misc_cores),
              memory=(context.config.misc_mem),
              disk=(context.config.misc_disk))
            init_job.addFollowOn(root_job)
            toil.start(init_job)
        else:
            toil.restart()
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
    logger.info('All jobs completed successfully. Pipeline took {} seconds.'.format(run_time_pipeline))