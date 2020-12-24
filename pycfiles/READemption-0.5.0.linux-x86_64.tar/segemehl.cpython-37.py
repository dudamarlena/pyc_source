# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/segemehl.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 2654 bytes
from subprocess import call
import pysam, os

class Segemehl(object):
    __doc__ = 'A simple segemehl wrapper.'

    def __init__(self, segemehl_bin='segemehl', show_progress=False):
        self._segemehl_bin = segemehl_bin
        self._show_progress = show_progress

    def build_index(self, fasta_files, index_file):
        """Create an index based on a list of fasta files"""
        segemehl_call = [
         self._segemehl_bin, '--database'] + fasta_files + [
         '--generate', index_file]
        if self._show_progress is False:
            with open(os.devnull, 'w') as (devnull):
                call(segemehl_call, stderr=devnull)
        else:
            call(segemehl_call)

    def align_reads(self, read_file_or_pair, index_file, fasta_files, output_file, hit_strategy=1, accuracy=95, evalue=5.0, threads=1, split=False, segemehl_format=False, order=False, nonmatch_file=None, other_parameters=None, paired_end=False):
        if not paired_end:
            assert type(read_file_or_pair) == str
            segemehl_call = [
             self._segemehl_bin,
             '--query', read_file_or_pair]
        else:
            assert type(read_file_or_pair) == list
            segemehl_call = [
             self._segemehl_bin,
             '--query', read_file_or_pair[0],
             '--mate', read_file_or_pair[1]]
        segemehl_call += [
         '--index', index_file, '--database'] + fasta_files + [
         '--outfile', output_file,
         '--bamabafixoida',
         '--hitstrategy', str(hit_strategy),
         '--accuracy', str(accuracy),
         '--evalue', str(evalue),
         '--threads', str(threads)]
        if segemehl_format:
            segemehl_call.append('--SEGEMEHL')
        else:
            if order is True:
                segemehl_call.append('--order')
            if split is True:
                segemehl_call.append('--splits')
            if nonmatch_file:
                segemehl_call += ['--nomatchfilename', nonmatch_file]
            if self._show_progress is False:
                pass
            if other_parameters:
                segemehl_call.append(other_parameters)
            if self._show_progress is False:
                with open(os.devnull, 'w') as (devnull):
                    call(segemehl_call, stderr=devnull)
            else:
                call(segemehl_call)
        tmp_sorted_outfile = f"{output_file}_sorted"
        pysam.sort('-o', tmp_sorted_outfile, output_file)
        os.rename(tmp_sorted_outfile, output_file)
        pysam.index(output_file)