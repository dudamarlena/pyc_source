# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/results/pointfinder/nucleotide/NucleotideMutationPosition.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 1771 bytes
import staramr.blast.results.pointfinder.MutationPosition as MutationPosition

class NucleotideMutationPosition(MutationPosition):

    def __init__(self, match_position, database_amr_gene_string, input_genome_string, database_amr_gene_start):
        super().__init__(match_position, database_amr_gene_start)
        self._database_amr_gene_mutation = database_amr_gene_string[match_position].upper()
        self._input_genome_mutation = input_genome_string[match_position].upper()

    def get_type(self):
        return 'nucleotide'

    def get_mutation_position(self):
        return self.get_nucleotide_position()

    def get_database_amr_gene_mutation(self):
        return self._database_amr_gene_mutation

    def get_input_genome_mutation(self):
        return self._input_genome_mutation

    def get_mutation_string(self):
        return self.get_database_amr_gene_mutation() + ' -> ' + self.get_input_genome_mutation()

    def __repr__(self):
        return ('NucleotideMutationPosition(_database_amr_gene_start={_database_amr_gene_start}, _nucleotide_position_amr_gene={_nucleotide_position_amr_gene}, _database_amr_gene_mutation={_database_amr_gene_mutation}, _input_genome_mutation={_input_genome_mutation})'.format)(**self.__dict__)