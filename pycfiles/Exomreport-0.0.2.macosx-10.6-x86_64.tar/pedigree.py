# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/pedigree.py
# Compiled at: 2019-05-30 01:58:07
import gzip, os
from collections import defaultdict
from annotation_filter import Filter
from hgvs import AA_change
from vcf_split import VCFSplit
import pandas as pd, json

class Pedigree(VCFSplit):
    title1 = [
     'chr', 'hg38_position', 'hg19_position', 'rsid', 'ref', 'alt', 'qual', 'filter', 'GT',
     'RefDepth', 'Alt1Depth', 'Alt2Depth', 'totalDP', 'genotype_quality', 'match_transcript', 'inheritance', 'phenotype', 'genetic_pattern']

    def __init__(self, vcf, child, father, mother):
        super(Pedigree, self).__init__(vcf)
        self.child = child
        self.father = father
        self.mother = mother
        self.get_father_mother_position()

    def get_trio(self):
        child_pos = [ i for i, v in enumerate(self.samples) if v.find(self.child) != -1
                    ][0]
        father_pos = [ i for i, v in enumerate(self.samples) if v.find(self.father) != -1
                     ][0]
        mother_pos = [ i for i, v in enumerate(self.samples) if v.find(self.mother) != -1
                     ][0]
        return (child_pos, father_pos, mother_pos)

    def get_father_mother_position(self):
        if not hasattr(self, 'child_pos'):
            self.child_pos, self.father_pos, self.mother_pos = self.get_trio()

    def get_father_mother_GT(self, line):
        father_gt = line[self.father_pos].split(':')[0]
        mother_gt = line[self.mother_pos].split(':')[0]
        return father_gt + '|' + mother_gt

    def parse_vcf(self, bool):
        assert len(self.samples[9:]) == 3, 'error,vcf should only contain trio sample'
        assert self.child in self.samples and self.father in self.samples and self.mother in self.samples, 'error,child father mother does not match'
        input = self._open()
        self.chr_pos_father_mother_GT = defaultdict(dict)
        sample_dict = defaultdict(list)
        for i in input:
            if i.startswith('#'):
                continue
            else:
                line = i.strip().split()
                chr = line[0]
                pos = line[1]
                self.chr_pos_father_mother_GT[chr][pos] = self.get_father_mother_GT(line)
                rsid = line[2]
                hg19_position = self.hg38_hg19[chr].get(pos, 'delete')
                ref = line[3]
                alt = line[4].replace(',', '/')
                if self.variant_type == self.snp_or_indel(ref, alt):
                    qual = line[5]
                    _filter = line[6]
                    if _filter == 'PASS':
                        basic_data = [
                         chr, pos, hg19_position,
                         rsid, ref, alt, qual, _filter]
                        info = line[7].split(';')
                        genetic_pattern_pos = [ i for i, v in enumerate(info) if v.find('genetic_pattern') != -1
                                              ]
                        assert not len(genetic_pattern_pos) == 0, 'error, is it annotated by trio module?'
                        genetic_pattern = info[genetic_pattern_pos[0]].split('=')[(-1)]
                        start, end = self.get_position(info)
                        info = info[start:end + 1]
                        info_dict = {}
                        info_list = []
                        for tag in info:
                            key = tag.split('=')[0]
                            value = tag.split('=')[(-1)].replace(',', '/')
                            info_list.append(value)
                            info_dict[key] = value

                        AA_value = info_dict['AAChange.refGene']
                        match_transcript = AA_change(AA_value, self.variant_type).std_AA()
                        gene = info_dict['Gene.refGene']
                        inheritance, phenotype = self._gene_phe(gene)
                        omim = [match_transcript, inheritance,
                         phenotype, genetic_pattern]
                        if bool == True:
                            __filter = Filter(info_dict)
                            if __filter.filter_arg():
                                continue
                            else:
                                for j in range(len(self.samples[9:])):
                                    sample = line[(9 + j)].split(':')
                                    sample_data = self.get_sample_data(sample)
                                    if sample_data == 'filter':
                                        continue
                                    else:
                                        all = basic_data + sample_data + omim + info_list
                                        sample_dict[self.samples[(9 + j)]].append(all)

                        else:
                            for j in range(len(self.samples[9:])):
                                sample = line[(9 + j)].split(':')
                                sample_data = self.get_sample_data(sample)
                                if sample_data == 'filter':
                                    continue
                                else:
                                    all = basic_data + sample_data + omim + info_list
                                    sample_dict[self.samples[(9 + j)]].append(all)

        print 1
        input.close()
        return sample_dict

    def sample_split(self, bool):
        sample_dict = self.parse_vcf(bool)
        for sample in sample_dict:
            output = 'pedigree.' + sample + self.output_name(bool)
            with open(output, 'w') as (f):
                f.write((',').join(self.title1 + self.title2) + '\n')
                for sample_list in sample_dict[sample]:
                    sample_list = map(str, sample_list)
                    f.write((',').join(sample_list) + '\n')

    def merge(self):
        f = [
         'filter', 'withoutfilter']
        for csv in f:
            child = pd.read_table(('pedigree.{}.{}.annovar.{}.csv').format(self.child, self.variant_type, csv), sep=',', header=0, low_memory=False)
            father = pd.read_table(('pedigree.{}.{}.annovar.{}.csv').format(self.father, self.variant_type, csv), sep=',', header=0, low_memory=False)
            mother = pd.read_table(('pedigree.{}.{}.annovar.{}.csv').format(self.mother, self.variant_type, csv), sep=',', header=0, low_memory=False)
            col_name = child.columns.tolist()
            col_name.insert(col_name.index('GT') + 1, 'father_mother_GT(f|m)')
            child = child.reindex(columns=col_name)
            child['father_mother_GT(f|m)'] = child.apply(lambda x: self.chr_pos_father_mother_GT[x['chr']][str(x['hg38_position'])], axis=1)
            father = father.drop('genetic_pattern', axis=1)
            mother = mother.drop('genetic_pattern', axis=1)
            child.to_csv(('pedigree.{}.{}.annovar.{}.csv').format(self.child, self.variant_type, csv), index=False, header=True)
            father.to_csv(('pedigree.{}.{}.annovar.{}.csv').format(self.father, self.variant_type, csv), index=False, header=True)
            mother.to_csv(('pedigree.{}.{}.annovar.{}.csv').format(self.mother, self.variant_type, csv), index=False, header=True)


def main(p_dict):
    vcf = p_dict['vcf']
    child = p_dict['child']
    father = p_dict['father']
    mother = p_dict['mother']
    variant = ['snp', 'indel']
    result = Pedigree(vcf, child, father, mother)
    for variant_type in variant:
        print variant_type
        result.variant_type = variant_type
        print 'true'
        result.sample_split(True)
        print 'false'
        result.sample_split(False)
        print 'merge'
        result.merge()