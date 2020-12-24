# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_crystal_kpoints.py
# Compiled at: 2020-01-17 14:32:16
# Size of source mod 2**32: 1240 bytes
import pychemia, unittest

class KPointsTest(unittest.TestCase):

    def test_optimized_grid(self):
        """
        Test (pychemia.crystal.kpoints)                             :
        """
        st = pychemia.code.vasp.read_poscar('tests/data/SbBi/POSCAR')
        kp = pychemia.crystal.KPoints.optimized_grid(st.lattice)
        self.assertEqual(kp.grid, [11, 11, 11])
        self.assertEqual(kp.get_density_of_kpoints(st.lattice), 93126.88854794503)
        kpdict = kp.to_dict
        kp2 = kp.from_dict(kpdict)
        self.assertEqual(kp.grid, kp2.grid)
        kp = pychemia.crystal.KPoints(kmode='path', kvertices=[
         [
          0, 0, 0], [0.5, 0.5, 0], [0.5, 0.5, 0.5], [0, 0, 0]],
          intermediates=10)
        self.assertEqual(kp.number_of_kpoints, 40)
        kp = pychemia.crystal.KPoints(kmode='reduced')
        kp.add_kpt([0, 0, 0], weight=0.5)
        self.assertEqual(kp.nkpt, 1)
        kp.add_kpt([0.5, 0.5, 0.5], weight=0.5)
        print(kp)
        self.assertEqual(kp.number_of_kpoints, 2)
        kp.set_kpoints_list([[0.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])
        self.assertEqual(kp.number_of_kpoints, 4)