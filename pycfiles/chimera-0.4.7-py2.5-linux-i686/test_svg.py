# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chimera/tests/test_svg.py
# Compiled at: 2007-02-08 13:55:31
import unittest, chimera

class TestChimeraSvg(unittest.TestCase):

    def test_toPNG(self):
        c = chimera.ChimeraSvg('logo.svg', 100, 100)
        assert c.width <= 100
        assert c.height <= 100
        c = chimera.ChimeraSvg('logo.svg', 512)
        assert c.width == 512
        assert c.height == 512
        c = chimera.ChimeraSvg('logo.svg')

    def test_maxSize(self):
        c = chimera.ChimeraSvg.atMaxSize('logo.svg', 512)
        assert c.width <= 512 and c.width > 500
        assert c.height <= 512

    def test_zoomMax(self):
        c = chimera.ChimeraSvg.atZoomWithMaxSize('logo.svg', 3, 3, 512, 100)
        assert c.width <= 512
        assert c.height <= 100


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestChimeraSvg))
    return suite


if __name__ == '__main__':
    unittest.main()