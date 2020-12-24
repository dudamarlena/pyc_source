# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paulina/pangtree/pangtreebuild/tests/tests_pangenome/fasta_providers/tests_FromNcbiProvider.py
# Compiled at: 2019-12-30 15:48:57
# Size of source mod 2**32: 2455 bytes
import unittest
from pathlib import Path
from ddt import unpack, data, ddt
from pangtreebuild.pangenome import graph
from pangtreebuild.pangenome.parameters import missings, msa

@ddt
class FromNCBITests(unittest.TestCase):

    def setUp(self) -> None:
        self.fasta_dir = Path(__file__).parent.joinpath('fasta_ncbi/').resolve()
        self.fasta_provider = missings.FromNCBI(use_cache=False)

    def test_0_get_10th_symbol_of_AB050936v1(self):
        sequence_id = msa.SequenceID('AB050936.1')
        actual_base = self.fasta_provider.get_base(sequence_id, 10)
        path = self.fasta_dir.joinpath('AB050936.1.fasta')
        expected_base = graph.Base(self.read_sequence(path)[10])
        self.assertEqual(expected_base, actual_base)

    def test_1_download_AB050936v1(self):
        fasta_provider = missings.FromNCBI(use_cache=False)
        sequence_id = msa.SequenceID('AB050936.1')
        actual_sequence = fasta_provider._download_from_ncbi(sequence_id)
        p = self.fasta_dir.joinpath('AB050936.1.fasta')
        expected_sequence = self.read_sequence(p)
        self.assertEqual(expected_sequence, actual_sequence)

    def test_2_failed_download(self):
        fasta_provider = missings.FromNCBI(use_cache=False)
        sequence_id = ''
        with self.assertRaises(Exception) as (err):
            _ = fasta_provider._download_from_ncbi(msa.SequenceID(sequence_id))
            self.assertEqual(str(err), f"Cannot download from Entrez sequence of ID: {sequence_id}")

    @data((msa.SequenceID('plain'), 'plain'), (
     msa.SequenceID('withv1'), 'with.1'))
    @unpack
    def test_3_guess_entrez_id(self, sequenceID: msa.SequenceID, expected_guessed_entrez_id: str):
        fasta_provider = missings.FromNCBI(use_cache=False)
        actual_guessed_entrez_id = fasta_provider._guess_ncbi_sequence_id(sequenceID)
        self.assertEqual(expected_guessed_entrez_id, actual_guessed_entrez_id)

    @staticmethod
    def read_sequence--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'path'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           50  'to 50'
                8  STORE_FAST               'fasta_file_hanlder'

 L.  53        10  LOAD_FAST                'fasta_file_hanlder'
               12  LOAD_METHOD              readline
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               '_'

 L.  54        18  LOAD_FAST                'fasta_file_hanlder'
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


if __name__ == '__main__':
    unittest.main()