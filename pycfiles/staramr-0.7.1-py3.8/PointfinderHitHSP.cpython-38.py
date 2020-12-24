# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/results/pointfinder/PointfinderHitHSP.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 1943 bytes
import logging
import staramr.blast.results.AMRHitHSP as AMRHitHSP
import staramr.blast.results.pointfinder.codon.CodonMutationPosition as CodonMutationPosition
logger = logging.getLogger('PointfinderHitHSP')

class PointfinderHitHSP(AMRHitHSP):

    def __init__(self, file, blast_record):
        super().__init__(file, blast_record)

    def get_amr_gene_name(self):
        """
        Gets the particular gene name for the PointFinder hit.
        :return: The gene name.
        """
        return self._blast_record['qseqid']

    def _get_match_positions(self):
        amr_seq = self.get_amr_gene_seq()
        genome_seq = self.get_genome_contig_hsp_seq()
        return [i for i, (x, y) in enumerate(zip(amr_seq, genome_seq)) if x != y]

    def _get_mutation_positions(self, start):
        mutation_positions_filtered = []
        codon_starts = []
        amr_seq = self.get_amr_gene_seq()
        genome_seq = self.get_genome_contig_hsp_seq()
        mutation_positions = [CodonMutationPosition(i, amr_seq, genome_seq, start) for i in self._get_match_positions()]
        for m in mutation_positions:
            if m._codon_start not in codon_starts:
                codon_starts.append(m._codon_start)
                mutation_positions_filtered.append(m)
            return mutation_positions_filtered

    def get_mutations(self):
        """
        Gets a list of NucleotideMutationPosition for the individual mutations.
        :return: A list of NucleotideMutationPosition.
        """
        return self._get_mutation_positions(self.get_amr_gene_start())