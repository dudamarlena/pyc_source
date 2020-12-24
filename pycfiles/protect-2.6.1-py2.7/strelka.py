# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/mutation_calling/strelka.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import print_function
from math import ceil
from protect.common import docker_call, docker_path, get_files_from_filestore, untargz
from protect.mutation_calling.common import sample_chromosomes, unmerge
from toil.job import PromisedRequirement
import os

def strelka_disk(tumor_bam, normal_bam, fasta):
    return int(ceil(tumor_bam.size) + ceil(normal_bam.size) + 6 * ceil(fasta.size))


def run_strelka_with_merge(job, tumor_bam, normal_bam, univ_options, strelka_options):
    """
    A wrapper for the the entire strelka sub-graph.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict strelka_options: Options specific to strelka
    :return: fsID to the merged strelka calls
    :rtype: toil.fileStore.FileID
    """
    spawn = job.wrapJobFn(run_strelka, tumor_bam, normal_bam, univ_options, strelka_options, split=False).encapsulate()
    job.addChild(spawn)
    return spawn.rv()


def run_strelka(job, tumor_bam, normal_bam, univ_options, strelka_options, split=True):
    """
    Run the strelka subgraph on the DNA bams.  Optionally split the results into per-chromosome
    vcfs.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict strelka_options: Options specific to strelka
    :param bool split: Should the results be split into perchrom vcfs?
    :return: Either the fsID to the genome-level vcf or a dict of results from running strelka
             on every chromosome
             perchrom_strelka:
                 |- 'chr1':
                 |      |-'snvs': fsID
                 |      +-'indels': fsID
                 |- 'chr2':
                 |      |-'snvs': fsID
                 |      +-'indels': fsID
                 |-...
                 |
                 +- 'chrM':
                        |-'snvs': fsID
                        +-'indels': fsID
    :rtype: toil.fileStore.FileID|dict
    """
    if strelka_options['chromosomes']:
        chromosomes = strelka_options['chromosomes']
    else:
        chromosomes = sample_chromosomes(job, strelka_options['genome_fai'])
    num_cores = min(len(chromosomes), univ_options['max_cores'])
    strelka = job.wrapJobFn(run_strelka_full, tumor_bam, normal_bam, univ_options, strelka_options, disk=PromisedRequirement(strelka_disk, tumor_bam['tumor_dna_fix_pg_sorted.bam'], normal_bam['normal_dna_fix_pg_sorted.bam'], strelka_options['genome_fasta']), memory='6G', cores=num_cores)
    job.addChild(strelka)
    if split:
        unmerge_strelka = job.wrapJobFn(wrap_unmerge, strelka.rv(), chromosomes, strelka_options, univ_options).encapsulate()
        strelka.addChild(unmerge_strelka)
        return unmerge_strelka.rv()
    else:
        return strelka.rv()


def run_strelka_full(job, tumor_bam, normal_bam, univ_options, strelka_options):
    """
    Run strelka on the DNA bams.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict strelka_options: Options specific to strelka
    :return: Dict of fsIDs snv and indel prediction files
             output_dict:
                 |-'snvs': fsID
                 +-'indels': fsID
    :rtype: dict
    """
    work_dir = os.getcwd()
    input_files = {'tumor.bam': tumor_bam['tumor_dna_fix_pg_sorted.bam'], 
       'tumor.bam.bai': tumor_bam['tumor_dna_fix_pg_sorted.bam.bai'], 
       'normal.bam': normal_bam['normal_dna_fix_pg_sorted.bam'], 
       'normal.bam.bai': normal_bam['normal_dna_fix_pg_sorted.bam.bai'], 
       'genome.fa.tar.gz': strelka_options['genome_fasta'], 
       'genome.fa.fai.tar.gz': strelka_options['genome_fai'], 
       'config.ini.tar.gz': strelka_options['config_file']}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    for key in ('genome.fa', 'genome.fa.fai', 'config.ini'):
        input_files[key] = untargz(input_files[(key + '.tar.gz')], work_dir)

    input_files = {key:docker_path(path) for key, path in input_files.items()}
    parameters = [input_files['config.ini'],
     input_files['tumor.bam'],
     input_files['normal.bam'],
     input_files['genome.fa'],
     str(job.cores)]
    docker_call(tool='strelka', tool_parameters=parameters, work_dir=work_dir, dockerhub=univ_options['dockerhub'], tool_version=strelka_options['version'])
    output_dict = {}
    for mutation_type in ['snvs', 'indels']:
        output_dict[mutation_type] = job.fileStore.writeGlobalFile(os.path.join(work_dir, 'strelka_out', 'results', 'passed.somatic.' + mutation_type + '.vcf'))

    job.fileStore.logToMaster('Ran strelka on %s successfully' % univ_options['patient'])
    return output_dict


def process_strelka_vcf(job, strelka_vcf, work_dir, univ_options):
    """
    Process the strelka vcf for accepted calls. Since the calls are pre-filtered, we just obtain the
    file from the file store and return it.

    :param toil.fileStore.FileID strelka_vcf: fsID for a strelka generated chromosome vcf
    :param str work_dir: Working directory
    :param dict univ_options: Dict of universal options used by almost all tools
    :return: Path to the processed vcf
    :rtype: str
    """
    return job.fileStore.readGlobalFile(strelka_vcf)


def wrap_unmerge(job, strelka_out, chromosomes, strelka_options, univ_options):
    """
    A wwrapper to unmerge the strelka snvs and indels

    :param dict strelka_out: Results from run_strelka
    :param list chromosomes: List of chromosomes to retain
    :param dict strelka_options: Options specific to strelka
    :param dict univ_options: Dict of universal options used by almost all tools
    :return: Dict of dicts containing the fsIDs for the per-chromosome snv and indel calls
             output:
               |- 'snvs':
               |      |- 'chr1': fsID
               |      |- 'chr2': fsID
               |      |- ...
               |      +- 'chrM': fsID
               +- 'indels':
                      |- 'chr1': fsID
                      |- 'chr2': fsID
                      |- ...
                      +- 'chrM': fsID
    :rtype: dict
    """
    return {'snvs': job.addChildJobFn(unmerge, strelka_out['snvs'], 'strelka/snv', chromosomes, strelka_options, univ_options).rv(), 
       'indels': job.addChildJobFn(unmerge, strelka_out['indels'], 'strelka/indel', chromosomes, strelka_options, univ_options).rv()}