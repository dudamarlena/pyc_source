# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/UnitTests/TestTranslation.py
# Compiled at: 2019-02-16 11:54:37
# Size of source mod 2**32: 3623 bytes
from __future__ import print_function
import unittest, random, numpy as np

class TestTranslation(unittest.TestCase):

    def setUp(self):
        import pdbparser
        self._TestTranslation__pdbData = pdbparser.pdbparser()
        self._TestTranslation__pdbData.records = __import__('Utilities.Database', fromlist=['__WATER__']).__WATER__
        self._TestTranslation__method = __import__('Utilities.Geometry', fromlist=['translate']).translate

    def test_X(self):
        from Utilities.Information import get_coordinates
        originalCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        sign = np.sign(random.random() - 0.5)
        value = sign * random.random()
        self._TestTranslation__method(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData, [value, 0, 0])
        translatedCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        self.assertTrue((np.sum(translatedCoordinates - [value, 0, 0] - originalCoordinates) < 1e-05), msg='Translation along X')

    def test_Y(self):
        from Utilities.Information import get_coordinates
        originalCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        sign = np.sign(random.random() - 0.5)
        value = sign * random.random()
        self._TestTranslation__method(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData, [0, value, 0])
        translatedCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        self.assertTrue((np.sum(translatedCoordinates - [0, value, 0] - originalCoordinates) < 1e-05), msg='Translation along Y')

    def test_Z(self):
        from Utilities.Information import get_coordinates
        originalCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        sign = np.sign(random.random() - 0.5)
        value = sign * random.random()
        self._TestTranslation__method(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData, [0, value, 0])
        translatedCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        self.assertTrue((np.sum(translatedCoordinates - [0, 0, value] - originalCoordinates) < 1e-05), msg='Translation along Z')

    def test_XYZ(self):
        from Utilities.Information import get_coordinates
        originalCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        signX = np.sign(random.random() - 0.5)
        valueX = signX * random.random()
        signY = np.sign(random.random() - 0.5)
        valueY = signY * random.random()
        signZ = np.sign(random.random() - 0.5)
        valueZ = signZ * random.random()
        self._TestTranslation__method(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData, [valueX, valueY, valueZ])
        translatedCoordinates = np.transpose(get_coordinates(self._TestTranslation__pdbData._range(), self._TestTranslation__pdbData))
        self.assertTrue((np.sum(translatedCoordinates - [valueX, valueY, valueZ] - originalCoordinates) < 1e-05), msg='Translation along XYZ')


def main():
    unittest.main()


if __name__ == '__main__':
    import sys, os
    path = os.path.join(os.getcwd().split('pdbparser')[0], 'pdbparser')
    sys.path.insert(0, path)
    main()