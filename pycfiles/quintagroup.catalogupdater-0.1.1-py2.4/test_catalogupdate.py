# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/catalogupdater/exportimport/tests/test_catalogupdate.py
# Compiled at: 2010-07-14 11:48:19
import unittest
from zope.component import getMultiAdapter
from zope.component import provideUtility
from Products.Five import zcml
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.ZCatalog.tests import test_exportimport
from Products.GenericSetup.testing import DummyLogger
from Products.GenericSetup.testing import DummySetupEnviron
from quintagroup.catalogupdater.interfaces import ICatalogUpdater
from Products.CMFPlone.utils import getFSVersionTuple
PLONEFOUR = getFSVersionTuple()[0] == 4 and True or False
_CATALOG_BODY = test_exportimport._CATALOG_BODY
_ZCTEXT_XML = test_exportimport._ZCTEXT_XML
_CATALOG_UPDATE_BODY = '<?xml version="1.0"?>\n<object name="foo_catalog">\n %s\n <index name="foo_text" remove="True"/>\n <index name="foo_text" meta_type="ZCTextIndex">\n  <indexed_attr value="foo_text"/>\n  <extra name="index_type" value="Okapi BM25 Rank"/>\n  <extra name="lexicon_id" value="foo_plexicon"/>\n </index>\n <index name="non_existing" remove="True"/>\n <column value="non_existing" remove="True"/>\n <column value="bacon" remove="True"/>\n <column value="eggs" update="True"/>\n <column value="spam" update="True"/>\n</object>\n' % (PLONEFOUR and '<object name="old_plexicon" remove="True"/>' or '<object name="foo_vocabulary" remove="True"/>')

class DummyCatalogUpdaterUtility:
    __module__ = __name__
    _logger = None

    def updateMetadata4All(self, catalog, columns):
        self._logger.info('%s:%s' % (catalog.id, columns))


class CatalogUpdaterZCMLLayer(test_exportimport.ZCatalogXMLAdapterTests.layer):
    __module__ = __name__

    @classmethod
    def setUp(cls):
        test_exportimport.ZCatalogXMLAdapterTests.layer.setUp()
        import quintagroup.catalogupdater
        zcml.load_config('overrides.zcml', quintagroup.catalogupdater)


class CatalogUpdaterXMLAdapterTest(test_exportimport.ZCatalogXMLAdapterTests):
    __module__ = __name__
    layer = CatalogUpdaterZCMLLayer

    def _getTargetClass(self):
        from quintagroup.catalogupdater.exportimport.catalogupdater import CatalogUpdaterXMLAdapter
        return CatalogUpdaterXMLAdapter

    def setUp(self):
        super(CatalogUpdaterXMLAdapterTest, self).setUp()
        self.logger = DummyLogger('CatalogUpdaterLogger', [])
        dummy_cu = DummyCatalogUpdaterUtility()
        dummy_cu._logger = self.logger
        provideUtility(dummy_cu, ICatalogUpdater, name='catalog_updater')

    def getLastMessage(self):
        messages = getattr(self.logger, '_messages', [])
        return messages[(-1)] or [None] * 3

    def test_body_set_update(self):
        self._populate_special(self._obj)
        context = DummySetupEnviron()
        context._should_purge = False
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = _CATALOG_UPDATE_BODY
        self.assertEqual(adapted.body, _CATALOG_BODY % ('', _ZCTEXT_XML, ''))
        message = self.getLastMessage()
        self.assertEqual(message[(-1)], "foo_catalog:['eggs', 'spam']", 'Not updated columns in catalog')


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(CatalogUpdaterXMLAdapterTest),))


if __name__ == '__main__':
    from Products.GenericSetup.testing import run
    run(test_suite())