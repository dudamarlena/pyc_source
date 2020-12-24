# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/blast.py
# Compiled at: 2014-12-19 21:46:14
import sys
from Bio.Blast import NCBIWWW, NCBIXML

def number_genome_qblast_hits(seqreclist):
    fastastring = ('').join([ rec.format('fasta') for rec in seqreclist ])
    results_handle = NCBIWWW.qblast('blastn', 'nr', fastastring, expect=1.0, word_size=7, nucl_reward=1, nucl_penalty=-3, hitlist_size=1000)
    blast_records = NCBIXML.parse(results_handle)
    hits = [ len(record.alignments) for record in blast_records ]
    return hits


def number_genome_qblast_protein_hits(sequence):
    results_handle = NCBIWWW.qblast('blastp', 'nr', sequence, expect=100, word_size=3, hitlist_size=1000)
    blast_records = NCBIXML.parse(results_handle)
    num_hits = sum([ len(record.alignments) for record in blast_records ])
    return num_hits