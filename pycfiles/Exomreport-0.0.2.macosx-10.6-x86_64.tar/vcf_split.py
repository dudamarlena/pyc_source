# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/vcf_split.py
# Compiled at: 2019-05-28 21:37:02
import time, os, sys
from collections import defaultdict
import gzip
from hg38Tohg19 import Hg38ToHg19
from hgvs import AA_change
from annotation_filter import Filter
import json

class VCFSplit(object):
    title1 = [
     'chr', 'hg38_position', 'hg19_position', 'rsid', 'ref', 'alt', 'qual', 'filter',
     'GT', 'RefDepth', 'Alt1Depth', 'Alt2Depth', 'totalDP', 'genotype_quality', 'match_transcript', 'inheritance', 'phenotype']

    def __init__(self, vcf):
        self.vcf = vcf
        self.coordinate()
        self.get_head()
        self.gene_phenotype()

    def _open(self):
        if os.path.splitext(self.vcf)[(-1)] == '.gz':
            input = gzip.open(self.vcf, 'r')
        else:
            input = open(self.vcf, 'r')
        return input

    def coordinate(self):
        if not hasattr(self, 'hg38_hg19'):
            self.hg38_hg19 = Hg38ToHg19(self.vcf).hg19_position()

    def get_head(self):
        if not hasattr(self, 'title2'):
            self.title2 = []
            self.samples = []
            input = self._open()
            for i in input:
                if i.startswith('##'):
                    continue
                elif i.startswith('#CHROM'):
                    self.samples = i.strip().split()
                else:
                    info = i.strip().split()[7].split(';')
                    start, end = self.get_position(info)
                    info = info[start:end + 1]
                    for tag in info:
                        key = tag.split('=')[0]
                        self.title2.append(key)

                    break

            input.close()

    def snp_or_indel(self, ref, alt):
        alt = alt.split('/')
        alt = sorted(alt, key=lambda x: len(x), reverse=False)[(-1)]
        if len(ref) > 1 or len(alt) > 1:
            return 'indel'
        return 'snp'

    def get_position(self, _info):
        start = [ i for i, x in enumerate(_info) if x.find('Func.refGene') != -1
                ][0]
        end = [ i for i, x in enumerate(_info) if x.find('MutationAssessor_pred') != -1
              ][0]
        return (start, end)

    def parse_vcf(self, bool):
        input = self._open()
        sample_dict = defaultdict(list)
        for i in input:
            if i.startswith('#'):
                continue
            else:
                line = i.strip().split()
                chr = line[0]
                pos = line[1]
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
                        omim = [match_transcript, inheritance, phenotype]
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

    def get_sample_data(self, sample):
        GT = sample[0]
        if GT == '0/0' or GT == './.':
            return 'filter'
        AD = sample[1]
        RefDepth = AD.split(',')[0]
        Alt1Depth = AD.split(',')[1]
        if len(sample) > 3:
            totalDP = sample[2]
            genotype_quality = sample[3]
            if totalDP == '.' or genotype_quality == '.' or int(genotype_quality) < 20:
                return 'filter'
            Alt2Depth = int(totalDP) - int(RefDepth) - int(Alt1Depth)
            sample_data = [GT, RefDepth, Alt1Depth,
             Alt2Depth, totalDP, genotype_quality]
            return sample_data

    def gene_phenotype(self):
        if not hasattr(self, 'gene_phe'):
            with open('/share/data3/lianlin/soft/bin/wes/data/inh_gene_phenotype.json') as (f):
                for i in f:
                    self.gene_phe = json.loads(i)

    def _gene_phe(self, gene):
        inh_phe = self.gene_phe.get(gene, '.')
        if inh_phe == '.':
            inheritance, phenotype = ('.', '.')
        else:
            inheritance, phenotype = inh_phe[0].encode('utf-8'), inh_phe[1].encode('utf-8')
        inheritance = inheritance.replace(',', '/')
        phenotype = phenotype.replace(',', '_')
        return (inheritance, phenotype)

    def output_name(self, bool):
        if bool == True:
            output = ('.{}.annovar.filter.csv').format(self.variant_type)
        else:
            output = ('.{}.annovar.withoutfilter.csv').format(self.variant_type)
        return output

    def sample_split(self, bool):
        sample_dict = self.parse_vcf(bool)
        for sample in sample_dict:
            output = 'carrier.' + sample + self.output_name(bool)
            with open(output, 'w') as (f):
                f.write((',').join(self.title1 + self.title2) + '\n')
                for sample_list in sample_dict[sample]:
                    sample_list = map(str, sample_list)
                    f.write((',').join(sample_list) + '\n')


def main(p_dict):
    vcf = p_dict['vcf']
    variant = ['snp', 'indel']
    result = VCFSplit(vcf)
    for variant_type in variant:
        print variant_type
        result.variant_type = variant_type
        print 'true'
        result.sample_split(True)
        print 'false'
        result.sample_split(False)