# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/results/pointfinder/nucleotide/PointfinderHitHSPRNA.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 812 bytes
import staramr.blast.results.pointfinder.PointfinderHitHSP as PointfinderHitHSP
import staramr.blast.results.pointfinder.nucleotide.NucleotideMutationPosition as NucleotideMutationPosition

class PointfinderHitHSPRNA(PointfinderHitHSP):

    def __init__(self, file, blast_record):
        super().__init__(file, blast_record)

    def _get_mutation_positions(self, start):
        amr_seq = self.get_amr_gene_seq()
        genome_seq = self.get_genome_contig_hsp_seq()
        return [NucleotideMutationPosition(i, amr_seq, genome_seq, start) for i in self._get_match_positions()]