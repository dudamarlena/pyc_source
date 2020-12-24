# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/anaconda/anaconda2/lib/python2.7/site-packages/bin/database_format.py
# Compiled at: 2019-05-30 02:02:48
import os, math, gzip, pandas as pd, json
from collections import defaultdict

def hpo():
    dic = defaultdict(list)
    with open('/share/data3/lianlin/soft/bin/wes/data/omim.phe_hpo.phe', 'r') as (f):
        for i in f:
            line = i.strip().split()
            omim = line[0]
            hp = line[1].split(':')[1]
            dic[hp].append(omim)

    with open('/share/data3/lianlin/soft/bin/wes/data/omim.phe_hpo.phe.json', 'w') as (f):
        json.dump(dic, f)


def omim():
    df = pd.read_excel('/share/data3/lianlin/soft/bin/wes/data/omimdata.xlsx', sheet_name='Sheet1', header=0)
    col = list(df.columns)
    phe = [ v for i, v in enumerate(col) if v.find('Phenotypes') != -1 ]
    phenotye = phe[:]
    phe.insert(0, 'Gene Symbols')
    df = df[phe]
    df = df.fillna('.')
    for i in range(len(df)):
        for j in phenotye:
            data = df.loc[(i, j)]
            if data == '.':
                continue
            else:
                data = data.split(',')
                if len(data) == 1:
                    df.loc[(i, j)] = '.'
                else:
                    data = data[(-1)].split(' ')[1]
                    if data.isdigit():
                        df.loc[(i, j)] = data
                    else:
                        df.loc[(i, j)] = '.'

    df.to_csv('/share/data3/lianlin/soft/bin/wes/data/omim2.csv', index=False, header=True, sep='\t')


def ff():
    with open('/share/data3/lianlin/soft/bin/wes/data/omim2.csv', 'r') as (f):
        next(f)
        with open('/share/data3/lianlin/soft/bin/wes/data/omim3.txt', 'w') as (p):
            for i in f:
                line = i.strip().split('\t')
                gene = line[0].split(',')[0]
                omim = line[1:]
                for j in omim:
                    if j != '.':
                        p.write(gene + '\t' + j + '\n')


def final():
    dic = defaultdict(list)
    df = pd.read_table('/share/data3/lianlin/soft/bin/wes/data/omim3.txt', header=None)
    df.columns = ['gene', 'omim_phe']
    for i in range(len(df)):
        omim = df.loc[(i, 'omim_phe')]
        gene = df.loc[(i, 'gene')]
        if gene not in dic[omim]:
            dic[omim].append(gene)

    return dic


def ad_gene_phe():
    df1 = pd.read_excel('/share/data3/lianlin/soft/bin/wes/data/omimdata.xlsx', header=0, sheet_name='Sheet1')
    df1 = df1[['Gene Symbols', 'MOI']]
    df1['Approved Symbol'] = ''
    df1 = df1.fillna('.')
    df1['Approved Symbol'] = df1['Gene Symbols'].map(lambda x: x.split(',')[0])
    df1 = df1.drop('Gene Symbols', axis=1)
    df2 = pd.read_table('/share/data3/lianlin/soft/bin/wes/data/genemap2.txt', header=3)
    df2 = df2[['Approved Symbol', 'Phenotypes']]
    df = pd.merge(df1, df2)
    df.columns = ['inheritance', 'gene', 'phenotype']
    df = df.fillna('.')
    df.to_csv('/share/data3/lianlin/soft/bin/wes/data/inh_gene_phenotype.csv', header=True, index=False, sep='\t', encoding='utf_8')


def gene_phe():
    dic = {}
    with open('/share/data3/lianlin/soft/bin/wes/data/inh_gene_phenotype.csv', 'r') as (f):
        for i in f:
            line = i.strip().split('\t')
            gene = line[1]
            inheritance = line[0]
            phenotype = line[2]
            dic[gene] = [inheritance, phenotype]

    with open('/share/data3/lianlin/soft/bin/wes/data/inh_gene_phenotype.json', 'w') as (f):
        json.dump(dic, f, encoding='utf-8')


def main():
    hpo()
    omim()
    ff()
    dic = final()
    with open('/share/data3/lianlin/soft/bin/wes/data/omim_gene.json', 'w') as (f):
        json.dump(dic, f)
    ad_gene_phe()
    gene_phe()