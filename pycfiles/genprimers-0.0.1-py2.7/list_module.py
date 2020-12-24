# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/lib/list_module.py
# Compiled at: 2017-03-26 22:12:05
from Bio import SeqIO

def list_sequences(fasta_file):
    for record in SeqIO.parse(fasta_file, 'fasta'):
        print record.id + '\t' + record.description