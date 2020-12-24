# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/writer/fasta.py
# Compiled at: 2014-10-06 17:21:15
from writer import Writer
from Bio import SeqIO

class Fasta(Writer):
    suffix = 'fa'

    def write(self):
        self.OutputFilesClass.extension = self.suffix
        next_output_file = self.OutputFilesClass.get_next_file()
        self.used_filenames.append(next_output_file)
        SeqIO.write(self.data, next_output_file, 'fasta')