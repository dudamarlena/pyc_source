# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/addons/assess_immunotherapy_resistance.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import print_function
from protect.addons.common import TCGAToGTEx
from protect.common import export_results, get_files_from_filestore, untargz
import json, os, pandas as pd, textwrap

def run_itx_resistance_assessment(job, rsem_files, univ_options, reports_options):
    """
    A wrapper for assess_itx_resistance.

    :param dict rsem_files: Results from running rsem
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict reports_options: Options specific to reporting modules
    :return: The results of running assess_itx_resistance
    :rtype: toil.fileStore.FileID
    """
    return job.addChildJobFn(assess_itx_resistance, rsem_files['rsem.genes.results'], univ_options, reports_options).rv()


def assess_itx_resistance(job, gene_expression, univ_options, reports_options):
    """
    Assess the prevalence of the various genes in various cancer pathways and return a report in the txt
    format.

    :param toil.fileStore.FileID gene_expression: fsID for the rsem gene expression file
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict reports_options: Options specific to reporting modules
    :return: The fsID for the itx resistance report file
    :rtype: toil.fileStore.FileID
    """
    work_dir = os.getcwd()
    tumor_type = univ_options['tumor_type']
    input_files = {'rsem_quant.tsv': gene_expression, 
       'itx_resistance.tsv.tar.gz': reports_options['itx_resistance_file'], 
       'immune_resistance_pathways.json.tar.gz': reports_options['immune_resistance_pathways_file']}
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    input_files['itx_resistance.tsv'] = untargz(input_files['itx_resistance.tsv.tar.gz'], work_dir)
    input_files['immune_resistance_pathways.json'] = untargz(input_files['immune_resistance_pathways.json.tar.gz'], work_dir)
    full_data = pd.read_table(input_files['itx_resistance.tsv'], index_col=0)
    with open(input_files['immune_resistance_pathways.json']) as (json_file):
        json_data = json.load(json_file)
    patient_df = pd.read_csv('rsem_quant.tsv', sep=' ', delimiter='\t', header='infer', index_col=0)
    patient_df.index = patient_df.index.str.replace('\\..*$', '')
    with open('immunotherapy_resistance_report.txt', 'w') as (report_file):
        try:
            pathways = json_data['Cancer_to_pathway'][tumor_type]
        except KeyError:
            print('Data not available for ' + tumor_type, file=report_file)

        for pathway in pathways:
            up_is_good = json_data['Pathways'][pathway]['up_is_good']
            if up_is_good:
                comp_fn = lambda x, y: x >= y
            else:
                comp_fn = lambda x, y: x < y
            print('Pathway: ' + pathway + '\n', file=report_file)
            print('Papers: ' + json_data['Pathways'][pathway]['paper'], file=report_file)
            description = json_data['Pathways'][pathway]['description']
            print('Description of pathway:\n' + textwrap.fill(description, width=100), file=report_file)
            print('Pathway genes: ', file=report_file)
            print(('\t{:10}{:<20}{:<20}{:<12}').format('Gene', 'GTEX Median', 'TCGA N Median', 'Observed'), file=report_file)
            status = []
            for gene in json_data['Pathways'][pathway]['genes']:
                gtex = ('{0:.2f}').format(float(full_data.loc[(gene, TCGAToGTEx[tumor_type])])) if gene in full_data.index else 'NA'
                tcga = ('{0:.2f}').format(float(full_data.loc[(gene, tumor_type + ' normal')])) if gene in full_data.index else 'NA'
                tpm_value = ('{0:.2f}').format(float(patient_df.loc[(gene, 'TPM')])) if gene in patient_df.index else 'NA'
                ensg = json_data['Pathways'][pathway]['genes'][gene]
                print(('\t{:10}{:<20}{:<20}{:<12}').format(ensg, gtex, tcga, tpm_value), file=report_file)
                if gtex != 'NA' and tpm_value != 'NA':
                    tcga_bool = comp_fn(float(tpm_value), float(tcga))
                    gtex_bool = comp_fn(float(tpm_value), float(gtex))
                    status.append(tcga_bool and gtex_bool)
                else:
                    status.append(False)

            print('Status: ' + json_data['Pathways'][pathway]['status'][str(sum(status) >= 0.75 * len(status))] + '\n', file=report_file)

    output_file = job.fileStore.writeGlobalFile(report_file.name)
    export_results(job, output_file, report_file.name, univ_options, subfolder='reports')
    job.fileStore.logToMaster('Ran create immunotherapy resistance report on %s successfully' % univ_options['patient'])
    return output_file