# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\registry\tests\test_processorindex.py
# Compiled at: 2010-12-23 17:42:44
from seishub.core.core import Component, implements
from seishub.core.packages.interfaces import IProcessorIndex, IPackage, IResourceType
from seishub.core.test import SeisHubEnvironmentTestCase
from seishub.core.xmldb import index
from seishub.core.xmldb.resource import newXMLDocument
import unittest
RAW_XML1 = '\n<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <paramXY>20.5</paramXY>\n        <paramXY>11.5</paramXY>\n        <paramXY>blah</paramXY>\n    </XY>\n    <creation_date>%s</creation_date>\n    <bool>%s</bool>\n</station>\n'

class ProcessorIndexTestPackage(Component):
    implements(IPackage)
    package_id = 'processorindextest'


class ProcessorIndexTestResourcetype(Component):
    implements(IResourceType)
    package_id = 'processorindextest'
    resourcetype_id = 'testtype'


class TestIndex(Component):
    implements(IProcessorIndex)
    package_id = 'processorindextest'
    resourcetype_id = 'testtype'
    type = index.FLOAT_INDEX
    label = 'testindex'

    def eval(self, document):
        return [
         1, 2, 3]


class ProcessorIndexTest(SeisHubEnvironmentTestCase):

    def setUp(self):
        self.env.enableComponent(ProcessorIndexTestPackage)
        self.env.enableComponent(ProcessorIndexTestResourcetype)

    def tearDown(self):
        self.env.disableComponent(ProcessorIndexTestPackage)
        self.env.disableComponent(ProcessorIndexTestResourcetype)

    def test_registerProcessorIndex(self):
        self.env.enableComponent(TestIndex)
        indexes = self.env.catalog.index_catalog.getIndexes(package_id='processorindextest', resourcetype_id='testtype')
        self.assertEqual(len(indexes), 1)
        idx = indexes[0]
        self.assertEqual(idx.resourcetype.package.package_id, 'processorindextest')
        self.assertEqual(idx.resourcetype.resourcetype_id, 'testtype')
        self.assertEqual(idx.type, index.PROCESSOR_INDEX)
        self.assertEqual(idx.options, TestIndex.__module__ + '.' + TestIndex.__name__)
        test_doc = newXMLDocument(RAW_XML1)
        res = idx.eval(test_doc, self.env)
        self.assertEqual(len(res), 3)
        self.assertEqual(type(res[0]), index.FloatIndexElement)
        self.assertEqual(type(res[1]), index.FloatIndexElement)
        self.assertEqual(type(res[2]), index.FloatIndexElement)
        self.assertEqual(res[0].key, 1)
        self.assertEqual(res[1].key, 2)
        self.assertEqual(res[2].key, 3)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ProcessorIndexTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')