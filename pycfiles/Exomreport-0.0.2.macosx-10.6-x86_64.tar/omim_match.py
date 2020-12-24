# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/omim_match.py
# Compiled at: 2019-05-20 23:05:07
import json, sys, pandas as pd, os

class Gene(object):

    def __init__(self, hpo, csv_list):
        self.hpo = hpo
        self.csv_list = csv_list
        self.samples = self.get_csvs()

    def omim_gene(self):
        with open('/share/data3/lianlin/soft/bin/wes/data/omim_gene.json', 'r') as (f):
            for i in f:
                omim = json.loads(i)

        return omim

    def hpo_phe(self):
        with open('/share/data3/lianlin/soft/bin/wes/data/omim.phe_hpo.phe.json', 'r') as (f):
            for i in f:
                omim_hpo = json.loads(i)

        return omim_hpo

    def get_hpo(self):
        hpo_list = []
        with open(self.hpo, 'r') as (f):
            for i in f:
                line = i.strip().split(':')[(-1)]
                hpo_list.append(line)

        return hpo_list

    def get_gene(self):
        hpo_list = self.get_hpo()
        omim = self.omim_gene()
        omim_hpo = self.hpo_phe()
        genes = []
        for hpo in hpo_list:
            omim_number_list = omim_hpo.get(hpo, 'no_hpo_number')
            if omim_number_list == 'no_hpo_number':
                gene = hpo + '\t' + 'no_hpo_number'
                genes.append(gene)
            else:
                for omim_num in omim_number_list:
                    gene_list = omim.get(omim_num, 'no_omim_number')
                    if gene_list == 'no_omim_number':
                        gene = hpo + '\t' + omim_num + '\t' + 'no_omim_number'
                        genes.append(gene)
                    else:
                        for g in gene_list:
                            gene = hpo + '\t' + omim_num + '\t' + g
                            genes.append(gene)

        genes = list(set(genes))
        genes = sorted(genes, key=lambda x: int(x.split()[0]))
        return genes

    def write_gene(self):
        self.genes = self.get_gene()
        with open('gene.txt', 'w') as (f):
            for i in self.genes:
                f.write(i + '\n')

    def get_csvs(self):
        samples = []
        with open(self.csv_list, 'r') as (f):
            for i in f:
                samples.append(i.strip())

        return samples

    def csv_filter(self):
        self.genes = [ i.split()[(-1)] for i in self.genes ]
        print self.genes
        for sample in self.samples:
            print 'panel.' + sample
            df = pd.read_csv(sample, header=0)
            df = df[df['Gene.refGene'].isin(self.genes)]
            out = os.path.basename(sample)
            df.to_csv('panel.' + out, index=False, header=True)


def main(p_dict):
    hpo = p_dict['hpo']
    csv_list = p_dict['csv']
    result = Gene(hpo, csv_list)
    result.write_gene()
    result.csv_filter()