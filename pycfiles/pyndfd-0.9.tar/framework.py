# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyndexter/tests/framework.py
# Compiled at: 2007-02-14 00:40:25
import unittest
from pyndexter import *
from pyndexter.sources.mock import MockSource
from pyndexter.indexers.mock import MockIndexer
from pyndexter.indexers.tests import IndexerTestCase

class FrameworkTestCase(IndexerTestCase):
    __module__ = __name__

    def setUp(self):
        self.framework = Framework('mock://')
        self.framework.add_source('mock://')

    def tearDown(self):
        pass

    def test_indexer_uri(self):
        self.assertTrue(isinstance(self.framework.indexer, MockIndexer))
        self.assertTrue(isinstance(self.framework.source.sources[0], MockSource))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FrameworkTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')