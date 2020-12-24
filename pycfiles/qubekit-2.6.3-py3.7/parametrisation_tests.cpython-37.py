# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/tests/parametrisation_tests.py
# Compiled at: 2019-09-30 09:58:49
# Size of source mod 2**32: 2011 bytes
from QUBEKit.ligand import Ligand
from QUBEKit.parametrisation import AnteChamber, OpenFF
import os
from shutil import copy, rmtree
import unittest

class ParametrisationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.files_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
        os.mkdir('temp')
        os.chdir('temp')
        copy(os.path.join(cls.files_folder, 'acetone.pdb'), 'acetone.pdb')
        cls.molecule = Ligand('acetone.pdb')

    def test_antechamber(self):
        AnteChamber(self.molecule)
        self.assertEqual(len(self.molecule.HarmonicBondForce), len(list(self.molecule.topology.edges)))
        self.assertEqual(len(self.molecule.HarmonicAngleForce), len(self.molecule.angles))
        self.assertEqual(len(self.molecule.PeriodicTorsionForce), len(self.molecule.dih_phis) + len(self.molecule.improper_torsions))
        self.assertEqual(len(self.molecule.coords['input']), len(self.molecule.NonbondedForce))

    def test_OpenFF(self):
        OpenFF(self.molecule)
        self.assertEqual(len(self.molecule.HarmonicBondForce), len(list(self.molecule.topology.edges)))
        self.assertEqual(len(self.molecule.HarmonicAngleForce), len(self.molecule.angles))
        self.assertEqual(len(self.molecule.PeriodicTorsionForce), len(self.molecule.dih_phis) + len(self.molecule.improper_torsions))
        self.assertEqual(len(self.molecule.coords['input']), len(self.molecule.NonbondedForce))

    @classmethod
    def tearDownClass(cls):
        """Remove the files produced during testing"""
        os.chdir('../')
        rmtree('temp')


if __name__ == '__main__':
    unittest.main()