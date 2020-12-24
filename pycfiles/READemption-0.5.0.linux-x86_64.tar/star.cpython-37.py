# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/star.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 1656 bytes
from subprocess import call

class STAR_Align(object):
    __doc__ = 'A simple STAR wrapper.'

    def __init__(self, STAR_bin='STAR'):
        self._STAR_bin = STAR_bin

    def build_index(self, threads, index_folder, fasta_files, indexN):
        """Create an index based on a list of fasta files"""
        STAR_call = [
         self._STAR_bin, '--runMode genomeGenerate',
         '--runThreadN', str(threads), '--genomeDir ',
         index_folder, '--genomeFastaFiles ' + fasta_files,
         '--genomeSAindexNbases', str(indexN)]
        call(STAR_call)

    def align_reads(self, threads, index_folder, read_file_or_pair, output_folder, annotation_file, paired_end=False, include_annotation=False):
        if not paired_end:
            assert type(read_file_or_pair) == str
            STAR_call = [
             self._STAR_bin,
             '--readFilesIn', read_file_or_pair,
             '--readFilesCommand zcat']
        else:
            assert type(read_file_or_pair) == list
            STAR_call = [
             self._STAR_bin,
             '--readFilesIn', read_file_or_pair[0],
             read_file_or_pair[1],
             '--readFilesCommand zcat']
        STAR_call += [
         '--runThreadN', str(threads),
         '--genomeDir', index_folder,
         '--outFileNamePrefix', output_folder,
         '--outReadsUnmapped Fastx']
        if include_annotation is True:
            STAR_call.append('--sjdbGTFfile', annotation_file)
        call(STAR_call)