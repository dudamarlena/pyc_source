# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimseq/getCoverage.py
# Compiled at: 2020-03-17 12:13:32
# Size of source mod 2**32: 6225 bytes
import subprocess, pandas as pd, numpy as np, os, logging
from functools import partial
from collections import defaultdict
from multiprocessing import Pool
log = logging.getLogger(__name__)

def filterCoverage(cov_table, min_cov):
    filtered_list = list(cov_table[((cov_table.values < min_cov).any(1) & ~cov_table.index.str.contains('mito'))].index)
    log.info('{} clusters filtered out according to minimum coverage threshold: {}'.format(len(filtered_list), min_cov))
    return filtered_list


def getBamList(sampleGroups):
    sampleGroups = open(sampleGroups, 'r')
    baminfo = defaultdict(list)
    bamlist = list()
    for line in sampleGroups:
        line = line.strip()
        currbam = str(line.split('\t')[0])
        condition = line.split('\t')[1]
        librarySize = int(line.split('\t')[2])
        baminfo[currbam] = [condition, librarySize]
        bamlist.append(currbam)

    return (baminfo, bamlist)


def getCoverage(sampleGroups, out_dir, min_cov, control_cond, filtered_cov):
    log.info('\n+-----------------------------------+\t\t\n| Calculating coverage and plotting |\t\t\n+-----------------------------------+')
    baminfo, bamlist = getBamList(sampleGroups)
    cov_mean = list()
    for bam, info in baminfo.items():
        coverage = pd.read_csv((out_dir + bam.split('/')[(-1)] + '_coverage.txt'), index_col=0, sep='\t')
        coverage['aa'] = coverage.index.format()
        coverage.loc[(coverage.aa.str.contains('mito'), 'aa')] = 'mito' + coverage[coverage.aa.str.contains('mito')].aa.str.split('-').str[(-4)]
        coverage.loc[(coverage.aa.str.contains('nmt'), 'aa')] = 'nmt' + coverage[coverage.aa.str.contains('nmt')].aa.str.split('-').str[(-4)]
        coverage.loc[(~coverage.aa.str.contains('mito') & ~coverage.aa.str.contains('nmt'), 'aa')] = coverage[(~coverage.aa.str.contains('mito') & ~coverage.aa.str.contains('nmt'))].aa.str.split('-').str[(-4)]
        coverage = coverage[['pos', 'cov', 'aa', 'bam']]
        coverage['condition'] = info[0]
        coverage['cov'] = coverage['cov'].astype(float)
        coverage['cov_norm'] = coverage['cov'] / info[1]
        coverage['bin'] = coverage.groupby([coverage.index])['pos'].transform(lambda x: pd.qcut(x, 25, labels=(range(4, 104, 4))))
        cov_mean.append(coverage)

    cov_mean = pd.concat(cov_mean, axis=0)
    cov_mean = cov_mean[(~cov_mean.index.isin(filtered_cov))]
    cov_mean_gene = cov_mean.copy()
    cov_mean_gene['Cluster'] = cov_mean_gene.index.format()
    cov_mean_gene.loc[(cov_mean_gene.Cluster.str.contains('mito'), 'Cluster')] = 'mito' + cov_mean_gene[cov_mean_gene.Cluster.str.contains('mito')].Cluster.str.split('-').str[1:].str.join('-')
    cov_mean_gene.loc[(cov_mean_gene.Cluster.str.contains('nmt'), 'Cluster')] = 'nmt' + cov_mean_gene[cov_mean_gene.Cluster.str.contains('nmt')].Cluster.str.split('-').str[1:].str.join('-')
    cov_mean_gene.loc[(~cov_mean_gene.Cluster.str.contains('mito') & ~cov_mean_gene.Cluster.str.contains('nmt'), 'Cluster')] = cov_mean_gene[(~cov_mean_gene.Cluster.str.contains('mito') & ~cov_mean_gene.Cluster.str.contains('nmt'))].Cluster.str.split('-').str[1:].str.join('-')
    cov_mean_gene = cov_mean_gene[['Cluster', 'pos', 'cov', 'aa', 'condition', 'cov_norm', 'bin', 'bam']]
    cov_mean_gene = cov_mean_gene.groupby(['Cluster', 'bin', 'condition', 'bam']).mean()
    cov_mean_gene = cov_mean_gene.dropna()
    cov_mean_gene.to_csv((out_dir + 'coverage_bygene.txt'), sep='\t')
    cov_mean_aa = cov_mean.groupby(['aa', 'condition', 'bam', 'pos']).sum()
    cov_mean_aa = cov_mean_aa.reset_index()
    cov_mean_aa = cov_mean_aa.groupby('aa').apply(lambda group: group.loc[(group['pos'] != group['pos'].max())])
    cov_mean_aa = cov_mean_aa.drop(columns='aa')
    cov_mean_aa = cov_mean_aa.reset_index()
    cov_mean_aa = cov_mean_aa.drop(columns='level_1')
    cov_mean_aa['bin'] = cov_mean_aa.groupby(['aa', 'condition', 'bam'])['pos'].transform(lambda x: pd.qcut(x, 25, labels=(range(4, 104, 4))))
    cov_mean_aa = cov_mean_aa.groupby(['aa', 'bin', 'condition', 'bam']).mean()
    cov_mean_aa = cov_mean_aa.dropna()
    cov_mean_aa = cov_mean_aa.reset_index()
    cov_mean_aa.to_csv((out_dir + 'coverage_byaa.txt'), sep='\t', index=False)
    cov_mean_aa_controlcond = cov_mean_aa[(cov_mean_aa.condition == control_cond)]
    bam = pd.unique(cov_mean_aa_controlcond['bam'])[0]
    cov_mean_aa_controlcond = cov_mean_aa_controlcond[(cov_mean_aa_controlcond.bam == bam)]
    cov_ratios = dict()
    for aa, data in cov_mean_aa_controlcond.groupby('aa'):
        try:
            ratio = float(data[(data.bin == 8)]['cov_norm']) / float(data[(data.bin == 92)]['cov_norm'])
        except ZeroDivisionError:
            ratio = float(data[(data.bin == 92)]['cov_norm'])

        cov_ratios[aa] = ratio

    sorted_aa = sorted(cov_ratios, key=(cov_ratios.get))
    sorted_aa = '_'.join(str(e) for e in sorted_aa)
    return sorted_aa


def plotCoverage(out_dir, mito_trnas, sorted_aa):
    script_path = os.path.dirname(os.path.realpath(__file__))
    command = ['Rscript', script_path + '/coveragePlot.R', out_dir + 'coverage_bygene.txt', out_dir + 'coverage_byaa.txt', out_dir, sorted_aa, mito_trnas]
    try:
        subprocess.check_call(command)
    except Exception as e:
        logging.error(('Error in {}'.format(command)), exc_info=e)
        raise