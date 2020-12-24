# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/tests/excerpt.py
# Compiled at: 2007-02-13 10:43:30
import unittest
from pyndexter import *
from pyndexter.tests.corpus import documents, corpus

class ExcerptTestCase(unittest.TestCase):
    __module__ = __name__

    def test_excerpt(self):
        terms = Query('lorem ipsum').terms()
        excerpt = Excerpt(documents['mock://3'], terms)
        self.assertEquals(unicode(excerpt), '...  Etiam pharetra. Vivamus diam ipsum, luctus et, luctus nec, auctor vel,\ntellus. Vestibulum lobortis feugiat dolor. Phasellus diam felis, commodo vitae,\nlaoreet ac, euismod sit amet, nunc. Vestibulum ut metus. Praesent vel nibh ac\nlibero convallis imperdiet. Morbi dignis ...')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ExcerptTestCase, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')