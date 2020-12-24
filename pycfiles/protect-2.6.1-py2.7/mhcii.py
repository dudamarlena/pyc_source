# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/binding_prediction/mhcii.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import absolute_import, print_function
from protect.common import docker_call, get_files_from_filestore, read_peptide_file
import os, re

def predict_mhcii_binding(job, peptfile, allele, univ_options, mhcii_options):
    """
    Predict binding for each peptide in `peptfile` to `allele` using the IEDB mhcii binding
    prediction tool.

    :param toil.fileStore.FileID peptfile: The input peptide fasta
    :param str allele: Allele to predict binding against
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict mhcii_options: Options specific to mhcii binding prediction
    :return: tuple of fsID for file containing the predictions and the predictor used
    :rtype: tuple(toil.fileStore.FileID, str|None)
    """
    work_dir = os.getcwd()
    input_files = {'peptfile.faa': peptfile}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=True)
    peptides = read_peptide_file(os.path.join(os.getcwd(), 'peptfile.faa'))
    parameters = [mhcii_options['pred'],
     allele,
     input_files['peptfile.faa']]
    if not peptides:
        return (job.fileStore.writeGlobalFile(job.fileStore.getLocalTempFile()), None)
    else:
        with open(('/').join([work_dir, 'predictions.tsv']), 'w') as (predfile):
            docker_call(tool='mhcii', tool_parameters=parameters, work_dir=work_dir, dockerhub=univ_options['dockerhub'], outfile=predfile, interactive=True, tool_version=mhcii_options['version'])
        run_netmhciipan = True
        predictor = None
        with open(predfile.name, 'r') as (predfile):
            for line in predfile:
                if not line.startswith('HLA'):
                    continue
                if line.strip().split('\t')[5] == 'NetMHCIIpan':
                    break
                elif line.strip().split('\t')[5] == 'Sturniolo':
                    predictor = 'Sturniolo'
                else:
                    predictor = 'Consensus'
                run_netmhciipan = False
                break

        if run_netmhciipan:
            netmhciipan = job.addChildJobFn(predict_netmhcii_binding, peptfile, allele, univ_options, mhcii_options['netmhciipan'], disk='100M', memory='100M', cores=1)
            job.fileStore.logToMaster('Ran mhcii on %s:%s successfully' % (
             univ_options['patient'], allele))
            return netmhciipan.rv()
        output_file = job.fileStore.writeGlobalFile(predfile.name)
        job.fileStore.logToMaster('Ran mhcii on %s:%s successfully' % (
         univ_options['patient'], allele))
        return (output_file, predictor)
        return


def predict_netmhcii_binding(job, peptfile, allele, univ_options, netmhciipan_options):
    """
    Predict binding for each peptide in `peptfile` to `allele` using netMHCIIpan.

    :param toil.fileStore.FileID peptfile: The input peptide fasta
    :param str allele: Allele to predict binding against
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict netmhciipan_options: Options specific to netmhciipan binding prediction
    :return: tuple of fsID for file containing the predictions and the predictor used (netMHCIIpan)
    :rtype: tuple(toil.fileStore.FileID, str)
    """
    work_dir = os.getcwd()
    input_files = {'peptfile.faa': peptfile}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=True)
    peptides = read_peptide_file(os.path.join(os.getcwd(), 'peptfile.faa'))
    if not peptides:
        return (job.fileStore.writeGlobalFile(job.fileStore.getLocalTempFile()), None)
    else:
        if allele.startswith('HLA-DQA') or allele.startswith('HLA-DPA'):
            allele = re.sub('[*:]', '', allele)
            allele = re.sub('/', '-', allele)
        elif allele.startswith('HLA-DRB'):
            allele = re.sub(':', '', allele)
            allele = re.sub('\\*', '_', allele)
            allele = allele.lstrip('HLA-')
        else:
            raise RuntimeError('Unknown allele seen')
        parameters = [
         '-a', allele,
         '-xls', '1',
         '-xlsfile', 'predictions.tsv',
         '-f', input_files['peptfile.faa']]
        with open(os.devnull, 'w') as (output_catcher):
            docker_call(tool='netmhciipan', tool_parameters=parameters, work_dir=work_dir, dockerhub=univ_options['dockerhub'], outfile=output_catcher, tool_version=netmhciipan_options['version'])
        output_file = job.fileStore.writeGlobalFile(('/').join([work_dir, 'predictions.tsv']))
        job.fileStore.logToMaster('Ran netmhciipan on %s successfully' % allele)
        return (output_file, 'netMHCIIpan')