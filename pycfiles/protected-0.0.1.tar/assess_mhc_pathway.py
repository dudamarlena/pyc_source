# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/addons/assess_mhc_pathway.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import print_function
from collections import Counter
from protect.addons.common import TCGAToGTEx
from protect.common import export_results, get_files_from_filestore, untargz
from protect.haplotyping.phlat import parse_phlat_file
import json, os, pandas as pd

def run_mhc_gene_assessment(job, rsem_files, rna_haplotype, univ_options, reports_options):
    """
    A wrapper for assess_mhc_genes.

    :param dict rsem_files: Results from running rsem
    :param str rna_haplotype: The job store id for the rna haplotype file
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict reports_options: Options specific to reporting modules
    :return: The results of running assess_mhc_genes
    :rtype: toil.fileStore.FileID
    """
    return job.addChildJobFn(assess_mhc_genes, rsem_files['rsem.genes.results'], rna_haplotype, univ_options, reports_options).rv()


def assess_mhc_genes(job, gene_expression, rna_haplotype, univ_options, reports_options):
    """
    Assess the prevalence of the various genes in the MHC pathway and return a report in the tsv
    format.

    :param toil.fileStore.FileID gene_expression: fsID for the rsem gene expression file
    :param toil.fileStore.FileID|None rna_haplotype: fsID for the RNA PHLAT file
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict reports_options: Options specific to reporting modules
    :return: The fsID for the mhc pathway report file
    :rtype: toil.fileStore.FileID
    """
    work_dir = os.getcwd()
    tumor_type = univ_options['tumor_type']
    b_types = {'tcga': tumor_type + ' normal', 
       'gtex': TCGAToGTEx[tumor_type] if tumor_type in TCGAToGTEx else 'NA'}
    input_files = {'rsem_quant.tsv': gene_expression, 
       'mhc_pathways.tsv.tar.gz': reports_options['mhc_pathways_file']}
    if rna_haplotype is not None:
        input_files['rna_haplotype.sum'] = rna_haplotype
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    input_files['mhc_pathways.tsv'] = untargz(input_files['mhc_pathways.tsv.tar.gz'], work_dir)
    background_df = pd.read_table(input_files['mhc_pathways.tsv'], index_col=0, header=0)
    if rna_haplotype is not None:
        with open(input_files['rna_haplotype.sum']) as (rna_mhc):
            mhc_alleles = {'HLA_A': [], 'HLA_B': [], 'HLA_C': [], 'HLA_DPA': [], 'HLA_DQA': [], 'HLA_DPB': [], 'HLA_DQB': [], 'HLA_DRB': []}
            mhc_alleles = parse_phlat_file(rna_mhc, mhc_alleles)
    gene_expressions = pd.read_table(input_files['rsem_quant.tsv'], index_col=0, header=0)
    gene_expressions = Counter({x.split('.')[0]:y for x, y in gene_expressions['TPM'].to_dict().items()})
    roles = {x for x in background_df['Roles'].values if ',' not in x if ',' not in x}
    with open('mhc_pathway_report.txt', 'w') as (mpr):
        for role in roles:
            role_df = background_df[background_df['Roles'].str.contains(role)]
            print(role.center(90, ' '), file=mpr)
            print(('{:12}{:<12}{:<17}{:<12}{:<20}{:<17}\n').format('Gene', 'Observed', 'Threshold_GTEX', 'Result', 'Threshold_TCGA_N', 'Result'), file=mpr)
            if role == 'MHCI loading':
                for mhci_allele in ('HLA_A', 'HLA_B', 'HLA_C'):
                    if rna_haplotype is not None:
                        num_alleles = len(mhc_alleles[mhci_allele])
                        result = 'FAIL' if num_alleles == 0 else 'LOW' if num_alleles == 1 else 'PASS'
                    else:
                        result = num_alleles = 'NA'
                    print(('{:12}{:<12}{:<17}{:<12}{:<20}{:<17}').format(mhci_allele, 2, num_alleles, result, 2, result), file=mpr)

            else:
                if role == 'MHCII loading':
                    for mhcii_allele in ('HLA_DQA', 'HLA_DQB', 'HLA_DRB'):
                        if rna_haplotype is not None:
                            num_alleles = len(mhc_alleles[mhcii_allele])
                            result = 'FAIL' if num_alleles == 0 else 'LOW' if num_alleles == 1 else 'PASS'
                        else:
                            result = num_alleles = 'NA'
                        print(('{:12}{:<12}{:<17}{:<12}{:<20}{:<17}').format(mhcii_allele, 2, num_alleles, result, 2, result), file=mpr)

                for ensg in role_df.index:
                    ensgName = background_df.ix[(ensg, 'Name')]
                    b_vals = {}
                    for bkg in b_types:
                        val = ('{0:.2f}').format(role_df.loc[ensg].get(b_types[bkg], default='NA'))
                        result = 'NA' if val == 'NA' else 'LOW' if float(val) >= float(gene_expressions[ensg]) else 'PASS'
                        b_vals[bkg] = (val, result)

                    print(('{:12}{:<12}{:<17}{:<12}{:<20}{:<17}').format(ensgName, float(gene_expressions[ensg]), b_vals['gtex'][0], b_vals['gtex'][1], b_vals['tcga'][0], b_vals['tcga'][1]), file=mpr)

            print('\n', file=mpr)

    output_file = job.fileStore.writeGlobalFile(mpr.name)
    export_results(job, output_file, mpr.name, univ_options, subfolder='reports')
    job.fileStore.logToMaster('Ran mhc gene assessment on %s successfully' % univ_options['patient'])
    return output_file