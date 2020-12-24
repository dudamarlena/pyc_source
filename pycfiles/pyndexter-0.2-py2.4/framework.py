# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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