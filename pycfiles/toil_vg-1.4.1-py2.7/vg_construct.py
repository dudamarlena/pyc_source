# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/vg_construct.py
# Compiled at: 2018-11-03 15:09:40
"""
vg_construct.py: construct a graph from a vcf and fasta

"""
from __future__ import print_function
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile, doctest, re, json, collections, time, timeit, logging, logging.handlers, SocketServer, struct, socket, threading, string, urlparse, getpass, pdb, logging, os
from math import ceil
from subprocess import Popen, PIPE
from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import *
from toil_vg.context import Context, run_write_info_to_outstore
from toil_vg.vg_index import run_xg_indexing, run_indexing, run_bwa_index, index_parse_args, index_toggle_parse_args
logger = logging.getLogger(__name__)
CEPH_SAMPLES = ('NA12889 NA12890 NA12891 NA12892 NA12877 NA12878 NA12879 NA12880 NA12881 NA12882 NA12883 NA12884 NA12885 NA12886 NA12887 NA12888 NA12893').split()

def construct_subparser(parser):
    """
    Create a subparser for construction.  Should pass in results of subparsers.add_parser()
    """
    Job.Runner.addToilOptions(parser)
    parser.add_argument('out_store', help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    parser.add_argument('--fasta', default=[], type=make_url, nargs='+', help='Reference sequence in fasta or fasta.gz (single fasta or 1/region in same order as --regions)')
    parser.add_argument('--vcf', default=[], type=make_url, nargs='+', help='Variants to make graph from (single vcf or 1/region in same order as --regions)')
    parser.add_argument('--regions', default=[], nargs='+', help='1-based inclusive VCF coordinates in the form of SEQ or SEQ:START-END')
    parser.add_argument('--fasta_regions', action='store_true', help='Infer regions from fasta file.  If multiple vcfs specified, any regions found that are not in --regions will be added without variants (useful for decoy sequences)')
    parser.add_argument('--max_node_size', type=int, default=32, help='Maximum node length')
    parser.add_argument('--alt_paths', action='store_true', help='Save paths for alts with variant ID')
    parser.add_argument('--flat_alts', action='store_true', help='flat alts')
    parser.add_argument('--construct_cores', type=int, help='Number of cores for vg construct')
    parser.add_argument('--out_name', default='graph', help='Name used for output graphs and indexes')
    parser.add_argument('--merge_graphs', action='store_true', help='Merge all regions into one graph')
    parser.add_argument('--normalize', action='store_true', help='Normalize the graphs')
    parser.add_argument('--primary', action='store_true', help='Make the primary graph (no variants) using just the FASTA')
    parser.add_argument('--pangenome', action='store_true', help='Make the pangenome graph using the input VCF(s)')
    parser.add_argument('--pos_control', type=str, help='Make a positive control (ref path plus sample variants) using this sample')
    parser.add_argument('--neg_control', type=str, help='Make a negative control (exclude all sample variants) using this sample')
    parser.add_argument('--sample_graph', type=str, help='Make a sample graph (only contains sample haplotypes) using this sample.  Only  phased variants will be included.  Will also make a _withref version that includes reference')
    parser.add_argument('--haplo_sample', type=str, help='Make two haplotype thread graphs (for simulating from) for this sample.  Phasing information required in the input vcf.')
    parser.add_argument('--filter_ceph', action='store_true', help='Make a graph where all variants private to the CEPH pedigree, which includes NA12878 are excluded')
    parser.add_argument('--filter_samples', nargs='+', help='Make a graph where all variants private to the CEPH pedigree, which includes NA12878 are excluded')
    parser.add_argument('--min_af', type=float, default=[], nargs='+', help='Create a graph including only variants with given minium allele frequency. If multiple frequencies given, a graph will be made for each one')
    parser.add_argument('--bwa_reference', type=make_url, help='Make a BWA reference (set of indexes) from the given FASTA (not the --fasta FASTAs).')
    parser.add_argument('--handle_unphased', default='arbitrary', choices=[
     'skip', 'keep', 'arbitrary'], help='How to handle unphased variants in the VCF when creating the sample or haplo graph. "skip": ignore variants, just using the reference allele. "keep": keep the unphased variants, breaking up the haplotype paths (potential downstream effects on indexing). "arbitrary": choose an arbitrary phasing for the unphased variants')
    index_toggle_parse_args(parser)
    index_parse_args(parser)
    add_common_vg_parse_args(parser)
    add_container_tool_parse_args(parser)


def validate_construct_options(options):
    """
    Throw an error if an invalid combination of options has been selected.
    """
    require(options.regions or options.fasta_regions, '--regions or --fasta_regions required')
    require(options.vcf == [] or len(options.vcf) == 1 or not options.regions or len(options.vcf) <= len(options.regions), 'if many vcfs specified, cannot have more vcfs than --regions')
    require(len(options.fasta) == 1 or len(options.fasta) == len(options.regions), 'if many fastas specified, must be same number as --regions')
    require(len(options.fasta) == 1 or not options.fasta_regions, '--fasta_regions currently only works when single fasta specified with --fasta')
    require(len(options.fasta) > 0 or options.bwa_reference, 'either --fasta or --bwa_reference must be set to give something to construct')
    require(not options.gbwt_index or options.xg_index, '--xg_index required with --gbwt_index')
    require(not options.gbwt_index or not options.pangenome and not options.pos_control and not options.neg_control and not options.sample_graph and not options.haplo_sample and not options.min_af or len(options.vcf) >= 1, '--gbwt_index with any graph other than --primary requires --vcf')
    require(not options.sample_graph or options.regions or options.fasta_regions, '--regions or --fasta_regions required with --sample_graph')
    require(options.primary or options.pangenome or options.pos_control or options.neg_control or options.sample_graph or options.haplo_sample or options.filter_ceph or options.filter_samples or options.min_af or options.bwa_reference, 'At least one kind of graph or reference must be specified for construction')
    require(not options.vcf or options.pangenome or options.pos_control or options.neg_control or options.sample_graph or options.haplo_sample or options.filter_ceph or options.filter_samples or options.min_af, 'At least one kind of non-primary graph must be specified for construction with --vcf')
    require(options.vcf or not (options.pangenome or options.pos_control or options.neg_control or options.sample_graph or options.haplo_sample or options.filter_ceph or options.filter_samples or options.min_af), '--vcf required for construction of non-primary graph')
    require(options.pos_control is None or options.neg_control is None or options.pos_control == options.neg_control, '--pos_control_sample and --neg_control_sample must be the same')
    require(not options.haplo_sample or not options.sample_graph or options.haplo_sample == options.sample_graph, '--haplo_sample and --sample_graph must be the same')
    return


def run_unzip_fasta(job, context, fasta_id, fasta_name):
    """
    vg construct doesn't work with zipped fasta, so we run this on input fasta that end in .gz
    """
    work_dir = job.fileStore.getLocalTempDir()
    fasta_file = os.path.join(work_dir, os.path.basename(fasta_name))
    job.fileStore.readGlobalFile(fasta_id, fasta_file, mutable=True)
    context.runner.call(job, ['bgzip', '-d', os.path.basename(fasta_file)], work_dir=work_dir)
    return context.write_intermediate_file(job, fasta_file[:-3])


def run_scan_fasta_sequence_names(job, context, fasta_id, fasta_name, regions=None):
    """
    if no regions specified, scrape them out of the (uncompressed) fasta
    """
    work_dir = job.fileStore.getLocalTempDir()
    fasta_file = os.path.join(work_dir, os.path.basename(fasta_name))
    job.fileStore.readGlobalFile(fasta_id, fasta_file)
    cmd = [
     'grep', '>', os.path.basename(fasta_file)]
    grep_output = context.runner.call(job, cmd, work_dir=work_dir, check_output=True, tool_name='bgzip')
    seq_names = [] if not regions else regions
    for line in grep_output.split('\n'):
        if len(line) > 1:
            name = line.split()[0]
            if name.startswith('>') and (not regions or name[1:] not in regions):
                seq_names.append(name[1:])

    return seq_names


def run_generate_input_vcfs(job, context, vcf_ids, vcf_names, tbi_ids, regions, output_name, do_primary=False, do_pan=False, pos_control_sample=None, neg_control_sample=None, sample_graph=None, handle_unphased=None, haplo_sample=None, filter_samples=[], min_afs=[]):
    """
    Preprocessing step to make a bunch of vcfs if wanted:
    - positive control
    - negative control
    - family filter
    - primary
    - thresholded by a given minimum allele frequency
    returns a dictionary of name -> (vcf_id, vcf_name, tbi_id, merge_name, region_names) tuples
    where name can be used to, ex, tell the controls apart
    """
    output = dict()
    if do_primary:
        if regions:
            primary_region_names = [ 'primary_' + c.replace(':', '-') for c in regions ]
        else:
            primary_region_names = None
        primary_output_name = 'primary.vg' if '_' not in output_name else 'primary' + output_name[output_name.find('_') + 1:]
        output['primary'] = [[], [], [], primary_output_name, primary_region_names]
    if do_pan:
        output[output_name] = [
         vcf_ids, vcf_names, tbi_ids, output_name,
         [ output_name + '_' + c.replace(':', '-') for c in regions ] if regions else None]
    if pos_control_sample or neg_control_sample:
        control_sample = pos_control_sample if pos_control_sample else neg_control_sample
        assert not neg_control_sample or neg_control_sample == control_sample
        assert not pos_control_sample or pos_control_sample == control_sample
        pos_control_vcf_ids, pos_control_tbi_ids = [], []
        neg_control_vcf_ids, neg_control_tbi_ids = [], []
        pos_control_vcf_names, neg_control_vcf_names = [], []
        for vcf_id, vcf_name, tbi_id in zip(vcf_ids, vcf_names, tbi_ids):
            make_controls = job.addChildJobFn(run_make_control_vcfs, context, vcf_id, vcf_name, tbi_id, control_sample, pos_only=not neg_control_sample, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
            pos_control_vcf_ids.append(make_controls.rv(0))
            pos_control_tbi_ids.append(make_controls.rv(1))
            neg_control_vcf_ids.append(make_controls.rv(2))
            neg_control_tbi_ids.append(make_controls.rv(3))
            vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
            pos_control_vcf_names.append(('{}_{}.vcf.gz').format(vcf_base, control_sample))
            neg_control_vcf_names.append(('{}_minus_{}.vcf.gz').format(vcf_base, control_sample))

        if regions:
            pos_region_names = [ output_name + ('_{}').format(control_sample) + '_' + c.replace(':', '-') for c in regions ]
            neg_region_names = [ output_name + ('_minus_{}').format(control_sample) + '_' + c.replace(':', '-') for c in regions ]
        else:
            pos_region_names = None
            neg_region_names = None
        pos_output_name = remove_ext(output_name, '.vg') + ('_{}.vg').format(control_sample)
        neg_output_name = remove_ext(output_name, '.vg') + ('_minus_{}.vg').format(control_sample)
        if pos_control_sample:
            output['pos-control'] = [
             pos_control_vcf_ids, pos_control_vcf_names, pos_control_tbi_ids,
             pos_output_name, pos_region_names]
        if neg_control_sample:
            output['neg-control'] = [
             neg_control_vcf_ids, neg_control_vcf_names, neg_control_tbi_ids,
             neg_output_name, neg_region_names]
        if haplo_sample and haplo_sample == control_sample:
            output['haplo'] = output['pos-control']
    if sample_graph:
        sample_graph_vcf_ids, sample_graph_tbi_ids = [], []
        sample_graph_vcf_names = []
        for vcf_id, vcf_name, tbi_id in zip(vcf_ids, vcf_names, tbi_ids):
            make_sample = job.addChildJobFn(run_make_control_vcfs, context, vcf_id, vcf_name, tbi_id, sample_graph, pos_only=True, unphased_handling=handle_unphased, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
            sample_graph_vcf_ids.append(make_sample.rv(0))
            sample_graph_tbi_ids.append(make_sample.rv(1))
            vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
            sample_graph_vcf_names.append(('{}_{}_sample_withref.vcf.gz').format(vcf_base, sample_graph))

        if regions:
            sample_graph_region_names = [ output_name + ('_{}_sample_withref').format(sample_graph) + '_' + c.replace(':', '-') for c in regions ]
        else:
            sample_graph_region_names = None
        sample_graph_output_name = remove_ext(output_name, '.vg') + ('_{}_sample_withref.vg').format(sample_graph)
        output['sample-graph'] = [
         sample_graph_vcf_ids, sample_graph_vcf_names, sample_graph_tbi_ids,
         sample_graph_output_name, sample_graph_region_names]
    if haplo_sample:
        hap_control_vcf_ids, hap_control_tbi_ids = [], []
        hap_control_vcf_names = []
        if haplo_sample != pos_control_sample:
            for vcf_id, vcf_name, tbi_id in zip(vcf_ids, vcf_names, tbi_ids):
                make_controls = job.addChildJobFn(run_make_control_vcfs, context, vcf_id, vcf_name, tbi_id, haplo_sample, pos_only=True, unphased_handling=handle_unphased, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
                hap_control_vcf_ids.append(make_controls.rv(0))
                hap_control_tbi_ids.append(make_controls.rv(1))
                vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
                hap_control_vcf_names.append(('{}_{}_haplo.vcf.gz').format(vcf_base, haplo_sample))

        else:
            hap_control_vcf_ids = pos_control_vcf_ids
            hap_control_tbi_ids = pos_control_tbi_ids
            hap_control_vcf_names = [ n.replace('.vcf.gz', '_haplo.vcf.gz') for n in pos_control_vcf_names ]
        if regions:
            hap_region_names = [ output_name + ('_{}_haplo').format(haplo_sample) + '_' + c.replace(':', '-') for c in regions ]
        else:
            hap_region_names = None
        hap_output_name = remove_ext(output_name, '.vg') + ('_{}_haplo.vg').format(haplo_sample)
        output['haplo'] = [
         hap_control_vcf_ids, hap_control_vcf_names, hap_control_tbi_ids,
         hap_output_name, hap_region_names]
    if filter_samples:
        filter_vcf_ids, filter_tbi_ids = [], []
        filter_vcf_names = []
        for vcf_id, vcf_name, tbi_id in zip(vcf_ids, vcf_names, tbi_ids):
            filter_job = job.addChildJobFn(run_filter_vcf_samples, context, vcf_id, vcf_name, tbi_id, filter_samples, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
            filter_vcf_ids.append(filter_job.rv(0))
            filter_tbi_ids.append(filter_job.rv(1))
            vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
            filter_vcf_names.append(('{}_filter.vcf.gz').format(vcf_base))

        if regions:
            filter_region_names = [ output_name + '_filter' + '_' + c.replace(':', '-') for c in regions ]
        else:
            filter_region_names = None
        filter_output_name = remove_ext(output_name, '.vg') + '_filter.vg'
        output['filter'] = [
         filter_vcf_ids, filter_vcf_names, filter_tbi_ids,
         filter_output_name, filter_region_names]
    for min_af in min_afs:
        af_vcf_ids, af_tbi_ids = [], []
        af_vcf_names = []
        for vcf_id, vcf_name, tbi_id in zip(vcf_ids, vcf_names, tbi_ids):
            af_job = job.addChildJobFn(run_min_allele_filter_vcf_samples, context, vcf_id, vcf_name, tbi_id, min_af, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
            af_vcf_ids.append(af_job.rv(0))
            af_tbi_ids.append(af_job.rv(1))
            vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
            af_vcf_names.append(('{}_minaf_{}.vcf.gz').format(vcf_base, min_af))

        if regions:
            af_region_names = [ output_name + ('_minaf_{}').format(min_af) + '_' + c.replace(':', '-') for c in regions ]
        else:
            af_region_names = None
        af_output_name = remove_ext(output_name, '.vg') + ('_minaf_{}.vg').format(min_af)
        output[('minaf-{}').format(min_af)] = [
         af_vcf_ids, af_vcf_names, af_tbi_ids,
         af_output_name, af_region_names]

    if regions and len(regions) > len(vcf_ids) and len(vcf_ids) != 1:
        padding = [
         None] * (len(regions) - len(vcf_ids))
        for key, val in output.items():
            val[0] += padding
            val[1] += padding
            val[2] += padding

    return output


def run_construct_all(job, context, fasta_ids, fasta_names, vcf_inputs, max_node_size, alt_paths, flat_alts, regions, merge_graphs=False, sort_ids=False, join_ids=False, gcsa_index=False, xg_index=False, gbwt_index=False, id_ranges_index=False, snarls_index=False, haplo_extraction_sample=None, haplotypes=[0, 1], gbwt_prune=False, normalize=False):
    """ 
    construct many graphs in parallel, optionally doing indexing too. vcf_inputs
    is a list of tuples as created by run_generate_input_vcfs
    
    Returns a list of tuples of the form (vg_ids, vg_names, indexes), where
    indexes is the index dict from index type to file ID.
    
    """
    output = []
    for name, (vcf_ids, vcf_names, tbi_ids, output_name, region_names) in vcf_inputs.items():
        merge_output_name = output_name if merge_graphs or not regions or len(regions) < 2 else None
        output_name_base = remove_ext(output_name, '.vg')
        haplo_extraction = name in ('haplo', 'sample-graph')
        construct_job = job.addChildJobFn(run_construct_genome_graph, context, fasta_ids, fasta_names, vcf_ids, vcf_names, tbi_ids, max_node_size, gbwt_index or haplo_extraction or alt_paths, flat_alts, regions, region_names, sort_ids, join_ids, name, merge_output_name, normalize)
        mapping_id = construct_job.rv('mapping')
        joined_vg_ids = construct_job.rv('joined')
        joined_vg_names = [ remove_ext(i, '.vg') + '.vg' for i in region_names ]
        if merge_graphs or not regions or len(regions) < 2:
            single_vg_id = construct_job.rv('merged')
            single_vg_name = remove_ext(merge_output_name, '.vg') + '.vg'
        else:
            single_vg_id = None
            single_vg_name = None
        if not regions:
            chroms = []
            gbwt_regions = []
        else:
            chroms = [ p.split(':')[0] for p in regions ]
            assert len(chroms) == len(set(chroms))
            gbwt_regions = [ p for p in regions if ':' in p ]
        input_vcf_ids = []
        input_tbi_ids = []
        if haplo_extraction or gbwt_index:
            for vcf_id, tbi_id in zip(vcf_ids, tbi_ids):
                if vcf_id and tbi_id:
                    input_vcf_ids.append(vcf_id)
                    input_tbi_ids.append(tbi_id)
                elif not (vcf_id == None and tbi_id == None):
                    raise AssertionError

        index_prev_job = construct_job
        if haplo_extraction:
            haplo_index_job = construct_job.addFollowOnJobFn(run_make_haplo_indexes, context, input_vcf_ids, input_tbi_ids, vcf_names, joined_vg_ids, joined_vg_names, output_name_base, regions, haplo_extraction_sample)
            haplo_xg_ids = haplo_index_job.rv(0)
            gbwt_ids = haplo_index_job.rv(1)
            if name == 'sample-graph':
                sample_name_base = output_name_base.replace('_withref', '')
                sample_merge_output_name = merge_output_name.replace('_withref', '') if merge_output_name else None
                region_names = [ r.replace('_withref', '') for r in region_names ]
                sample_job = haplo_index_job.addFollowOnJobFn(run_make_sample_graphs, context, joined_vg_ids, joined_vg_names, haplo_xg_ids, sample_name_base, regions, haplo_extraction_sample, gbwt_ids)
                join_job = sample_job.addFollowOnJobFn(run_join_graphs, context, sample_job.rv(), False, region_names, name, sample_merge_output_name)
                if len(regions) > 1 and xg_index:
                    construct_job.addFollowOnJobFn(run_indexing, context, joined_vg_ids, joined_vg_names, output_name_base, chroms, [], [], skip_xg=not xg_index, skip_gcsa=True, skip_id_ranges=True, skip_snarls=True)
                index_prev_job = join_job
                joined_vg_ids = join_job.rv('joined')
                joined_vg_names = [ n.replace('_withref', '') for n in joined_vg_names ]
                if sample_merge_output_name:
                    single_vg_id = join_job.rv('merged')
                    single_vg_name = remove_ext(sample_merge_output_name, '.vg') + '.vg'
                else:
                    single_vg_id = None
                    single_vg_name = None
                output_name_base = sample_name_base
            elif name == 'haplo':
                assert haplo_extraction_sample is not None
                haplo_job = haplo_index_job.addFollowOnJobFn(run_make_haplo_graphs, context, joined_vg_ids, joined_vg_names, haplo_xg_ids, output_name_base, regions, haplo_extraction_sample, haplotypes, gbwt_ids)
                for haplotype in haplotypes:
                    haplo_xg_job = haplo_job.addFollowOnJobFn(run_xg_indexing, context, haplo_job.rv(haplotype), joined_vg_names, output_name_base + ('_thread_{}').format(haplotype), cores=context.config.xg_index_cores, memory=context.config.xg_index_mem, disk=context.config.xg_index_disk)

        skip_gcsa = not gcsa_index or name == 'haplo'
        skip_snarls = not snarls_index or haplo_extraction
        make_gbwt = gbwt_index and not haplo_extraction
        indexing_job = index_prev_job.addFollowOnJobFn(run_indexing, context, joined_vg_ids, joined_vg_names, output_name_base, chroms, input_vcf_ids if make_gbwt else [], input_tbi_ids if make_gbwt else [], node_mapping_id=mapping_id, skip_xg=not xg_index, skip_gcsa=skip_gcsa, skip_id_ranges=not id_ranges_index, skip_snarls=skip_snarls, make_gbwt=make_gbwt, gbwt_prune=gbwt_prune and make_gbwt, gbwt_regions=gbwt_regions)
        indexes = indexing_job.rv()
        output.append((joined_vg_ids, joined_vg_names, indexes))

    return output


def run_construct_genome_graph(job, context, fasta_ids, fasta_names, vcf_ids, vcf_names, tbi_ids, max_node_size, alt_paths, flat_alts, regions, region_names, sort_ids, join_ids, name, merge_output_name, normalize):
    """
    
    Construct graphs from one or more FASTA files and zero or more VCFs.
    
    If regions and region_names are set, constructs only for the specified
    regions, and constructs one graph per region. Otherwise, constructs one
    graph overall on a single default region.
    
    If merge_output_name is set, merges all constructed graphs together and
    outputs them under that name. Otherwise, outputs each graph constructed
    under its own name, but in a unified ID space.
    
    Returns a dict containing:
    
    'joined': a list of the unmerged, id-joined graph file IDs for each region.
    
    'merged': the merged graph file ID, if merge_output_name is set, or the
    only graph, if there is only one. None otherwise.
    
    'mapping': the file ID of the .mapping file produced by `vg ids --join`, if
    id joining had to happen. None otherwise.
    
    """
    child_job = Job()
    job.addChild(child_job)
    work_dir = job.fileStore.getLocalTempDir()
    if not regions:
        regions, region_names = [
         None], ['genome']
    region_graph_ids = []
    for i, (region, region_name) in enumerate(zip(regions, region_names)):
        if not vcf_ids or len(vcf_ids) > 1 and i >= len(vcf_ids):
            vcf_id = None
            tbi_id = None
            vcf_name = None
        elif len(vcf_ids) == 1:
            vcf_id = vcf_ids[0]
            tbi_id = tbi_ids[0]
            vcf_name = vcf_names[0]
        else:
            vcf_id = vcf_ids[i]
            tbi_id = tbi_ids[i]
            vcf_name = vcf_names[i]
        fasta_id = fasta_ids[0] if len(fasta_ids) == 1 else fasta_ids[i]
        fasta_name = fasta_names[0] if len(fasta_names) == 1 else fasta_names[i]
        region_graph_ids.append(child_job.addChildJobFn(run_construct_region_graph, context, fasta_id, fasta_name, vcf_id, vcf_name, tbi_id, region, region_name, max_node_size, alt_paths, flat_alts, is_chrom=not region or ':' not in region, sort_ids=sort_ids, normalize=normalize, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk).rv())

    return child_job.addFollowOnJobFn(run_join_graphs, context, region_graph_ids, join_ids, region_names, name, merge_output_name).rv()


def run_join_graphs(job, context, region_graph_ids, join_ids, region_names, name, merge_output_name=None):
    """
    Join the ids of some graphs. If a merge_output_name is given, cat them all
    together as well.
    
    Saves the unmerged, id-joined graphs, or the single merged graph if its
    name is given, to the output store. Also saves the node mapping file,
    produced from the `vg ids --join` call, to the output store.
    
    Skips doing any joining or merging if there is only one input graph.
    
    If join_ids is false, assumes the input graphs are already id-joined, and
    passes them through, merging if requested.
    
    Returns a dict containing:
    
    'joined': a list of the unmerged, id-joined graph file IDs (or the input
    graph(s) re-uploaded as output files if no joining occurred)
    
    'merged': the merged graph file ID, if merging occurred, or the only input
    graph ID, if there was only one. None otherwise.
    
    'mapping': the file ID of the .mapping file produced by `vg ids --join`, if
    run. None otherwise.
    
    """
    work_dir = job.fileStore.getLocalTempDir()
    region_files = []
    for region_graph_id, region_name in zip(region_graph_ids, region_names):
        region_file = ('{}.vg').format(region_name)
        job.fileStore.readGlobalFile(region_graph_id, os.path.join(work_dir, region_file), mutable=True)
        region_files.append(region_file)

    if merge_output_name:
        merge_output_name = remove_ext(merge_output_name, '.vg') + '.vg'
    to_return = {'joined': [], 'merged': None, 
       'mapping': None}
    if join_ids and len(region_files) != 1:
        mapping_file = merge_output_name[:-3] if merge_output_name else name
        mapping_file = os.path.join(work_dir, mapping_file + '.mapping')
        cmd = [
         'vg', 'ids', '--join', '--mapping', os.path.basename(mapping_file)] + region_files
        context.runner.call(job, cmd, work_dir=work_dir)
        to_return['mapping'] = context.write_output_file(job, mapping_file)
    if merge_output_name is not None:
        assert merge_output_name[:-3] not in region_names
        with open(os.path.join(work_dir, merge_output_name), 'w') as (merge_file):
            for region_file in region_files:
                with open(os.path.join(work_dir, region_file)) as (cf):
                    shutil.copyfileobj(cf, merge_file)

        to_return['merged'] = context.write_output_file(job, os.path.join(work_dir, merge_output_name))
        if join_ids and len(region_files) != 1:
            to_return['joined'] = [ context.write_intermediate_file(job, os.path.join(work_dir, f)) for f in region_files ]
        else:
            to_return['joined'] = region_graph_ids
    else:
        for region_file in region_files:
            to_return['joined'] = [ context.write_output_file(job, os.path.join(work_dir, f)) for f in region_files ]

    return to_return


def run_construct_region_graph(job, context, fasta_id, fasta_name, vcf_id, vcf_name, tbi_id, region, region_name, max_node_size, alt_paths, flat_alts, is_chrom=False, sort_ids=True, normalize=False, validate=False):
    """
    Construct a graph from the vcf for a given region and return its file id.
    
    If is_chrom is set, pass along that fact to the constructor so it doesn't
    try to pass a region out of the chromosome name.
    
    If sort_ids is set (the default), do a sort pass after construction to make
    sure the IDs come in topological order.
    
    If normalize is set, try to normalize the graph and merge splits that
    produce identical sequences.
    
    If validate is true, subject the graph to a `vg validate` pass after
    construct. This is off by default because vg currently does internal
    validation during construction.
    """
    work_dir = job.fileStore.getLocalTempDir()
    fasta_file = os.path.join(work_dir, os.path.basename(fasta_name))
    job.fileStore.readGlobalFile(fasta_id, fasta_file)
    if vcf_id:
        vcf_file = os.path.join(work_dir, os.path.basename(vcf_name))
        job.fileStore.readGlobalFile(vcf_id, vcf_file)
        job.fileStore.readGlobalFile(tbi_id, vcf_file + '.tbi')
    cmd = ['vg', 'construct', '--reference', os.path.basename(fasta_file)]
    if vcf_id:
        cmd += ['--vcf', os.path.basename(vcf_file)]
    if region:
        cmd += ['--region', region]
        if is_chrom:
            cmd += ['--region-is-chrom']
    if max_node_size:
        cmd += ['--node-max', max_node_size]
    if alt_paths:
        cmd += ['--alt-paths']
    if flat_alts:
        cmd += ['--flat-alts']
    if job.cores:
        cmd += ['--threads', job.cores]
    if normalize or sort_ids:
        cmd = [
         cmd]
    if normalize:
        cmd.append(['vg', 'mod', '--normalize', '-'])
        cmd.append(['vg', 'mod', '--chop', str(max_node_size), '-'])
    if sort_ids:
        cmd.append(['vg', 'ids', '--sort', '-'])
    vg_path = os.path.join(work_dir, region_name)
    with open(vg_path, 'w') as (vg_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=vg_file)
    if validate:
        context.runner.call(job, ['vg', 'validate', os.path.basename(vg_path)], work_dir=work_dir)
    return context.write_intermediate_file(job, vg_path)


def run_filter_vcf_samples(job, context, vcf_id, vcf_name, tbi_id, samples):
    """ 
    
    Use vcflib to remove all variants specifc to a set of samples.
    Keep all the sample data in the VCF except that for the sample that was removed.
    
    """
    if not samples:
        return (
         vcf_id, tbi_id)
    work_dir = job.fileStore.getLocalTempDir()
    vcf_file = os.path.join(work_dir, os.path.basename(vcf_name))
    job.fileStore.readGlobalFile(vcf_id, vcf_file)
    job.fileStore.readGlobalFile(tbi_id, vcf_file + '.tbi')
    vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
    filter_vcf_name = ('{}_filter.vcf.gz').format(vcf_base)
    private_vcf_name = ('{}_private.vcf.gz').format(vcf_base)
    cmd = [
     'bcftools', 'view', os.path.basename(vcf_file), '--private',
     '--samples', (',').join(samples), '--force-samples', '--output-type', 'z']
    with open(os.path.join(work_dir, private_vcf_name), 'w') as (out_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
    context.runner.call(job, ['tabix', '-f', '-p', 'vcf', private_vcf_name], work_dir=work_dir)
    cmd = [
     [
      'bcftools', 'isec', '--complement', os.path.basename(vcf_file), os.path.basename(private_vcf_name),
      '--write', '1'],
     [
      'bcftools', 'view', '-', '--samples', '^' + (',').join(samples),
      '--force-samples', '--output-type', 'z']]
    with open(os.path.join(work_dir, filter_vcf_name), 'w') as (out_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
    out_vcf_id = context.write_output_file(job, os.path.join(work_dir, filter_vcf_name))
    context.runner.call(job, ['tabix', '-f', '-p', 'vcf', filter_vcf_name], work_dir=work_dir)
    out_tbi_id = context.write_output_file(job, os.path.join(work_dir, filter_vcf_name) + '.tbi')
    return (
     out_vcf_id, out_tbi_id)


def run_make_control_vcfs(job, context, vcf_id, vcf_name, tbi_id, sample, pos_only=False, unphased_handling=None):
    """ make a positive and negative control vcf 
    The positive control has only variants in the sample, the negative
    control has only variants not in the sample
    """
    assert sample is not None
    work_dir = job.fileStore.getLocalTempDir()
    vcf_file = os.path.join(work_dir, os.path.basename(vcf_name))
    job.fileStore.readGlobalFile(vcf_id, vcf_file)
    job.fileStore.readGlobalFile(tbi_id, vcf_file + '.tbi')
    cmd = [
     'bcftools', 'query', '--list-samples', os.path.basename(vcf_file)]
    found_samples = context.runner.call(job, cmd, work_dir=work_dir, check_output=True)
    found_sample = sample in found_samples.strip().split('\n')
    cmd = [
     [
      'bcftools', 'view', os.path.basename(vcf_file), '--samples', sample]]
    if found_sample:
        if unphased_handling == 'skip':
            cmd[0] += ['--phased']
        gfilter = 'GT="0" || GT="0|0" || GT="0/0"'
        gfilter += ' || GT="." || GT=".|." || GT="./."'
        gfilter += ' || GT=".|0" || GT="0/."'
        gfilter += ' || GT="0|." || GT="./0"'
        if unphased_handling == 'arbitrary':
            cmd.append(['sed', '-e', 's/\\([0-9,.]\\)\\/\\([0-9,.]\\)/\\1\\|\\2/g'])
        cmd.append(['bcftools', 'view', '-', '--output-type', 'z', '--exclude', gfilter])
    else:
        cmd[0] += ['--force-samples', '--header-only', '--output-type', 'z']
    out_pos_name = remove_ext(remove_ext(os.path.basename(vcf_name), '.gz'), '.vcf')
    out_neg_name = out_pos_name + ('_minus_{}.vcf.gz').format(sample)
    out_pos_name += ('_{}.vcf.gz').format(sample)
    with open(os.path.join(work_dir, out_pos_name), 'w') as (out_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
    context.runner.call(job, ['tabix', '--force', '--preset', 'vcf', out_pos_name], work_dir=work_dir)
    pos_control_vcf_id = context.write_output_file(job, os.path.join(work_dir, out_pos_name))
    pos_control_tbi_id = context.write_output_file(job, os.path.join(work_dir, out_pos_name + '.tbi'))
    if pos_only:
        return (pos_control_vcf_id, pos_control_tbi_id, None, None)
    else:
        cmd = [
         'bcftools', 'isec', os.path.basename(vcf_file), out_pos_name, '-p', 'isec', '-O', 'z']
        context.runner.call(job, cmd, work_dir=work_dir)
        context.runner.call(job, ['tabix', '--force', '--preset', 'vcf', 'isec/0000.vcf.gz'], work_dir=work_dir)
        neg_control_vcf_id = context.write_output_file(job, os.path.join(work_dir, 'isec', '0000.vcf.gz'), out_store_path=out_neg_name)
        neg_control_tbi_id = context.write_output_file(job, os.path.join(work_dir, 'isec', '0000.vcf.gz.tbi'), out_store_path=out_neg_name + '.tbi')
        return (
         pos_control_vcf_id, pos_control_tbi_id, neg_control_vcf_id, neg_control_tbi_id)


def run_min_allele_filter_vcf_samples(job, context, vcf_id, vcf_name, tbi_id, min_af):
    """
    filter a vcf by allele frequency using bcftools --min-af
    """
    if not min_af:
        return (vcf_id, tbi_id)
    work_dir = job.fileStore.getLocalTempDir()
    vcf_file = os.path.join(work_dir, os.path.basename(vcf_name))
    job.fileStore.readGlobalFile(vcf_id, vcf_file)
    job.fileStore.readGlobalFile(tbi_id, vcf_file + '.tbi')
    vcf_base = os.path.basename(remove_ext(remove_ext(vcf_name, '.gz'), '.vcf'))
    af_vcf_name = ('{}_minaf_{}.vcf.gz').format(vcf_base, min_af)
    cmd = [
     'bcftools', 'view', '--min-af', min_af, '-O', 'z', os.path.basename(vcf_file)]
    with open(os.path.join(work_dir, af_vcf_name), 'w') as (out_file):
        context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
    out_vcf_id = context.write_output_file(job, os.path.join(work_dir, af_vcf_name))
    context.runner.call(job, ['tabix', '-f', '-p', 'vcf', af_vcf_name], work_dir=work_dir)
    out_tbi_id = context.write_output_file(job, os.path.join(work_dir, af_vcf_name) + '.tbi')
    return (
     out_vcf_id, out_tbi_id)


def run_make_haplo_indexes(job, context, vcf_ids, tbi_ids, vcf_names, vg_ids, vg_names, output_name, regions, sample):
    """
    return xg/gbwt for each chromosome for extracting haplotype thread graphs
    (to simulate from) or sample graphs (as positive control)
    """
    assert sample is not None
    chroms = [ region[0:region.find(':')] if ':' in region else region for region in regions ]
    vcf_names = [ v for v in vcf_names if v is not None ]
    logger.debug(('Making gbwt for {} vgs, {} chroms, {} vcfs, {} tbis, and {} vcf names').format(len(vg_ids), len(chroms), len(vcf_ids), len(tbi_ids), len(vcf_names)))
    assert len(vg_ids) == len(regions)
    assert len(vcf_ids) == 1 or len(vcf_ids) <= len(regions)
    assert len(tbi_ids) == len(vcf_ids)
    assert len(vcf_names) == len(vcf_ids)
    logger.info(('Making gbwt for chromosomes {}').format(chroms))
    xg_ids = []
    gbwt_ids = []
    for i, (vg_id, vg_name, region) in enumerate(zip(vg_ids, vg_names, chroms)):
        if len(vcf_names) == 1:
            vcf_name = vcf_names[0]
            vcf_id = vcf_ids[0]
            tbi_id = tbi_ids[0]
        elif i < len(vcf_names):
            vcf_name = vcf_names[i]
            vcf_id = vcf_ids[i]
            tbi_id = tbi_ids[i]
        else:
            vcf_name = None
            vcf_id = None
            tbi_id = None
        xg_name = remove_ext(vg_name, '.vg')
        xg_job = job.addChildJobFn(run_xg_indexing, context, [vg_id], [vg_name], xg_name, vcf_id, tbi_id, make_gbwt=True, cores=context.config.xg_index_cores, memory=context.config.xg_index_mem, disk=context.config.xg_index_disk)
        xg_ids.append(xg_job.rv(0))
        gbwt_ids.append(xg_job.rv(1))

    return (xg_ids, gbwt_ids)


def run_make_haplo_graphs(job, context, vg_ids, vg_names, xg_ids, output_name, regions, sample, haplotypes, gbwt_ids):
    """
    Make some haplotype graphs for threads in a gbwt. regions must be defined
    since we use the chromosome name to get the threads. Also, gbwt_ids must be
    specified (one genome gbwt or one per region).
    
    Returns a list of haplotypes, where each haplotype is a list of vg graphs subset to that haplotype.
    """
    assert sample is not None
    thread_vg_ids = []
    for h in haplotypes:
        thread_vg_ids.append([])

    chroms = [ region[0:region.find(':')] if ':' in region else region for region in regions ]
    assert len(vg_ids) == len(regions)
    logger.info(('Making haplo graphs for chromosomes {}').format(chroms))
    for i, (vg_id, vg_name, region, xg_id) in enumerate(zip(vg_ids, vg_names, chroms, xg_ids)):
        assert not gbwt_ids or len(gbwt_ids) in [1, len(xg_ids)]
        gbwt_id = None if not gbwt_ids else (gbwt_ids[0] if len(gbwt_ids) == 1 else gbwt_ids[i])
        hap_job = job.addChildJobFn(run_make_haplo_thread_graphs, context, vg_id, vg_name, output_name, [region], xg_id, sample, haplotypes, gbwt_id, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
        for j in range(len(haplotypes)):
            thread_vg_ids[j].append(hap_job.rv(j))

    return thread_vg_ids


def run_make_haplo_thread_graphs(job, context, vg_id, vg_name, output_name, chroms, xg_id, sample, haplotypes, gbwt_id):
    """
    make some haplotype graphs for threads in a gbwt
    
    If there are no haplotypes in the gbwt, passes through the portion of the input graph covered by paths.
    """
    work_dir = job.fileStore.getLocalTempDir()
    xg_path = os.path.join(work_dir, vg_name[:-3] + '.xg')
    job.fileStore.readGlobalFile(xg_id, xg_path)
    vg_path = os.path.join(work_dir, vg_name)
    job.fileStore.readGlobalFile(vg_id, vg_path)
    if gbwt_id:
        gbwt_path = os.path.join(work_dir, vg_name[:-3] + '.gbwt')
        job.fileStore.readGlobalFile(gbwt_id, gbwt_path)
        thread_count = int(context.runner.call(job, [
         [
          'vg', 'paths', '--threads', '--list', '--gbwt', os.path.basename(gbwt_path), '-x', os.path.basename(xg_path)],
         [
          'wc', '-l']], work_dir=work_dir, check_output=True))
    else:
        thread_count = 0
    thread_vg_ids = []
    for hap in haplotypes:
        assert sample is not None
        try:
            tag = ('_{}').format(chroms[0]) if len(chroms) == 1 else ''
            if thread_count == 0:
                vg_with_thread_as_path_path = vg_path
            else:
                vg_with_thread_as_path_path = os.path.join(work_dir, ('{}{}_thread_{}_merge.vg').format(output_name, tag, hap))
                logger.info(('Creating thread graph {}').format(vg_with_thread_as_path_path))
                with open(vg_with_thread_as_path_path, 'w') as (thread_only_file):
                    cmd = ['vg', 'mod', '-D', os.path.basename(vg_path)]
                    context.runner.call(job, cmd, work_dir=work_dir, outfile=thread_only_file)
                    cmd = [
                     'vg', 'paths', '--gbwt', os.path.basename(gbwt_path), '--extract-vg', '-x', os.path.basename(xg_path)]
                    for chrom in chroms:
                        cmd += ['-q', ('_thread_{}_{}_{}').format(sample, chrom, hap)]

                    context.runner.call(job, cmd, work_dir=work_dir, outfile=thread_only_file)
            vg_trimmed_path = os.path.join(work_dir, ('{}{}_thread_{}.vg').format(output_name, tag, hap))
            logger.info(('Creating trimmed thread graph {}').format(vg_trimmed_path))
            with open(vg_trimmed_path, 'w') as (trimmed_file):
                cmd = [['vg', 'mod', '-N', os.path.basename(vg_with_thread_as_path_path)]]
                filter_cmd = [
                 'vg', 'mod', '-']
                for chrom in chroms:
                    filter_cmd += ['-r', chrom]

                cmd.append(filter_cmd)
                context.runner.call(job, cmd, work_dir=work_dir, outfile=trimmed_file)
            thread_vg_ids.append(context.write_output_file(job, vg_trimmed_path))
        except:
            logging.error('Thread extraction failed. Dumping files.')
            context.write_output_file(job, vg_path)
            context.write_output_file(job, xg_path)
            if gbwt_id:
                context.write_output_file(job, gbwt_path)
            raise

    logger.info(('Got {} thread file IDs').format(len(thread_vg_ids)))
    return thread_vg_ids


def run_make_sample_graphs(job, context, vg_ids, vg_names, xg_ids, output_name, regions, sample, gbwt_ids):
    """
    Make some sample graphs for threads in a gbwt. regions must be defined
    since we use the chromosome name to get the threads. Also, gbwt_ids must be
    specified (one genome gbwt or one per region).
    """
    assert sample is not None
    sample_vg_ids = []
    chroms = [ region[0:region.find(':')] if ':' in region else region for region in regions ]
    assert len(vg_ids) == len(regions)
    logger.info(('Making sample graphs for chromosomes {}').format(chroms))
    for i, (vg_id, vg_name, region, xg_id) in enumerate(zip(vg_ids, vg_names, chroms, xg_ids)):
        assert not gbwt_ids or len(gbwt_ids) in [1, len(xg_ids)]
        gbwt_id = gbwt_ids[0] if len(gbwt_ids) == 1 else gbwt_ids[i]
        hap_job = job.addChildJobFn(run_make_sample_region_graph, context, vg_id, vg_name, output_name, region, xg_id, sample, [0, 1], gbwt_id, cores=context.config.construct_cores, memory=context.config.construct_mem, disk=context.config.construct_disk)
        sample_vg_ids.append(hap_job.rv())

    return sample_vg_ids


def run_make_sample_region_graph(job, context, vg_id, vg_name, output_name, chrom, xg_id, sample, haplotypes, gbwt_id, leave_thread_paths=True, validate=True):
    """
    make a sample graph using the gbwt.
    
    Extract the subgraph visited by threads for the requested sample, if it is nonempty.
    Otherwise (for cases like chrM where there are no variant calls and no threads) pass through
    the primary path of the graph.
    
    If validate is True (the default), makes sure the final graph passes
    `vg validate` before sending it on.
    """
    assert sample is not None
    work_dir = job.fileStore.getLocalTempDir()
    xg_path = os.path.join(work_dir, vg_name[:-3] + '.xg')
    job.fileStore.readGlobalFile(xg_id, xg_path)
    vg_path = os.path.join(work_dir, vg_name)
    job.fileStore.readGlobalFile(vg_id, vg_path)
    gbwt_path = os.path.join(work_dir, vg_name[:-3] + '.gbwt')
    if gbwt_id:
        job.fileStore.readGlobalFile(gbwt_id, gbwt_path)
    assert gbwt_id
    thread_count = int(context.runner.call(job, [
     [
      'vg', 'paths', '--threads', '--list', '--gbwt', os.path.basename(gbwt_path), '-x', os.path.basename(xg_path)],
     [
      'wc', '-l']], work_dir=work_dir, check_output=True))
    if thread_count == 0:
        extract_graph_path = vg_path
    else:
        extract_graph_path = os.path.join(work_dir, ('{}_{}_extract.vg').format(output_name, chrom))
        logger.info(('Creating sample extraction graph {}').format(extract_graph_path))
        with open(extract_graph_path, 'w') as (extract_graph_file):
            cmd = ['vg', 'mod', '-D', os.path.basename(vg_path)]
            context.runner.call(job, cmd, work_dir=work_dir, outfile=extract_graph_file)
            for hap in haplotypes:
                if gbwt_id:
                    cmd = [
                     'vg', 'paths', '--gbwt', os.path.basename(gbwt_path), '--extract-vg']
                else:
                    cmd = [
                     'vg', 'find']
                cmd += ['-x', os.path.basename(xg_path)]
                cmd += ['-q', ('_thread_{}_{}_{}').format(sample, chrom, hap)]
                context.runner.call(job, cmd, work_dir=work_dir, outfile=extract_graph_file)

    sample_graph_path = os.path.join(work_dir, ('{}_{}.vg').format(output_name, chrom))
    logger.info(('Creating sample graph {}').format(sample_graph_path))
    with open(sample_graph_path, 'w') as (sample_graph_file):
        cmd = [['vg', 'mod', '-N', os.path.basename(extract_graph_path)]]
        if not leave_thread_paths:
            cmd.append(['vg', 'mod', '-', '-D'])
        context.runner.call(job, cmd, work_dir=work_dir, outfile=sample_graph_file)
    if validate:
        context.runner.call(job, ['vg', 'validate', os.path.basename(sample_graph_path)], work_dir=work_dir)
    sample_vg_id = context.write_intermediate_file(job, sample_graph_path)
    return sample_vg_id


def construct_main(context, options):
    """
    Wrapper for vg constructing. 
    """
    validate_construct_options(options)
    run_time_pipeline = None
    start_time_pipeline = timeit.default_timer()
    filter_samples = []
    if options.filter_samples:
        filter_samples += options.filter_samples
    if options.filter_ceph:
        filter_samples += CEPH_SAMPLES
    filter_samples = list(set(filter_samples))
    with context.get_toil(options.jobStore) as (toil):
        if not toil.options.restart:
            start_time = timeit.default_timer()
            logger.info('Importing input files into Toil')
            inputFastaFileIDs = [ toil.importFile(fasta) for fasta in options.fasta ]
            inputFastaNames = [ os.path.basename(fasta) for fasta in options.fasta ]
            inputVCFFileIDs = []
            inputVCFNames = []
            inputTBIFileIDs = []
            if options.vcf:
                for vcf in options.vcf:
                    inputVCFFileIDs.append(toil.importFile(vcf))
                    inputVCFNames.append(os.path.basename(vcf))
                    inputTBIFileIDs.append(toil.importFile(vcf + '.tbi'))

            inputBWAFastaID = None
            if options.bwa_reference:
                inputBWAFastaID = toil.importFile(options.bwa_reference)
            end_time = timeit.default_timer()
            logger.info(('Imported input files into Toil in {} seconds').format(end_time - start_time))
            haplo_extraction_sample = options.haplo_sample if options.haplo_sample else options.sample_graph
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, sys.argv)
            for i, fasta in enumerate(options.fasta):
                if fasta.endswith('.gz'):
                    inputFastaFileIDs[i] = init_job.addChildJobFn(run_unzip_fasta, context, inputFastaFileIDs[i], os.path.basename(fasta)).rv()
                    inputFastaNames[i] = inputFastaNames[i][:-3]

            if options.fasta_regions:
                scrape_fasta_job = init_job.addFollowOnJobFn(run_scan_fasta_sequence_names, context, inputFastaFileIDs[0], inputFastaNames[0], options.regions)
                cur_job = scrape_fasta_job
                regions = scrape_fasta_job.rv()
            else:
                cur_job = init_job
                regions = options.regions
            vcf_job = cur_job.addFollowOnJobFn(run_generate_input_vcfs, context, inputVCFFileIDs, inputVCFNames, inputTBIFileIDs, regions, options.out_name, do_primary=options.primary, do_pan=options.pangenome, pos_control_sample=options.pos_control, neg_control_sample=options.neg_control, sample_graph=options.sample_graph, handle_unphased=options.handle_unphased, haplo_sample=options.haplo_sample, filter_samples=filter_samples, min_afs=options.min_af)
            vcf_job.addFollowOnJobFn(run_construct_all, context, inputFastaFileIDs, inputFastaNames, vcf_job.rv(), options.max_node_size, options.alt_paths, options.flat_alts, regions, merge_graphs=options.merge_graphs, sort_ids=True, join_ids=True, gcsa_index=options.gcsa_index or options.all_index, xg_index=options.xg_index or options.all_index, gbwt_index=options.gbwt_index or options.all_index, id_ranges_index=options.id_ranges_index or options.all_index, snarls_index=options.snarls_index or options.all_index, haplo_extraction_sample=haplo_extraction_sample, gbwt_prune=options.gbwt_prune, normalize=options.normalize)
            if inputBWAFastaID:
                init_job.addFollowOnJobFn(run_bwa_index, context, inputBWAFastaID, copy_fasta=True, cores=context.config.bwa_index_cores, memory=context.config.bwa_index_mem, disk=context.config.bwa_index_disk)
            toil.start(init_job)
        else:
            toil.restart()
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
    print(('All jobs completed successfully. Pipeline took {} seconds.').format(run_time_pipeline))
    return