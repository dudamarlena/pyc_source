# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/bammerger.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 770 bytes
import os, sys, pysam

class BamMerger(object):

    def merge(self, output_bam, input_bam_1, input_bam_2):
        for input_bam in [input_bam_1, input_bam_2]:
            if os.path.exists(input_bam) is not True:
                sys.stderr.write('Input file %s does exist. Merging not possible.\n' % input_bam)
                return

        if os.path.exists(output_bam) is True:
            sys.stderr.write('Output file %s already exists. Merging not possible.\n' % output_bam)
            return
        pysam.merge(output_bam, input_bam_1, input_bam_2)
        pysam.index(output_bam)