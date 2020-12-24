# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zjshao/Documents/repos/VASPy/tests/oszicar_test.py
# Compiled at: 2017-06-01 02:14:07
# Size of source mod 2**32: 1644 bytes
"""
    OsziCar类单元测试.
"""
import os, unittest, numpy as np, matplotlib
matplotlib.use('Agg')
from vaspy.iter import OsziCar
from tests import abs_path

class OsziCarTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_attrs(self):
        """Make sure load() effects"""
        filename = abs_path + '/testdata/OSZICAR'
        oszicar = OsziCar(filename)
        for var in oszicar.vars:
            self.assertTrue(hasattr(oszicar, var))

        self.assertRaises(AttributeError)

    def test_esort(self):
        """Make sure the esort() effects"""
        filename = abs_path + '/testdata/OSZICAR'
        oszicar = OsziCar(filename)
        srted = oszicar.esort('E0', 2)
        shouldbe = np.array([(-101.21186, 326), (-101.21116, 324)], dtype=[
         ('var', '<f8'), ('step', '<i4')])
        srted = srted.tolist()
        shouldbe = shouldbe.tolist()
        self.assertTrue(srted == shouldbe)

    def test_plot(self):
        """Make sure object could plot"""
        filename = abs_path + '/testdata/OSZICAR'
        oszicar = OsziCar(filename)
        plot = oszicar.plot('E0', mode='save')
        self.assertTrue(isinstance(plot, matplotlib.figure.Figure))
        os.remove('E0_vs_step.png')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OsziCarTest)
    unittest.TextTestRunner(verbosity=2).run(suite)