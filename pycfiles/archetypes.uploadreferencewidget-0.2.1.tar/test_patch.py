# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/schematuning/tests/test_patch.py
# Compiled at: 2010-01-22 07:59:46
import unittest
from archetypes.schematuning.patch import cache_key
from archetypes.schematuning.patch import _Schema
from base import SchemaTuningTestCase

class TestPatch(SchemaTuningTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_cache_keys(self):
        """ Test that the cache keys for two docs are the same.
        """
        id = self.portal.invokeFactory('Document', 'doc1')
        doc1 = self.portal._getOb(id)
        self.portal.invokeFactory('Document', 'do2c')
        doc2 = self.portal._getOb(id)
        key1 = cache_key(_Schema, doc1)
        key2 = cache_key(_Schema, doc2)
        self.assertEquals(key1, key2)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPatch))
    return suite