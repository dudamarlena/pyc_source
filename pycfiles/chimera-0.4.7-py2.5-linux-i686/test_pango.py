# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chimera/tests/test_pango.py
# Compiled at: 2007-02-08 13:55:31
import unittest, chimera.pangocairo as pangocairo

class TestChimeraPango(unittest.TestCase):

    def test_toPNG(self):
        i = pangocairo.ImageSurface('argb', 640, 256)
        p = pangocairo.CairoContext(i)
        c.antialias = 'subpixel'
        c.hint_style = 'strong'
        c.hint_metrics = 'on'
        (l, t) = c.layout(text, font)
        l.show()
        assert i.toPngBuffer()

    def test_families(self):
        i = pangocairo.ImageSurface('argb', 640, 256)
        p = pangocairo.CairoContext(i)
        fonts = p.listFontFamilies()
        assert 'Sans' in fonts
        assert 'Serif' in fonts
        assert 'Monospace' in fonts


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestChimeraPango))
    return suite


if __name__ == '__main__':
    unittest.main()