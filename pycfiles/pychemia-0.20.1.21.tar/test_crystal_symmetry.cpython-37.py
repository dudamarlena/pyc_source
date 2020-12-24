# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_crystal_symmetry.py
# Compiled at: 2020-01-17 14:47:28
# Size of source mod 2**32: 717 bytes
import pychemia, unittest, numpy as np

class CrystalSymmetryTest(unittest.TestCase):

    def test_optimized_grid(self):
        """
        Test (pychemia.crystal.symmetry)                            :
        """
        from pychemia import pcm_log
        pcm_log.debug('CrystalSymmetryTest')
        st = pychemia.code.vasp.read_poscar('tests/data/SbBi/POSCAR')
        cs = pychemia.crystal.CrystalSymmetry(st)
        assert cs.number() == 160
        assert cs.symbol() == 'R3m'
        pr = cs.find_primitive()
        assert np.abs(st.volume - pr.volume) < 1e-06
        assert cs.crystal_system() == 'Trigonal'
        ss = cs.symmetrize()
        assert np.abs(st.volume - ss.volume) < 1e-06