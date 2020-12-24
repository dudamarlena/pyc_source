# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\xmldb\tests\test_xmlindexcatalog.py
# Compiled at: 2011-01-03 17:15:12
from seishub.core.exceptions import DuplicateObjectError, NotFoundError
from seishub.core.test import SeisHubEnvironmentTestCase
from seishub.core.xmldb.index import XmlIndex, DATETIME_INDEX, FLOAT_INDEX
from seishub.core.xmldb.resource import Resource, newXMLDocument
from seishub.core.xmldb.xpath import XPathQuery
import os, unittest
RAW_XML1 = '<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n</station>'
RAW_XML2 = '<station rel_uri="genf">\n    <station_code>GENF</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>22.51200</lon>\n    <lat>55.23200</lat>\n    <stat_elav>0.73500</stat_elav>\n    <XY>\n        <paramXY>2.5</paramXY>\n        <paramXY>0</paramXY>\n        <paramXY>99</paramXY>\n    </XY>\n    <test_date>20081212010102.123456789</test_date>\n    <test_date2>20081212010102.050300000</test_date2>\n</station>'
RAW_XML3 = '<?xml version="1.0"?>\n<testml>\n<res_link>BERN</res_link>\n<blah1 id="3"><blahblah1>blahblahblah</blahblah1></blah1>\n</testml>\n'
RAW_XML4 = '\n<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <X>1</X>\n        <Y id = "1">2</Y>\n        <Z>\n            <value>3</value>\n        </Z>\n    </XY>\n    <XY>\n        <X>4</X>\n        <Y id = "2">5</Y>\n        <Z>\n            <value>6</value>\n        </Z>\n    </XY>\n    <creation_date>%s</creation_date>\n    <bool>%s</bool>\n</station>\n'
URI1 = '/real/bern'
URI2 = '/fake/genf'
URI3 = '/testml/res1'
IDX1 = '/station/lon'
IDX2 = '/station/lat'
IDX3 = '/testml/blah1/@id'
IDX4 = '/station/XY/paramXY'
so_tests = [
 'so1.xml', 'so2.xml', 'so3.xml', 'so4.xml', 'so5.xml']
so_indexes = [
 '/sortorder/int1',
 '/sortorder/int2',
 '/sortorder/str1',
 '/sortorder/str2']

class XmlIndexCatalogTest(SeisHubEnvironmentTestCase):
    """
    """

    def setUp(self):
        self.catalog = self.env.catalog.index_catalog
        self.xmldb = self.env.catalog.xmldb
        self.so_res = list()
        self.pkg1 = self.env.registry.db_registerPackage('testpackage')
        self.rt1 = self.env.registry.db_registerResourceType('testpackage', 'station')
        self.rt2 = self.env.registry.db_registerResourceType('testpackage', 'testml')
        self.rt3 = self.env.registry.db_registerResourceType('testpackage', 'testtype')
        self.pkg2 = self.env.registry.db_registerPackage('sortordertests')
        self.rt4 = self.env.registry.db_registerResourceType('sortordertests', 'sotest')

    def tearDown(self):
        self.env.registry.db_deleteResourceType('testpackage', 'station')
        self.env.registry.db_deleteResourceType('testpackage', 'testml')
        self.env.registry.db_deleteResourceType('testpackage', 'testtype')
        self.env.registry.db_deletePackage('testpackage')
        self.env.registry.db_deleteResourceType('sortordertests', 'sotest')
        self.env.registry.db_deletePackage('sortordertests')

    def _setup_testdata(self):
        self.res1 = self.env.catalog.addResource(self.pkg1.package_id, self.rt1.resourcetype_id, RAW_XML1, name='RAW_XML1')
        self.res2 = self.env.catalog.addResource(self.pkg1.package_id, self.rt1.resourcetype_id, RAW_XML2, name='RAW_XML2')
        self.res3 = self.env.catalog.addResource(self.pkg1.package_id, self.rt2.resourcetype_id, RAW_XML3, name='RAW_XML3')
        self.idx1 = self.env.catalog.registerIndex('testpackage', 'station', 'longitude', IDX1)
        self.idx2 = self.env.catalog.registerIndex('testpackage', 'station', 'latitude', IDX2)
        self.idx3 = self.env.catalog.registerIndex('testpackage', 'testml', 'blah_id', IDX3)
        self.idx4 = self.env.catalog.registerIndex('testpackage', 'station', 'paramXY', IDX4)
        self.idx5 = self.env.catalog.registerIndex('testpackage', 'station', '5', '/station', type='boolean')
        self.env.catalog.reindexIndex(self.idx1)
        self.env.catalog.reindexIndex(self.idx2)
        self.env.catalog.reindexIndex(self.idx3)
        self.env.catalog.reindexIndex(self.idx4)
        self.env.catalog.reindexIndex(self.idx5)
        path = os.path.dirname(__file__)
        test_path = os.path.join(path, 'data')
        for f in so_tests:
            fh = open(test_path + os.sep + f, 'r')
            data = fh.read()
            fh.close()
            res = self.env.catalog.addResource('sortordertests', 'sotest', data)
            self.so_res.append(res)

        self.idx_so = []
        for i in so_indexes:
            idx = self.env.catalog.registerIndex('sortordertests', 'sotest', i[-4:], i)
            self.idx_so.append(idx)
            self.env.catalog.reindexIndex(idx)

    def _cleanup_testdata(self):
        """
        """
        self.env.catalog.deleteIndex(self.idx1)
        self.env.catalog.deleteIndex(self.idx2)
        self.env.catalog.deleteIndex(self.idx3)
        self.env.catalog.deleteIndex(self.idx4)
        self.env.catalog.deleteIndex(self.idx5)
        self.env.catalog.deleteResource(self.res1)
        self.env.catalog.deleteResource(self.res2)
        self.env.catalog.deleteResource(self.res3)
        for idx in self.idx_so:
            self.env.catalog.deleteIndex(idx)

        for res in self.so_res:
            self.env.catalog.deleteResource(res)

    def test_registerIndex(self):
        """
        """
        index = XmlIndex(self.rt1, '/station/XY/paramXY', DATETIME_INDEX, '%Y/%m', label='test')
        self.catalog.registerIndex(index)
        res = self.catalog.getIndexes(package_id=self.rt1.package.package_id, resourcetype_id=self.rt1.resourcetype_id, xpath='/station/XY/paramXY')[0]
        self.assertEquals(res.resourcetype.resourcetype_id, self.rt1.resourcetype_id)
        self.assertEquals(res.xpath, '/station/XY/paramXY')
        self.assertEquals(res.type, DATETIME_INDEX)
        self.assertEquals(res.options, '%Y/%m')
        self.assertRaises(DuplicateObjectError, self.catalog.registerIndex, index)
        self.catalog.deleteIndex(index)

    def test_deleteIndex(self):
        """
        """
        index = XmlIndex(self.rt1, '/station/XY/paramXY', label='test')
        self.catalog.registerIndex(index)
        res = self.catalog.getIndexes(package_id=self.rt1.package.package_id, resourcetype_id=self.rt1.resourcetype_id, xpath='/station/XY/paramXY')
        self.assertEquals(len(res), 1)
        self.catalog.deleteIndex(index)
        res = self.catalog.getIndexes(package_id=self.rt1.package.package_id, resourcetype_id=self.rt1.resourcetype_id, xpath='/station/XY/paramXY')
        self.assertEquals(len(res), 0)

    def test_getIndexes(self):
        """
        """
        index_rt1 = XmlIndex(self.rt1, '/station/XY/paramXY', label='id1')
        index2_rt1 = XmlIndex(self.rt1, '/station/station_code', label='id2')
        index_rt2 = XmlIndex(self.rt2, '/station/XY/paramXY', label='id3')
        self.catalog.registerIndex(index_rt1)
        self.catalog.registerIndex(index2_rt1)
        self.catalog.registerIndex(index_rt2)
        res = self.catalog.getIndexes(package_id=self.rt1.package.package_id, resourcetype_id=self.rt1.resourcetype_id)
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0].resourcetype.resourcetype_id, self.rt1.resourcetype_id)
        self.assertEquals(res[0].xpath, index_rt1.xpath)
        self.assertEquals(res[1].resourcetype.resourcetype_id, self.rt1.resourcetype_id)
        self.assertEquals(res[1].xpath, index2_rt1.xpath)
        res = self.catalog.getIndexes(package_id=self.rt2.package.package_id, resourcetype_id=self.rt2.resourcetype_id)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0].resourcetype.resourcetype_id, self.rt2.resourcetype_id)
        self.assertEquals(res[0].xpath, index_rt2.xpath)
        res = self.catalog.getIndexes(xpath='/station/XY/paramXY')
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0].resourcetype.resourcetype_id, self.rt1.resourcetype_id)
        self.assertEquals(res[0].xpath, index_rt1.xpath)
        self.assertEquals(res[1].resourcetype.resourcetype_id, self.rt2.resourcetype_id)
        self.assertEquals(res[1].xpath, index_rt2.xpath)
        res = self.catalog.getIndexes(xpath='/station/station_code')
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0].resourcetype.resourcetype_id, self.rt1.resourcetype_id)
        self.assertEquals(res[0].xpath, index2_rt1.xpath)
        res = self.catalog.getIndexes(package_id=self.rt1.package.package_id, resourcetype_id=self.rt1.resourcetype_id, xpath='/station/XY/paramXY')
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0].resourcetype.resourcetype_id, self.rt1.resourcetype_id)
        self.assertEquals(res[0].xpath, '/station/XY/paramXY')
        self.catalog.deleteIndex(index_rt1)
        self.catalog.deleteIndex(index2_rt1)
        self.catalog.deleteIndex(index_rt2)

    def test_indexResource(self):
        res = Resource(self.rt1, document=newXMLDocument(RAW_XML2))
        self.xmldb.addResource(res)
        index1 = XmlIndex(self.rt1, '/station/station_code', label='idx1')
        index2 = XmlIndex(self.rt1, '/station/XY/paramXY', label='idx2')
        index3 = XmlIndex(self.rt1, '/station/test_date', FLOAT_INDEX)
        self.catalog.registerIndex(index1)
        self.catalog.registerIndex(index2)
        self.catalog.registerIndex(index3)
        r = self.catalog.indexResource(res)
        self.assertEquals(len(r), 5)
        el = self.catalog.dumpIndex(index1)
        self.assertEquals(len(el), 1)
        self.assertEquals(el[0].key, 'GENF')
        self.assertEquals(el[0].document.data, res.document.data)
        el = self.catalog.dumpIndex(index2)
        self.assertEqual(len(el), 3)
        keys = ['0', '2.5', '99']
        for e in el:
            assert e.key in keys
            keys.remove(e.key)
            self.assertEquals(e.document.data, res.document.data)

        el = self.catalog.dumpIndexByResource(res)
        self.assertEqual(len(el), 5)
        self.assertEquals(el[0].key, 'GENF')
        self.assertEquals(el[0].document.data, res.document.data)
        self.assertEquals(el[0].index.xpath, '/station/station_code')
        self.assertTrue(el[1].key in ('0', '2.5', '99'))
        self.assertEquals(el[1].document.data, res.document.data)
        self.assertEquals(el[1].index.xpath, '/station/XY/paramXY')
        self.assertTrue(el[2].key in ('0', '2.5', '99'))
        self.assertEquals(el[2].document.data, res.document.data)
        self.assertEquals(el[2].index.xpath, '/station/XY/paramXY')
        self.assertTrue(el[3].key in ('0', '2.5', '99'))
        self.assertEquals(el[3].document.data, res.document.data)
        self.assertEquals(el[3].index.xpath, '/station/XY/paramXY')
        self.assertEquals(el[4].key, 20081212010102.125)
        self.assertEquals(el[4].document.data, res.document.data)
        self.assertEquals(el[4].index.xpath, '/station/test_date')
        self.catalog.deleteIndex(index1)
        self.catalog.deleteIndex(index2)
        self.catalog.deleteIndex(index3)
        self.xmldb.deleteResource(res)

    def test_indexResourceWithGrouping(self):
        res = Resource(self.rt1, document=newXMLDocument(RAW_XML4))
        self.xmldb.addResource(res)
        index = XmlIndex(self.rt1, '/station/XY/Z/value', group_path='/station/XY')
        self.catalog.registerIndex(index)
        r = self.catalog.indexResource(res)
        self.assertEquals(len(r), 2)
        el = self.catalog.dumpIndex(index)
        self.assertEquals(len(el), 2)
        self.assertEquals(el[0].key, '3')
        self.assertEquals(el[0].group_pos, 0)
        self.assertEquals(el[0].document.data, res.document.data)
        self.assertEquals(el[1].key, '6')
        self.assertEquals(el[1].group_pos, 1)
        self.assertEquals(el[1].document.data, res.document.data)
        self.catalog.deleteIndex(index)
        self.xmldb.deleteResource(res)

    def test_flushIndex(self):
        index1 = XmlIndex(self.rt1, '/station/station_code', label='code')
        index2 = XmlIndex(self.rt1, '/station/XY/paramXY', label='paramXY')
        self.catalog.registerIndex(index1)
        self.catalog.registerIndex(index2)
        res = Resource(self.rt1, document=newXMLDocument(RAW_XML2))
        self.xmldb.addResource(res)
        self.catalog.indexResource(res)
        el = self.catalog.dumpIndex(index1)
        self.assertEquals(len(el), 1)
        el = self.catalog.dumpIndex(index2)
        self.assertEquals(len(el), 3)
        self.catalog.flushIndex(index1)
        el = self.catalog.dumpIndex(index1)
        self.assertEquals(len(el), 0)
        el = self.catalog.dumpIndex(index2)
        self.assertEquals(len(el), 3)
        self.catalog.flushIndex(index2)
        el = self.catalog.dumpIndex(index2)
        self.assertEquals(len(el), 0)
        self.catalog.deleteIndex(index1)
        self.catalog.deleteIndex(index2)
        self.xmldb.deleteResource(res)

    def test_runXPathQuery(self):
        self._setup_testdata()
        q = '/testpackage/station/station'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/station/*'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/station/* limit 1'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 1)
        self.assertTrue(self.res1.document._id in res)
        q = '/testpackage/station/* limit 1 offset 1'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 1)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/station/* limit 1,1'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 1)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/*/*'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 3)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        self.assertTrue(self.res3.document._id in res)
        q = '/*/*/*'
        res = self.catalog.query(XPathQuery(q))
        assert len(res['ordered']) >= 3
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        self.assertTrue(self.res3.document._id in res)
        q = '/testpackage/station[station/lat]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/station[station/XY/paramXY]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 1)
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[station/lon = 12.51200]'
        xpq = XPathQuery(q)
        res = self.catalog.query(xpq)
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = '/testpackage/station[station/lon != 12.51200 and ' + 'station/lat = 55.23200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[station/lat = 55.23200 and ' + 'station/lon != 12.51200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[station/lon = 12.51200 or ' + 'station/lon = 22.51200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/station[station/lon = 12.51200 or ' + 'station/lon = 0.51200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = '/testpackage/station[station/lon = 12.51200 or ' + 'station/XY/paramXY = 2.5]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        q = '/testpackage/station[station/lon = 12.51200 or ' + 'station/XY/paramXY = -100]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = '/testpackage/station[station/XY/paramXY and ' + 'station/lon = 12.51200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 0)
        q = '/testpackage/station[station/XY/paramXY and ' + 'station/lon = 22.51200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[station/lon = 12.51200 and ' + 'station/XY/paramXY]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 0)
        q = '/testpackage/station[station/lon = 22.51200 and ' + 'station/XY/paramXY]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[station/XY/paramXY or ' + 'station/lon = 12.51200]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        self.assertTrue(self.res1.document._id in res)
        self.assertTrue(self.res2.document._id in res)
        q = '/sortordertests/sotest[sortorder/int1] ' + 'order by sortorder/int1 desc'
        res = self.catalog.query(XPathQuery(q))
        res_ids = [ r.document._id for r in self.so_res ]
        res_ids.reverse()
        self.assertEqual(res['ordered'], res_ids)
        so1 = '/sortordertests/sotest[sortorder/int1] ' + 'order by sortorder/int1 desc ' + 'limit 3'
        so2 = '/sortordertests/sotest[sortorder/int1] ' + 'order by sortorder/int1 desc ' + 'offset 2'
        so3 = '/sortordertests/sotest[sortorder/int1] ' + 'order by sortorder/int2 asc, sortorder/str2 desc ' + 'limit 5,2'
        so4 = '/sortordertests/sotest ' + 'order by sortorder/int2 desc, sortorder/str2 desc ' + 'limit 3'
        so5 = '/sortordertests/sotest[sortorder/int1] ' + 'order by sortorder/int2 asc, sortorder/str2 desc ' + 'limit 5 offset 2'
        res1 = self.catalog.query(XPathQuery(so1))
        res2 = self.catalog.query(XPathQuery(so2))
        res3 = self.catalog.query(XPathQuery(so3))
        res4 = self.catalog.query(XPathQuery(so4))
        res5 = self.catalog.query(XPathQuery(so5))
        self.assertEqual(res1['ordered'], res_ids[:3])
        self.assertEqual(res2['ordered'], res_ids[2:])
        res_ids.reverse()
        self.assertEqual(res3['ordered'], [res_ids[4], res_ids[1], res_ids[2]])
        self.assertEqual(res4['ordered'], [res_ids[1], res_ids[2], res_ids[0]])
        self.assertEqual(res5['ordered'], [res_ids[4], res_ids[1], res_ids[2]])
        q = '/testpackage/station[not(station/XY/paramXY)]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 1)
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = "/testpackage/station[station/XY/paramXY != '2.5']"
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = "/testpackage/station[not(station/XY/paramXY = '2.5')]"
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = "/testpackage/station[not(station/XY/paramXY = '2.5' " + "and station/XY/paramXY = '0' and station/XY/paramXY = '99')]"
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = "/testpackage/station[not(station/XY/paramXY = '2.5')]"
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res1.document._id])
        q = '/testpackage/station[longitude]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(len(res['ordered']), 2)
        q = '/testpackage/station[longitude = 22.51200 and station/XY/paramXY]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[longitude=22.51200 and paramXY=5]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [])
        q = '/testpackage/station[longitude=22.51200 and paramXY=2.5]'
        res = self.catalog.query(XPathQuery(q))
        self.assertEqual(res['ordered'], [self.res2.document._id])
        q = '/testpackage/station[station/XY]'
        self.assertRaises(NotFoundError, self.catalog.query, XPathQuery(q))
        self._cleanup_testdata()

    def test_indexTypes(self):
        text_idx = self.env.catalog.registerIndex('testpackage', 'station', 'idx1', '/station/station_code', 'text')
        float_idx = self.env.catalog.registerIndex('testpackage', 'station', 'idx2', '/station/lon', 'float')
        self.env.catalog.reindexIndex(text_idx)
        self.env.catalog.reindexIndex(float_idx)
        self.env.catalog.deleteAllIndexes('testpackage')

    def test_updateIndexView(self):
        """
        Tests creation of an index view.
        """
        self._setup_testdata()
        self.catalog.updateIndexView(self.idx1)
        sql = 'SELECT * FROM "/testpackage/station"'
        res = self.env.db.engine.execute(sql).fetchall()
        self.assertEquals([ i[0] for i in res ], [8, 9, 9, 9])
        self.catalog.dropIndexView(self.idx1)
        sql = 'SELECT * FROM "/testpackage/station"'
        self.assertRaises(Exception, self.env.db.engine.execute, sql)
        self._cleanup_testdata()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XmlIndexCatalogTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')