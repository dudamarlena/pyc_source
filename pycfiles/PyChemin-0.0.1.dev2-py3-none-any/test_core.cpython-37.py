# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_core.py
# Compiled at: 2019-12-16 12:57:25
# Size of source mod 2**32: 2562 bytes
import pychemia, numpy as np, unittest

class TestCore(unittest.TestCase):
    """TestCore"""

    def test_composition_1(self):
        """
        Test (pychemia.core.composition)                            :
        """
        comp = pychemia.Composition('YBa2Cu3O7')
        self.assertEqual(sorted(comp.species), ['Ba', 'Cu', 'O', 'Y'])
        self.assertEqual(sorted(comp.symbols), [
         'Ba', 'Ba', 'Cu', 'Cu', 'Cu', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'Y'])
        self.assertEqual(comp.formula, 'Ba2Cu3O7Y')
        self.assertTrue(abs(comp.covalent_volume() - 285.185) < 1e-05)
        self.assertEqual(comp.natom, 13)
        self.assertEqual(comp.sorted_formula(sortby='hill'), 'Ba2Cu3O7Y')

    def test_composition_2(self):
        """
        Test (pychemia.core.composition)                            :
        """
        comp = pychemia.Composition('Na2Cl2')
        self.assertEqual(comp.symbols, ['Cl', 'Cl', 'Na', 'Na'])
        self.assertEqual(pychemia.utils.periodic.valence(comp.symbols), [7, 7, 1, 1])

    def test_structure(self):
        """
        Test (pychemia.core.structure)                              :
        """
        a = 4.05
        b = a / 2
        fcc = pychemia.Structure(symbols=['Au'], cell=[[0, b, b], [b, 0, b], [b, b, 0]], periodicity=True)
        self.assertEqual(fcc.natom, 1)
        fcc_copy = fcc.copy()
        fcc_copy.canonical_form()
        self.assertTrue(abs(fcc.volume - fcc_copy.volume) < 1e-13)
        self.assertTrue(np.linalg.norm(fcc_copy.lattice.angles - fcc.lattice.angles) < 1e-10)
        spc = fcc.supercell((3, 3, 3))
        self.assertEqual(spc.natom, 27)

    def test_from_file_1(self):
        """
        Test (pychemia.core.from_file)                              :
        """
        filename = 'tests/data/vasp_07/POSCAR_new'
        st = pychemia.structure_from_file(filename)
        self.assertEqual(st.nsites, 44)

    def test_from_file_2(self):
        """
        Test (pychemia.core.from_file)                              :
        """
        filename = 'tests/data/abinit_05/abinit.in'
        st = pychemia.structure_from_file(filename)
        self.assertEqual(st.nsites, 20)

    def test_from_file_3(self):
        """
        Test (pychemia.core.from_file)                              :
        """
        filename = 'tests/data/abinit_05/structure.json'
        st = pychemia.structure_from_file(filename)
        self.assertEqual(st.nsites, 20)