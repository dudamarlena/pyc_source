# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/tests/unit/blast/results/pointfinder/codon/test_CodonMutationPosition.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 29419 bytes
import unittest
import staramr.blast.results.pointfinder.codon.CodonMutationPosition as CodonMutationPosition

class CodonMutationPositionTest(unittest.TestCase):

    def testMutationPositionStartCodon1(self):
        mutation_position = 0
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'TTCGATCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'TTC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'F', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1F', 'Incorrect string')

    def testMutationPositionMiddleCodon1(self):
        mutation_position = 1
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'AGCGATCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 2, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'AGC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'S', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1S', 'Incorrect string')

    def testMutationPositionEndCodon1(self):
        mutation_position = 2
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'ATGGATCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 3, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATG', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'M', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1M', 'Incorrect string')

    def testMutationPositionStartCodon2(self):
        mutation_position = 3
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'ATCAATCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'GAT', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'AAT', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'D', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'N', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'D2N', 'Incorrect string')

    def testMutationPositionEndCodon2(self):
        mutation_position = 5
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'ATCGACCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 6, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'GAT', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'GAC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'D', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'D', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'D2D', 'Incorrect string')

    def testMutationPositionStartCodon3(self):
        mutation_position = 6
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'ATCGATGGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 7, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 3, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 3, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'CGA', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'GGA', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'R', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'G', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'R3G', 'Incorrect string')

    def testMutationPositionStartCodon1StartMethionine(self):
        mutation_position = 0
        database_amr_gene_string = 'ATCGATCGA'
        input_genome_string = 'ATGGATCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 1, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATG', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'M', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1M', 'Incorrect string')

    def testMutationPositionStartCodon1Stop(self):
        mutation_position = 2
        database_amr_gene_string = 'TACGATCGA'
        input_genome_string = 'TAAGATCGA'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 3, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'TAC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'TAA', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'Y', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), '*', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'Y1*', 'Incorrect string')

    def testMutationPositionGapStart(self):
        mutation_position = 0
        database_amr_gene_string = 'ATCG'
        input_genome_string = '-TCG'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 1, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), '-TC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1del', 'Incorrect string')

    def testMutationPositionGapMiddle(self):
        mutation_position = 1
        database_amr_gene_string = 'ATCG'
        input_genome_string = 'A-CG'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 2, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'A-C', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1del', 'Incorrect string')

    def testMutationPositionGapEnd(self):
        mutation_position = 2
        database_amr_gene_string = 'ATCG'
        input_genome_string = 'AT-G'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 3, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'AT-', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1del', 'Incorrect string')

    def testMutationPositionGapMiddleEnd(self):
        mutation_position = 2
        database_amr_gene_string = 'ATCGG'
        input_genome_string = 'AT--G'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 3, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'AT-', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I1del', 'Incorrect string')

    def testMutationPositionGapStartMiddleEnd(self):
        mutation_position = 3
        database_amr_gene_string = 'CCCATCGAC'
        input_genome_string = 'CCC---GAC'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), '---', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I2del', 'Incorrect string')

    def testMutationPositionGapPreviousCodon(self):
        mutation_position = 3
        database_amr_gene_string = 'CCCATCGACT'
        input_genome_string = 'CC----GACT'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), '---', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I2del', 'Incorrect string')

    def testMutationPositionGapLargerPreviousCodon(self):
        mutation_position = 3
        database_amr_gene_string = 'CCCATCGACTT'
        input_genome_string = 'C-----GACTT'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), '---', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I2del', 'Incorrect string')

    def testMutationPositionGapBefore(self):
        mutation_position = 3
        database_amr_gene_string = 'CCCATCGAC'
        input_genome_string = '-CCA--GAC'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'A--', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I2del', 'Incorrect string')

    def testMutationPositionGapBeforeAfter(self):
        mutation_position = 3
        database_amr_gene_string = 'CCCATCGACT'
        input_genome_string = '-CCA--GA-T'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'ATC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'A--', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'I', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'del', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'I2del', 'Incorrect string')

    def testMutationPositionGapReferenceStart(self):
        mutation_position = 0
        database_amr_gene_string = '-TCG'
        input_genome_string = 'ATCG'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 1, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), '-TC', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins1I', 'Incorrect string')

    def testMutationPositionGapReferenceMiddle(self):
        mutation_position = 1
        database_amr_gene_string = 'A-CG'
        input_genome_string = 'ATCG'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 2, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'A-C', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins1I', 'Incorrect string')

    def testMutationPositionGapReferenceEnd(self):
        mutation_position = 2
        database_amr_gene_string = 'AT-G'
        input_genome_string = 'ATCG'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 3, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 1, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 1, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'AT-', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins1I', 'Incorrect string')

    def testMutationPositionGapReferenceStartMiddleEnd(self):
        mutation_position = 3
        database_amr_gene_string = 'CCC---GAC'
        input_genome_string = 'CCCATCGAC'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), '---', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins2I', 'Incorrect string')

    def testMutationPositionGapReferencePreviousCodon(self):
        mutation_position = 3
        database_amr_gene_string = 'CC----GACT'
        input_genome_string = 'CCCATCGACT'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), '---', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins2I', 'Incorrect string')

    def testMutationPositionGapReferenceLargerPreviousCodon(self):
        mutation_position = 3
        database_amr_gene_string = 'C-----GACTT'
        input_genome_string = 'CCCATCGACTT'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), '---', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins2I', 'Incorrect string')

    def testMutationPositionGapReferenceBefore(self):
        mutation_position = 3
        database_amr_gene_string = '-CCA--GAC'
        input_genome_string = 'CCCATCGAC'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'A--', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins2I', 'Incorrect string')

    def testMutationPositionGapReferenceBeforeAfter(self):
        mutation_position = 3
        database_amr_gene_string = '-CCA--GA-T'
        input_genome_string = 'CCCATCGACT'
        amr_gene_start = 1
        mutation = CodonMutationPosition(mutation_position, database_amr_gene_string, input_genome_string, amr_gene_start)
        self.assertEqual(mutation.get_nucleotide_position(), 4, 'Incorrect nucleotide position')
        self.assertEqual(mutation.get_codon_start(), 2, 'Incorrect codon start')
        self.assertEqual(mutation.get_mutation_position(), 2, 'Incorrect mutation start')
        self.assertEqual(mutation.get_database_amr_gene_codon(), 'A--', 'Incorrect database codon')
        self.assertEqual(mutation.get_input_genome_codon(), 'ATC', 'Incorrect query codon')
        self.assertEqual(mutation.get_database_amr_gene_mutation(), 'ins', 'Incorrect database amino acid')
        self.assertEqual(mutation.get_input_genome_mutation(), 'I', 'Incorrect query amino acid')
        self.assertEqual(mutation.get_mutation_string_short(), 'ins2I', 'Incorrect string')