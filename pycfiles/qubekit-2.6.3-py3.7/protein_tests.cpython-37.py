# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/tests/protein_tests.py
# Compiled at: 2019-09-16 10:20:01
# Size of source mod 2**32: 978 bytes
from QUBEKit.ligand import Protein
import os
from shutil import copy, rmtree
import unittest

class TestProteins(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.files_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
        os.mkdir('temp')
        os.chdir('temp')
        copy(os.path.join(cls.files_folder, 'capped_leu.pdb'), 'capped_leu.pdb')
        cls.molecule = Protein('capped_leu.pdb')

    def test_xml_generation(self):
        self.assertEqual(len(self.molecule.atoms), 31)
        self.assertEqual(len(self.molecule.topology.edges), len(self.molecule.bond_lengths))

    @classmethod
    def tearDownClass(cls):
        """Remove the files produced during testing"""
        os.chdir('../')
        rmtree('temp')


if __name__ == '__main__':
    unittest.main()