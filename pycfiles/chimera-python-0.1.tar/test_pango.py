# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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