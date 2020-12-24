# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/haplotyping/phlat.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import absolute_import, print_function
from collections import defaultdict
from math import ceil
from protect.common import docker_call, docker_path, export_results, get_files_from_filestore, is_gzipfile, untargz
import os, re

def phlat_disk(rna_fastqs):
    return int(ceil(sum([ f.size for f in rna_fastqs ]) + 524288) + 8053063680)


def run_phlat(job, fastqs, sample_type, univ_options, phlat_options):
    """
    Run PHLAT on a pair of input fastqs of type `sample_type`.

    :param list fastqs: List of input fastq files
    :param str sample_type: Description of the sample type to inject into the file name.
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict phlat_options: Options specific to PHLAT
    :return: fsID for the HLA haplotype called from teh input fastqs
    :rtype: toil.fileStore.FileID
    """
    work_dir = os.getcwd()
    input_files = {'input_1.fastq': fastqs[0], 
       'input_2.fastq': fastqs[1], 
       'phlat_index.tar.gz': phlat_options['index']}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    gz = '.gz' if is_gzipfile(input_files['input_1.fastq']) else ''
    if gz:
        for read_file in ('input_1.fastq', 'input_2.fastq'):
            os.symlink(read_file, read_file + gz)
            input_files[read_file + gz] = input_files[read_file] + gz

    input_files['phlat_index'] = untargz(input_files['phlat_index.tar.gz'], work_dir)
    input_files = {key:docker_path(path) for key, path in input_files.items()}
    parameters = [
     '-1', input_files[('input_1.fastq' + gz)],
     '-2', input_files[('input_2.fastq' + gz)],
     '-index', input_files['phlat_index'],
     '-b2url', '/usr/local/bin/bowtie2',
     '-tag', sample_type,
     '-e', '/home/phlat-1.0',
     '-o', '/data',
     '-p', str(phlat_options['n'])]
    docker_call(tool='phlat', tool_parameters=parameters, work_dir=work_dir, dockerhub=univ_options['dockerhub'], tool_version=phlat_options['version'])
    output_file = job.fileStore.writeGlobalFile(('').join([work_dir, '/', sample_type, '_HLA.sum']))
    job.fileStore.logToMaster('Ran phlat on %s:%s successfully' % (
     univ_options['patient'], sample_type))
    return output_file


def merge_phlat_calls(job, tumor_phlat, normal_phlat, rna_phlat, univ_options):
    """
    Merge tumor, normal and tumor rna Haplotypes into consensus calls.

    :param toil.fileStore.FileID tumor_phlat: fsID for HLA haplotypes called from tumor DNA
    :param toil.fileStore.FileID normal_phlat: fsID for HLA haplotypes called from normal DNA
    :param toil.fileStore.FileID rna_phlat: fsID for HLA haplotypes called from tumor RNA
    :param dict univ_options: Dict of universal options used by almost all tools
    :return: Dict of fsIDs for consensus MHCI and MHCII alleles
             output_files
                    |- 'mhci_alleles.list': fsID
                    +- 'mhcii_alleles.list': fsID
    :rtype: dict
    """
    job.fileStore.logToMaster('Merging Phlat calls')
    work_dir = os.getcwd()
    input_files = {'tumor_dna': tumor_phlat, 
       'normal_dna': normal_phlat, 
       'tumor_rna': rna_phlat}
    input_files = get_files_from_filestore(job, input_files, work_dir)
    with open(input_files['tumor_dna'], 'r') as (td_file):
        with open(input_files['normal_dna'], 'r') as (nd_file):
            with open(input_files['tumor_rna'], 'r') as (tr_file):
                mhc_alleles = {'HLA_A': [], 'HLA_B': [], 'HLA_C': [], 'HLA_DPA': [], 'HLA_DQA': [], 'HLA_DPB': [], 'HLA_DQB': [], 'HLA_DRB': []}
                for phlatfile in (td_file, nd_file, tr_file):
                    mhc_alleles = parse_phlat_file(phlatfile, mhc_alleles)

    with open(os.path.join(work_dir, 'mhci_alleles.list'), 'w') as (mhci_file):
        with open(os.path.join(work_dir, 'mhcii_alleles.list'), 'w') as (mhcii_file):
            for mhci_group in ['HLA_A', 'HLA_B', 'HLA_C']:
                mpa = most_probable_alleles(mhc_alleles[mhci_group])
                print(('\n').join([ ('').join(['HLA-', x]) for x in mpa ]), file=mhci_file)

            drb_mpa = most_probable_alleles(mhc_alleles['HLA_DRB'])
            print(('\n').join([ ('').join(['HLA-', x]) for x in drb_mpa ]), file=mhcii_file)
            dqa_mpa = most_probable_alleles(mhc_alleles['HLA_DQA'])
            dqb_mpa = most_probable_alleles(mhc_alleles['HLA_DQB'])
            for dqa_allele in dqa_mpa:
                for dqb_allele in dqb_mpa:
                    print(('').join(['HLA-', dqa_allele, '/', dqb_allele]), file=mhcii_file)

    output_files = defaultdict()
    for allele_file in ['mhci_alleles.list', 'mhcii_alleles.list']:
        output_files[allele_file] = job.fileStore.writeGlobalFile(os.path.join(work_dir, allele_file))
        export_results(job, output_files[allele_file], os.path.join(work_dir, allele_file), univ_options, subfolder='haplotyping')

    return output_files


def parse_phlat_file(phlatfile, mhc_alleles):
    """
    Parse an input phlat file to identify predicted HLA alleles.

    :param file phlatfile: Open file descriptor for a phlat output sum file
    :param dict mhc_alleles: Dict of alleles.
    :return: Updated dict of alleles
    :rtype: dict
    """
    for line in phlatfile:
        if line.startswith('Locus'):
            continue
        line = line.strip().split()
        if line[0].startswith('HLA_D'):
            line[0] = line[0][:-1]
        if line[1] == 'no':
            continue
        if line[4] != 'NA':
            split_field = line[1].split(':')
            if len(split_field) >= 2 and not split_field[1] == 'xx':
                mhc_alleles[line[0]].append((line[1], line[4]))
        if line[5] != 'NA':
            split_field = line[2].split(':')
            if len(split_field) >= 2 and not split_field[1] == 'xx':
                mhc_alleles[line[0]].append((line[2], line[5]))

    return mhc_alleles


def most_probable_alleles(allele_list):
    """
    Identify the most probable haplotype in a list

    :param list allele_list: List of tuples of (allele, p_value)
    :return: List of 2 most probable alleles in the group
    :rtype: list[str]
    """
    all_alleles = defaultdict()
    for allele, pvalue in allele_list:
        allele = re.split(':', allele)
        if len(allele) < 2:
            continue
        allele = (':').join([allele[0], allele[1]])
        try:
            all_alleles[allele].append(float(pvalue))
        except KeyError:
            all_alleles[allele] = [
             float(pvalue)]

    if len(all_alleles.keys()) <= 2:
        return all_alleles.keys()
    else:
        return sorted(all_alleles.keys(), key=lambda x: (
         -len(all_alleles[x]), sum(all_alleles[x])))[0:2]