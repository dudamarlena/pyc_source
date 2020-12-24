# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/UnitTests/TestConnectivity.py
# Compiled at: 2019-02-16 11:54:35
# Size of source mod 2**32: 3286 bytes
from __future__ import print_function
import os, unittest, random, copy, numpy as np

class TestTranslation(unittest.TestCase):

    def setUp(self):
        import pdbparser
        from Utilities.Collection import get_path
        pdbparserPath = get_path('pdbparser_path')
        self._TestTranslation__pdb = pdbparser.pdbparser(os.path.join(pdbparserPath, 'Data', 'connectivityTestMolecule.pdb'))
        self._TestTranslation__method = __import__('Utilities.Connectivity', fromlist=['Connectivity']).Connectivity
        self._TestTranslation__bonds = [
         [
          1], [2], [3, 9], [5], [5, 7], [6], [], [8], [], [10], [11, 12], [], [13, 14, 15], [], [], []]
        self._TestTranslation__angles = [[0, 1, 2], [1, 2, 3], [1, 2, 9], [3, 2, 9], [2, 3, 5], [2, 9, 10], [3, 5, 6], [5, 4, 7], [4, 5, 6], [4, 7, 8], [9, 10, 11], [9, 10, 12], [11, 10, 12], [10, 12, 13], [10, 12, 14], [10, 12, 15], [13, 12, 14], [13, 12, 15], [14, 12, 15]]
        self._TestTranslation__dihedrals = [[0, 1, 2, 3], [0, 1, 2, 9], [1, 2, 3, 5], [1, 2, 9, 10], [5, 3, 2, 9], [3, 2, 9, 10], [2, 3, 5, 6], [2, 9, 10, 11], [2, 9, 10, 12], [6, 5, 4, 7], [5, 4, 7, 8], [9, 10, 12, 13], [9, 10, 12, 14], [9, 10, 12, 15], [11, 10, 12, 13], [11, 10, 12, 14], [11, 10, 12, 15]]

    def test_bonds(self):
        connectivity = self._TestTranslation__method(self._TestTranslation__pdb)
        connectivity.calculate_bonds()
        bonds = connectivity.get_bonds()[1]
        trueBonds = copy.copy(self._TestTranslation__bonds)
        while bonds:
            bond = bonds.pop(0)
            self.assertTrue(bond in trueBonds)
            trueBonds.remove(bond)

        self.assertTrue(not trueBonds)

    def test_angles(self):
        connectivity = self._TestTranslation__method(self._TestTranslation__pdb)
        connectivity.calculate_angles()
        angles = connectivity.get_angles()
        trueAngles = copy.copy(self._TestTranslation__angles)
        while angles:
            angle = angles.pop(0)
            self.assertTrue(angle in trueAngles)
            trueAngles.remove(angle)

        self.assertTrue(not trueAngles)

    def test_dihedrals(self):
        connectivity = self._TestTranslation__method(self._TestTranslation__pdb)
        connectivity.calculate_dihedrals()
        dihedrals = connectivity.get_dihedrals()
        trueDihedrals = copy.copy(self._TestTranslation__dihedrals)
        while dihedrals:
            dihedral = dihedrals.pop(0)
            self.assertTrue(dihedral in trueDihedrals)
            trueDihedrals.remove(dihedral)

        self.assertTrue(not trueDihedrals)


def main():
    unittest.main()


if __name__ == '__main__':
    import sys, os
    path = os.path.join(os.getcwd().split('pdbparser')[0], 'pdbparser')
    sys.path.insert(0, path)
    main()