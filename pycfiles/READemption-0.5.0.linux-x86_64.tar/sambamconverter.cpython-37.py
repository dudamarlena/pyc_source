# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/sambamconverter.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 2028 bytes
import os, pysam

class SamToBamConverter(object):

    def __init__(self):
        self._unsorted_appendix = '.tmp_unsorted'

    def sam_to_bam(self, sam_path, bam_path_prefix):
        if self._sam_file_is_empty(sam_path) is True:
            self._generate_empty_bam_file(sam_path, bam_path_prefix)
            os.remove(sam_path)
            return
        temp_unsorted_bam_path = self._temp_unsorted_bam_path(bam_path_prefix)
        pysam.samtools.view('-b',
          ('-o{}'.format(temp_unsorted_bam_path)), sam_path, catch_stdout=False)
        pysam.sort(temp_unsorted_bam_path, '-o', bam_path_prefix + '.bam')
        pysam.index('%s.bam' % bam_path_prefix)
        os.remove(temp_unsorted_bam_path)
        os.remove(sam_path)

    def bam_to_sam(self, bam_path, sam_path):
        pysam.view(('-ho{}'.format(sam_path)), bam_path, catch_stdout=False)

    def _temp_unsorted_bam_path(self, bam_path_prefix):
        return '%s%s.bam' % (bam_path_prefix, self._unsorted_appendix)

    def _sam_file_is_empty(self, sam_path):
        for line in open(sam_path):
            if line.startswith('@') is False:
                return False

        return True

    def _generate_empty_bam_file(self, sam_path, bam_path_prefix):
        samfile = pysam.Samfile(sam_path, 'r')
        bamfile = pysam.Samfile(('%s.bam' % bam_path_prefix),
          'wb', header=(samfile.header))
        bamfile.close()
        samfile.close()
        pysam.index('%s.bam' % bam_path_prefix)