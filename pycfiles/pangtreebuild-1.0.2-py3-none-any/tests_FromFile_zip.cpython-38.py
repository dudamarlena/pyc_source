# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paulina/pangtree/pangtreebuild/tests/tests_pangenome/fasta_providers/tests_FromFile_zip.py
# Compiled at: 2019-12-30 15:48:57
# Size of source mod 2**32: 4019 bytes
import unittest
from pathlib import Path
from pangtreebuild.pangenome import graph
from pangtreebuild.pangenome.parameters import missings, msa

class FromFileFastaProviderFastaTests(unittest.TestCase):

    def setUp(self) -> None:
        self.fasta_dir = Path(__file__).parent.joinpath('files_zip/').resolve()

    @staticmethod
    def read_sequence--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'path'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           50  'to 50'
                8  STORE_FAST               'fasta_file_hanlder'

 L.  16        10  LOAD_FAST                'fasta_file_hanlder'
               12  LOAD_METHOD              readline
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               '_'

 L.  17        18  LOAD_FAST                'fasta_file_hanlder'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  LOAD_METHOD              upper
               26  CALL_METHOD_0         0  ''
               28  LOAD_METHOD              replace
               30  LOAD_STR                 '\n'
               32  LOAD_STR                 ''
               34  CALL_METHOD_2         2  ''
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH        6  '6'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38

    def raise_error_if_unequal(self, sequence_id: msa.SequenceID, expected_sequence: str, fasta_provider: missings.FromFile) -> None:
        for i, expected_symbol in enumerate(expected_sequence):
            expected_base = graph.Base(expected_symbol)
            actual_base = fasta_provider.get_basesequence_idi
            self.assertEqualexpected_baseactual_base

    def test_1_one_sequence_one_file_in_zip(self):
        fasta_path = self.fasta_dir.joinpath('test_1_one_sequence_one_file_in_zip.zip')
        fasta_provider = missings.FromFile(Path(fasta_path))
        sequence_id = msa.SequenceID('seq1')
        expected_sequence = 'ACTGGGTGGGA'
        self.raise_error_if_unequal(sequence_id, expected_sequence, fasta_provider)

    def test_2_three_sequences_in_two_files_in_zip(self):
        fasta_path = self.fasta_dir.joinpath('test_2_three_sequences_in_two_files_in_zip.zip')
        fasta_provider = missings.FromFile(Path(fasta_path))
        sequence_id_1 = msa.SequenceID('seq1')
        self.raise_error_if_unequal(sequence_id_1, 'ACTGGGTGGGA', fasta_provider)
        sequence_id_2 = msa.SequenceID('seq2')
        self.raise_error_if_unequal(sequence_id_2, 'AA', fasta_provider)
        sequence_id_3 = msa.SequenceID('seq3')
        self.raise_error_if_unequal(sequence_id_3, 'GT', fasta_provider)

    def test_3_empty_sequence_name(self):
        fasta_path = self.fasta_dir.joinpath('test_3_empty_sequence_name.zip')
        with self.assertRaises(Exception) as (exp):
            _ = missings.FromFile(Path(fasta_path))
        expected_message = 'No sequences in zipped fastas or incorrect zipped files.'
        actual_message = str(exp.exception)
        self.assertEqualexpected_messageactual_message

    def test_4_empty_sequence(self):
        fasta_path = self.fasta_dir.joinpath('test_4_empty_sequence.zip')
        with self.assertRaises(Exception) as (exp):
            _ = missings.FromFile(Path(fasta_path))
        expected_message = 'Empty sequence in FASTA. Provide the sequence or remove its header.'
        actual_message = str(exp.exception)
        self.assertEqualexpected_messageactual_message

    def test_5_empty_fasta(self):
        fasta_path = self.fasta_dir.joinpath('test_5_empty_fasta.zip')
        with self.assertRaises(Exception) as (exp):
            _ = missings.FromFile(Path(fasta_path))
        expected_message = 'No sequences in zipped fastas or incorrect zipped files.'
        actual_message = str(exp.exception)
        self.assertEqualexpected_messageactual_message

    def test_6_empty_zip(self):
        fasta_path = self.fasta_dir.joinpath('test_6_empty_zip.zip')
        with self.assertRaises(Exception) as (exp):
            _ = missings.FromFile(Path(fasta_path))
        expected_message = 'Incorrect zip fasta source.'
        actual_message = str(exp.exception)
        self.assertEqualexpected_messageactual_message

    def test_7_no_fasta_in_zip(self):
        fasta_path = self.fasta_dir.joinpath('test_7_no_fasta_in_zip.zip')
        with self.assertRaises(Exception) as (exp):
            _ = missings.FromFile(Path(fasta_path))
        expected_message = 'No sequences in zipped fastas or incorrect zipped files.'
        actual_message = str(exp.exception)
        self.assertEqualexpected_messageactual_message


if __name__ == '__main__':
    unittest.main()