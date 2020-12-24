# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/lack.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 1140 bytes
from subprocess import call
import os

class Lack(object):
    __doc__ = 'A simple lack wrapper.'

    def __init__(self, lack_bin='lack', show_progress=False):
        self._lack_bin = lack_bin
        self._show_progress = show_progress

    def realign_reads(self, query_fasta_path, query_sam_path, ref_fasta_paths, output_sam_path, nonmatch_path, accuracy=95, threads=1, nonmatch_file=None, other_parameters=None):
        lack_call = [
         self._lack_bin, '--query', query_sam_path, '--remapfilename', query_fasta_path, '--database'] + ref_fasta_paths + [
         '--outfile', output_sam_path,
         '--threads', str(threads),
         '--nomatchfilename', nonmatch_path]
        if self._show_progress is False:
            lack_call += ['--silent']
        else:
            if other_parameters:
                lack_call.append(other_parameters)
            if self._show_progress is False:
                with open(os.devnull, 'w') as (devnull):
                    call(lack_call, stderr=devnull)
            else:
                call(lack_call)