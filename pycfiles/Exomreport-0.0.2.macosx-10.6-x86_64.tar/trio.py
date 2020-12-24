# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/trio.py
# Compiled at: 2019-05-23 05:29:15
import gzip, os, sys

class Trio(object):
    t0 = {0: {0: {0: 'anyway', 1: 'anyway', 2: 'back_mutation'}, 1: {0: 'anyway', 1: 'anyway', 2: 'back_mutation'}, 
           2: {0: 'back_mutation', 1: 'back_mutation', 2: 'back_mutation'}}}
    t1 = {1: {0: {0: 'denovo', 1: 'M_HET', 2: 'M_HOM'}, 1: {0: 'F_HET', 1: 'Unknown', 
               2: 'M_HOM'}, 
           2: {0: 'F_HOM', 1: 'F_HOM', 2: 'back_mutation'}}}
    t2 = {2: {0: {0: 'denovo', 1: 'denovo', 2: 'denovo'}, 1: {0: 'denovo', 1: 'F_HET_M_HET', 2: 'F_HET_M_HOM'}, 
           2: {0: 'denovo', 1: 'F_HOM_M_HET', 2: 'F_HOM_M_HOM'}}}
    trio = {}
    trio.update(t0)
    trio.update(t1)
    trio.update(t2)

    def __init__(self, vcf, child, father, mother):
        self.vcf = vcf
        self.child = child
        self.father = father
        self.mother = mother
        self.vcfhead, self.samples = self.get_head()

    def get_head(self):
        input = self.__open()
        vcfhead = []
        samples = []
        for line in input:
            if line.startswith('##'):
                vcfhead.append(line.strip())
            elif line.startswith('#CHROM'):
                vcfhead.append(line)
                samples = line.strip().split()
                if len(samples) != 12:
                    print 'the vcf should only contain child-father-mother trio samples'
                    sys.exit()
                elif self.child in samples and self.father in samples and self.mother in samples:
                    pass
                else:
                    print 'error,child father mother does not match'
                    sys.exit()
                break

        input.close()
        _ = '##INFO=<ID=genetic_pattern,Number=.,Type=String,Description="genetic pattern made by lianlin">'
        vcfhead.insert(20, _)
        return (vcfhead, samples)

    def __open(self):
        if os.path.splitext(self.vcf)[(-1)] == '.gz':
            input = gzip.open(self.vcf, 'r')
        else:
            input = open(self.vcf, 'r')
        return input

    def get_trio(self):
        child_pos = [ i for i, v in enumerate(self.samples) if v.find(self.child) != -1
                    ][0]
        father_pos = [ i for i, v in enumerate(self.samples) if v.find(self.father) != -1
                     ][0]
        mother_pos = [ i for i, v in enumerate(self.samples) if v.find(self.mother) != -1
                     ][0]
        return (child_pos, father_pos, mother_pos)

    def parse_vcf(self):
        child_pos, father_pos, mother_pos = self.get_trio()
        _tran = {'0/0': 0, '0/1': 1, '1/1': 2, '0|0': 0, '0|1': 1, '1|1': 2}
        input = self.__open()
        for i in input:
            if i.startswith('#'):
                continue
            else:
                line = i.strip().split()
                part1 = ('\t').join(line[0:7])
                info = line[7].split(';')
                _format = line[8]
                child_gt = line[child_pos].split(':')[0]
                father_gt = line[father_pos].split(':')[0]
                mother_gt = line[mother_pos].split(':')[0]
                child_gt = _tran.get(child_gt, 'invalid')
                father_gt = _tran.get(father_gt, 'invalid')
                mother_gt = _tran.get(mother_gt, 'invalid')
                if child_gt == 'invalid' or father_gt == 'invalid' or mother_gt == 'invalid':
                    genetic_pattern = 'genetic_pattern=unknown'
                else:
                    genetic_pattern = self.trio.get(child_gt, 'unknown').get(father_gt, 'unknown').get(mother_gt, 'unknown')
                    genetic_pattern = ('genetic_pattern={}').format(genetic_pattern)
                print genetic_pattern
                info.append(genetic_pattern)
                info = (';').join(info)
                part3 = ('\t').join(line[9:])
                all = part1 + '\t' + info + '\t' + _format + '\t' + part3
                yield all

    def out(self):
        outprefix = 'trio.' + os.path.basename(self.vcf)
        if os.path.splitext(self.vcf)[(-1)] == '.gz':
            f = gzip.open(outprefix, 'w')
        else:
            f = open(outprefix, 'w')
        f.write(('\n').join(self.vcfhead))
        for i in self.parse_vcf():
            f.write(i + '\n')

        f.close()
        return


def main(p_dict):
    vcf = p_dict['vcf']
    child = p_dict['child']
    father = p_dict['father']
    mother = p_dict['mother']
    result = Trio(vcf, child, father, mother)
    result.out()