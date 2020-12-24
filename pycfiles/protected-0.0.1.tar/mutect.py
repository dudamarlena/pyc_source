# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/mutation_calling/mutect.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import print_function
from collections import defaultdict
from math import ceil
from protect.common import docker_call, docker_path, export_results, get_files_from_filestore, gunzip, untargz
from protect.mutation_calling.common import sample_chromosomes, merge_perchrom_vcfs
from toil.job import PromisedRequirement
import os

def mutect_disk(tumor_bam, normal_bam, fasta, dbsnp, cosmic):
    return int(ceil(tumor_bam.size) + ceil(normal_bam.size) + 4 * ceil(fasta.size) + 10 * ceil(dbsnp.size) + 2 * ceil(cosmic.size))


def run_mutect_with_merge(job, tumor_bam, normal_bam, univ_options, mutect_options):
    """
    A wrapper for the the entire MuTect sub-graph.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict mutect_options: Options specific to MuTect
    :return: fsID to the merged MuTect calls
    :rtype: toil.fileStore.FileID
    """
    spawn = job.wrapJobFn(run_mutect, tumor_bam, normal_bam, univ_options, mutect_options).encapsulate()
    merge = job.wrapJobFn(merge_perchrom_vcfs, spawn.rv())
    job.addChild(spawn)
    spawn.addChild(merge)
    return merge.rv()


def run_mutect(job, tumor_bam, normal_bam, univ_options, mutect_options):
    """
    Spawn a MuTect job for each chromosome on the DNA bams.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict mutect_options: Options specific to MuTect
    :return: Dict of results from running MuTect on every chromosome
             perchrom_mutect:
                 |- 'chr1': fsID
                 |- 'chr2' fsID
                 |
                 |-...
                 |
                 +- 'chrM': fsID
    :rtype: dict
    """
    if mutect_options['chromosomes']:
        chromosomes = mutect_options['chromosomes']
    else:
        chromosomes = sample_chromosomes(job, mutect_options['genome_fai'])
    perchrom_mutect = defaultdict()
    for chrom in chromosomes:
        perchrom_mutect[chrom] = job.addChildJobFn(run_mutect_perchrom, tumor_bam, normal_bam, univ_options, mutect_options, chrom, memory='6G', disk=PromisedRequirement(mutect_disk, tumor_bam['tumor_dna_fix_pg_sorted.bam'], normal_bam['normal_dna_fix_pg_sorted.bam'], mutect_options['genome_fasta'], mutect_options['dbsnp_vcf'], mutect_options['cosmic_vcf'])).rv()

    return perchrom_mutect


def run_mutect_perchrom(job, tumor_bam, normal_bam, univ_options, mutect_options, chrom):
    """
    Run MuTect call on a single chromosome in the input bams.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict mutect_options: Options specific to MuTect
    :param str chrom: Chromosome to process
    :return: fsID for the chromsome vcf
    :rtype: toil.fileStore.FileID
    """
    work_dir = os.getcwd()
    input_files = {'tumor.bam': tumor_bam['tumor_dna_fix_pg_sorted.bam'], 
       'tumor.bam.bai': tumor_bam['tumor_dna_fix_pg_sorted.bam.bai'], 
       'normal.bam': normal_bam['normal_dna_fix_pg_sorted.bam'], 
       'normal.bam.bai': normal_bam['normal_dna_fix_pg_sorted.bam.bai'], 
       'genome.fa.tar.gz': mutect_options['genome_fasta'], 
       'genome.fa.fai.tar.gz': mutect_options['genome_fai'], 
       'genome.dict.tar.gz': mutect_options['genome_dict'], 
       'cosmic.vcf.tar.gz': mutect_options['cosmic_vcf'], 
       'cosmic.vcf.idx.tar.gz': mutect_options['cosmic_idx'], 
       'dbsnp.vcf.gz': mutect_options['dbsnp_vcf'], 
       'dbsnp.vcf.idx.tar.gz': mutect_options['dbsnp_idx']}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    input_files['dbsnp.vcf'] = gunzip(input_files['dbsnp.vcf.gz'])
    for key in ('genome.fa', 'genome.fa.fai', 'genome.dict', 'cosmic.vcf', 'cosmic.vcf.idx',
                'dbsnp.vcf.idx'):
        input_files[key] = untargz(input_files[(key + '.tar.gz')], work_dir)

    input_files = {key:docker_path(path) for key, path in input_files.items()}
    mutout = ('').join([work_dir, '/', chrom, '.out'])
    mutvcf = ('').join([work_dir, '/', chrom, '.vcf'])
    parameters = ['-R', input_files['genome.fa'],
     '--cosmic', input_files['cosmic.vcf'],
     '--dbsnp', input_files['dbsnp.vcf'],
     '--input_file:normal', input_files['normal.bam'],
     '--input_file:tumor', input_files['tumor.bam'],
     '-L', chrom,
     '--out', docker_path(mutout),
     '--vcf', docker_path(mutvcf)]
    java_xmx = mutect_options['java_Xmx'] if mutect_options['java_Xmx'] else univ_options['java_Xmx']
    docker_call(tool='mutect', tool_parameters=parameters, work_dir=work_dir, dockerhub=univ_options['dockerhub'], java_xmx=java_xmx, tool_version=mutect_options['version'])
    output_file = job.fileStore.writeGlobalFile(mutvcf)
    export_results(job, output_file, mutvcf, univ_options, subfolder='mutations/mutect')
    job.fileStore.logToMaster('Ran MuTect on %s:%s successfully' % (univ_options['patient'], chrom))
    return output_file


def process_mutect_vcf(job, mutect_vcf, work_dir, univ_options):
    """
    Process the MuTect vcf for accepted calls.

    :param toil.fileStore.FileID mutect_vcf: fsID for a MuTect generated chromosome vcf
    :param str work_dir: Working directory
    :param dict univ_options: Dict of universal options used by almost all tools
    :return: Path to the processed vcf
    :rtype: str
    """
    mutect_vcf = job.fileStore.readGlobalFile(mutect_vcf)
    with open(mutect_vcf, 'r') as (infile):
        with open(mutect_vcf + 'mutect_parsed.tmp', 'w') as (outfile):
            for line in infile:
                line = line.strip()
                if line.startswith('#'):
                    print(line, file=outfile)
                    continue
                line = line.split('\t')
                if line[6] != 'REJECT':
                    print(('\t').join(line), file=outfile)

    return outfile.name