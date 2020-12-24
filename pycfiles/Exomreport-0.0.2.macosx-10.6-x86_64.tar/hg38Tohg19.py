# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/anaconda/anaconda2/lib/python2.7/site-packages/bin/hg38Tohg19.py
# Compiled at: 2019-05-30 02:02:48
import subprocess
from collections import defaultdict

class Hg38ToHg19(object):

    def __init__(self, vcf):
        self.vcf = vcf
        self.write_bed()
        self.liftOver()

    def write_bed(self):
        cmd = ("less  {vcf} |grep -v '^#'|awk '{arg}' >hg38.bed").format(vcf=self.vcf, arg='{print $1,$2-1,$2,$1,$2}')
        subprocess.call(cmd, shell=True)
        return

    def liftOver(self):
        cmd = 'liftOver hg38.bed /share/data1/genome/hg38ToHg19.over.chain.gz hg19.bed unmap'
        subprocess.call(cmd, shell=True)
        return

    def get_bed(self):
        with open('hg19.bed', 'r') as (f):
            for i in f:
                line = i.strip().split()
                yield line

    def hg19_position(self):
        hg38_hg19 = defaultdict(dict)
        for line in self.get_bed():
            chr = line[3]
            hg38_position = line[4]
            _hg19_position = line[2]
            hg38_hg19[chr][hg38_position] = _hg19_position

        return hg38_hg19