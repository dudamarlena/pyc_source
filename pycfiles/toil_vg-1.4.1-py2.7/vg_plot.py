# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_plot.py
# Compiled at: 2018-11-03 15:09:40
"""
vg_plot.py: Make plots from toil-vg experiments

"""
from __future__ import print_function
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, SocketServer, struct, socket, threading, string, math, urlparse, getpass, pdb, gzip, logging, copy
from collections import Counter
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import require, make_url, remove_ext, add_common_vg_parse_args, add_container_tool_parse_args, parse_plot_sets
from toil_vg.vg_mapeval import run_map_eval_summarize, run_map_eval_table, run_map_eval_plot
from toil_vg.vg_calleval import run_calleval_plots
from toil_vg.context import Context, run_write_info_to_outstore
logger = logging.getLogger(__name__)

def plot_subparser(parser):
    """
    Create a subparser for plot.  Should pass in results of subparsers.add_parser()
    """
    Job.Runner.addToilOptions(parser)
    parser.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    add_plot_options(parser)
    add_container_tool_parse_args(parser)


def add_plot_options(parser):
    """
    Add the mapeval options to the given argparse parser.
    """
    parser.add_argument('--position-stats', type=make_url, default=None, help='position.results.tsv file from a mapeval run')
    parser.add_argument('--tables-only', action='store_true', help='make only summary tables and not plots')
    parser.add_argument('--plots-only', action='store_true', help='make only plots and not summary tables')
    parser.add_argument('--roc-base', help='ROC file base URL, under which <condition>_vcfeval_output/<type>_roc.tsv.gz files exist')
    parser.add_argument('--names', nargs='+', help='condition names for ROC files to load')
    parser.add_argument('--clipping', nargs='+', default=['clipped'], help='clipping modes to load')
    parser.add_argument('--plot-sets', nargs='+', default=[], help='comma-separated lists of condition-tagged GAM names (primary-mp-pe, etc.) with colon-separated title prefixes')
    add_common_vg_parse_args(parser)
    return


def validate_options(options):
    """
    Throw an error if an invalid combination of options has been selected.
    """
    require(options.position_stats or options.roc_base, 'either --position-stats or --roc-base is required')
    require(not (options.position_stats and options.roc_base), 'cannot operate on --position-stats and --roc-base in the same run')
    require(options.roc_base is None or options.names is not None, '--roc-base requires --names')
    require(options.names is None or options.roc_base is not None, '--names requires --roc-base')
    return


def run_plot(job, context, options, position_stats_file_id=None, eval_results_dict=None, plot_sets=[None]):
    """
    Main Toil job.
    
    If position_stats_file_id is given, make mapping plots and/or tables based
    on the given position_stats_file_id stats file, restricting to the given
    set of sets of conditions to plot.
    
    If instead eval_results_dict is given, as a dict from condition name, then
    'clipped'/'unclipped', then 'snp'/'non_snp'/'weighted' to ROC data file ID,
    then plot the variant calling ROC curves.
    
    """
    if position_stats_file_id is not None:
        job_fn = run_map_eval_summarize
        if options.tables_only:
            job_fn = run_map_eval_table
        if options.plots_only:
            job_fn = run_map_eval_plot
        plot_job = job.addChildJobFn(job_fn, context, position_stats_file_id, plot_sets, cores=context.config.misc_cores, memory=context.config.misc_mem, disk=context.config.misc_disk)
    elif eval_results_dict is not None:
        names = eval_results_dict.keys()
        plot_job = job.addChildJobFn(run_calleval_plots, context, names, eval_results_dict, plot_sets=plot_sets)
    else:
        raise RuntimeError('No position stats or vcfeval results available!')
    return


def make_plot_plan(toil, options):
    """
    Import all the necessary files form options into Toil.
    
    Keep the IDs under names in an argparse namespace that functions as a "plan"
    for the workflow.
    
    """
    plan = argparse.Namespace()
    start_time = timeit.default_timer()
    plan.position_stats_file_id = None
    if options.position_stats:
        plan.position_stats_file_id = toil.importFile(options.position_stats)
    plan.eval_results_dict = None
    if options.roc_base:
        plan.eval_results_dict = collections.defaultdict(lambda : collections.defaultdict(dict))
        for condition in options.names:
            for clipping in options.clipping:
                clip_tag_condition = condition
                if clipping == 'unclipped' and 'clipped' in options.clipping:
                    clip_tag_condition += '-unclipped'
                for roc_name in ['snp', 'non_snp', 'weighted']:
                    url = make_url(options.roc_base + '/' + clip_tag_condition + '_vcfeval_output/' + roc_name + '_roc.tsv.gz')
                    plan.eval_results_dict[condition][clipping][roc_name] = toil.importFile(url)

    plan.plot_sets = parse_plot_sets(options.plot_sets)
    end_time = timeit.default_timer()
    logger.info(('Imported input files into Toil in {} seconds').format(end_time - start_time))
    return plan


def plot_main(context, options):
    """
    Run the mapeval workflow.
    """
    validate_options(options)
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    t = copy.deepcopy(context)
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            plan = make_plot_plan(toil, options)
            main_job = Job.wrapJobFn(run_plot, context, options, position_stats_file_id=plan.position_stats_file_id, eval_results_dict=plan.eval_results_dict, plot_sets=plan.plot_sets)
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, sys.argv)
            init_job.addFollowOn(main_job)
            toil.start(init_job)
        else:
            toil.restart()
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
    print(('All jobs completed successfully. Pipeline took {} seconds.').format(run_time_pipeline))
    return