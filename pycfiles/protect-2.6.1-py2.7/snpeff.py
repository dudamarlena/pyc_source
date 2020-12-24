# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/mutation_annotation/snpeff.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import absolute_import, print_function
from math import ceil
from protect.common import docker_call, docker_path, export_results, get_files_from_filestore, untargz
import os

def snpeff_disk(snpeff_index):
    return int(6 * ceil(snpeff_index.size + 524288))


def run_snpeff(job, merged_mutation_file, univ_options, snpeff_options):
    """
    Run snpeff on an input vcf.

    :param toil.fileStore.FileID merged_mutation_file: fsID for input vcf
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict snpeff_options: Options specific to snpeff
    :return: fsID for the snpeffed vcf
    :rtype: toil.fileStore.FileID
    """
    work_dir = os.getcwd()
    input_files = {'merged_mutations.vcf': merged_mutation_file, 
       'snpeff_index.tar.gz': snpeff_options['index']}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    input_files['snpeff_index'] = untargz(input_files['snpeff_index.tar.gz'], work_dir)
    input_files = {key:docker_path(path) for key, path in input_files.items()}
    parameters = [
     'eff',
     '-dataDir', input_files['snpeff_index'],
     '-c',
     ('/').join([input_files['snpeff_index'],
      'snpEff_' + univ_options['ref'] + '_gencode.config']),
     '-no-intergenic',
     '-no-downstream',
     '-no-upstream',
     '-noStats',
     univ_options['ref'] + '_gencode',
     input_files['merged_mutations.vcf']]
    xmx = snpeff_options['java_Xmx'] if snpeff_options['java_Xmx'] else univ_options['java_Xmx']
    with open(('/').join([work_dir, 'mutations.vcf']), 'w') as (snpeff_file):
        docker_call(tool='snpeff', tool_parameters=parameters, work_dir=work_dir, dockerhub=univ_options['dockerhub'], java_xmx=xmx, outfile=snpeff_file, tool_version=snpeff_options['version'])
    output_file = job.fileStore.writeGlobalFile(snpeff_file.name)
    export_results(job, output_file, snpeff_file.name, univ_options, subfolder='mutations/snpeffed')
    job.fileStore.logToMaster('Ran snpeff on %s successfully' % univ_options['patient'])
    return output_file