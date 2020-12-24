# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/readrealigner.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 727 bytes
from reademptionlib.lack import Lack

class ReadRealigner(object):
    __doc__ = 'An abstraction layer for different short read realigners.'

    def __init__(self, lack_bin, show_progress):
        self.lack = Lack(lack_bin, show_progress=show_progress)

    def run_alignment(self, query_fasta_path, query_sam_path, ref_seq_paths, output_sam_path, nomatch_path, threads, accuracy):
        self.lack.realign_reads(query_fasta_path, query_sam_path,
          ref_seq_paths,
          output_sam_path,
          nonmatch_path=nomatch_path,
          threads=threads,
          accuracy=accuracy)