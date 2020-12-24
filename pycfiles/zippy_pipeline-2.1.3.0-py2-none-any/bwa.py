# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quejebo/zippy/zippy/zippy/bwa.py
# Compiled at: 2018-04-11 20:07:59
import os.path
from pyflow import WorkflowRunner

class BWAWorkflow(WorkflowRunner):

    def __init__(self, output_dir, bwa_exec, samtools_exec, genome_fa, cores, mem, fastq, sample='', args=''):
        self.output_dir = output_dir
        self.bwa_exec = bwa_exec
        self.samtools_exec = samtools_exec
        self.genome_fa = genome_fa
        self.cores = cores
        self.mem = mem
        self.fastq = fastq
        self.sample = sample
        self.args = args

    def workflow(self):
        cmd = ('mkdir -p {}').format(self.output_dir)
        self.addTask(label='make_out_dir', command=cmd, isForceLocal=True)
        out_bam = os.path.join(self.output_dir, 'out.bam')
        if len(self.fastq) == 2:
            fastq = (' ').join(self.fastq)
        elif len(self.fastq) == 1:
            fastq = self.fastq
        else:
            raise 'More than two FASTQs passed to bwamem!'
        if self.args != '':
            self.args = ' ' + self.args
        else:
            self.args = (" -M -R '@RG\\tID:1\\tLB:{0}\\tPL:ILLUMINA\\tSM:{0}'").format(self.sample)
        cmd = '%s mem' % self.bwa_exec + ' -t %i' % (self.cores * 2) + self.args + ' %s %s' % (self.genome_fa, fastq) + ' | %s view -b -o %s -' % (self.samtools_exec, out_bam)
        self.flowLog(cmd)
        self.addTask(label='bwamem', command=cmd, nCores=self.cores, memMb=self.mem, dependencies='make_out_dir')
        out_sorted_bam = os.path.join(self.output_dir, 'out.sorted.bam')
        out_temp = os.path.join(self.output_dir, 'tmp')
        cmd = self.samtools_exec + ' sort %s' % out_bam + ' -O bam' + ' -o ' + out_sorted_bam + ' -T ' + out_temp + ' -@ %i' % self.cores
        self.addTask(label='sort_bam', command=cmd, nCores=self.cores, memMb=min(32768, self.mem), dependencies='bwamem')
        cmd = ('rm {}').format(out_bam)
        self.addTask(label='del_unsorted_bam', command=cmd, dependencies='sort_bam')


if __name__ == '__main__':
    pass