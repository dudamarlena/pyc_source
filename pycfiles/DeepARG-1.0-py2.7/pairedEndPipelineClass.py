# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/short_reads_pipeline/pipeline/pairedEndPipelineClass.py
# Compiled at: 2019-06-07 17:56:20
import tools.trimmomaticClass as trim, tools.vsearchClass as vsearch, tools.deepargClass as deeparg, quantification.quantificationClass as quant, pipeline.d16spipelineClass as D16sPipe, quantification.normalizationClass as norm, os
d16sPipe = D16sPipe.d16sPipe()

class PairedEnd:

    def __init__(self, data):
        self.info = ''
        self.pairedR1File = data['pairedR1File']
        self.pairedR2File = data['pairedR2File']
        self.bin = data['programs']
        self.sample_name = data['sample_output_file']
        self.data = data

    def run(self):
        print 'Step 1: Trimming and QC using Trimmomatic'
        if not trim.pairedEnd(self.bin, self.pairedR1File, self.pairedR2File):
            return 0
        print '\n\n\nStep 2: Merging paired end reads using Vsearch'
        if not vsearch.merge(self.bin, self.pairedR1File + '.paired', self.pairedR2File + '.paired', self.sample_name):
            return 0
        print '\n\n\nStep 3: Run DeepARG-SS to identify ARG-like reads'
        if not deeparg.run(self.sample_name + '.clean', self.data, self.data['deep_arg_parameters']['path']):
            return 0
        print '\n\n\nStep 4: Quantification of ARG-like counts'
        if not quant.merge(self.sample_name + '.clean.deeparg.mapping.ARG', self.bin, self.data['deep_arg_parameters']['path']):
            return 0
        print '\n\n\nStep 5: Normalize to 16S rRNAs - this may take a while ...'
        if not d16sPipe.run(self.sample_name + '.clean'):
            return 0
        norm.normalize(self.sample_name + '.clean.sorted.bam.merged.quant', self.sample_name + '.clean.deeparg.mapping.ARG.merged.quant', float(self.data['parameters']['coverage']) / 100, self.data['parameters'])