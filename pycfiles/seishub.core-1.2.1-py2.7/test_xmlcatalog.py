# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\xmldb\tests\test_xmlcatalog.py
# Compiled at: 2010-12-23 17:42:44
"""
This test suite consists of various tests related to the catalog interface.
"""
from seishub.core.exceptions import SeisHubError
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import unittest
RAW_XML = '<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <paramXY>20.5</paramXY>\n        <paramXY>11.5</paramXY>\n        <paramXY>blah</paramXY>\n    </XY>\n    <missing>No</missing>\n</station>'
RAW_XML1 = '<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <paramXY>20.5</paramXY>\n        <paramXY>11.5</paramXY>\n        <paramXY>blah</paramXY>\n    </XY>\n</station>'
RAW_XML2 = '<station rel_uri="genf">\n    <station_code>GENF</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>22.51200</lon>\n    <lat>55.23200</lat>\n    <stat_elav>0.73500</stat_elav>\n    <XY>\n        <paramXY>2.5</paramXY>\n        <paramXY>0</paramXY>\n        <paramXY>99</paramXY>\n    </XY>\n    <XY>\n        <paramXY>2110.5</paramXY>\n        <paramXY>111.5</paramXY>\n        <paramXY>cblah</paramXY>\n    </XY>\n</station>'
RAW_XML3 = '<?xml version="1.0"?>\n<testml>\n<blah1 id="3"><blahblah1>blahblahblah</blahblah1></blah1>\n</testml>\n'
RAW_XML4 = '<?xml version="1.0"?>\n<testml>\n<blah1 id="4"><blahblah1>moep</blahblah1></blah1>\n</testml>\n'
PID1 = 'testpackage'
RID1 = 'station'
RID2 = 'testml'
PID2 = 'degenesis'
RID3 = 'weapon'
IDX1 = '/station/XY/paramXY'
IDX2 = '/testml/blah1/@id'
IDX3 = '/weapon/damage'
IDX4 = '/station'
IDX5 = '/testml'

class XmlCatalogTest(SeisHubEnvironmentTestCase):

    def setUp(self):
        self.env.registry.db_registerPackage(PID1)
        self.env.registry.db_registerPackage(PID2)
        self.env.registry.db_registerResourceType(PID1, RID1)
        self.env.registry.db_registerResourceType(PID1, RID2)
        self.env.registry.db_registerResourceType(PID2, RID3)
        self.idx1 = self.env.catalog.registerIndex(PID1, RID1, '1', IDX1)
        self.idx2 = self.env.catalog.registerIndex(PID1, RID2, '2', IDX2)
        self.idx3 = self.env.catalog.registerIndex(PID2, RID3, '3', IDX3)
        self.res1 = self.env.catalog.addResource(PID1, RID1, RAW_XML1)
        self.res2 = self.env.catalog.addResource(PID1, RID1, RAW_XML2)
        self.res3 = self.env.catalog.addResource(PID1, RID2, RAW_XML3)

    def tearDown(self):
        try:
            self.env.catalog.deleteResource(self.res1)
        except:
            pass

        try:
            self.env.catalog.deleteResource(self.res2)
        except:
            pass

        try:
            self.env.catalog.deleteResource(self.res3)
        except:
            pass

        self.env.catalog.deleteIndex(self.idx1)
        self.env.catalog.deleteIndex(self.idx2)
        self.env.catalog.deleteIndex(self.idx3)
        self.env.registry.db_deleteResourceType(PID1, RID1)
        self.env.registry.db_deleteResourceType(PID1, RID2)
        self.env.registry.db_deleteResourceType(PID2, RID3)
        self.env.registry.db_deletePackage(PID1)
        self.env.registry.db_deletePackage(PID2)

    def test_renameResource(self):
        """
        Tests for renaming resources.
        """
        catalog = self.env.catalog
        res1 = catalog.addResource(PID1, RID1, RAW_XML, name='test.xml')
        res2 = catalog.addResource(PID1, RID1, RAW_XML, name='test2.xml')
        catalog.renameResource(res1, 'test3.xml')
        res = catalog.getResource(PID1, RID1, 'test3.xml')
        self.assertEquals(res.name, 'test3.xml')
        try:
            catalog.renameResource(res2, 'üöä.üöä')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.BAD_REQUEST)

        catalog.deleteResource(res1)
        catalog.deleteResource(res2)

    def test_renameToExistingResource(self):
        """
        Tests for renaming resources to already existing names.
        """
        catalog = self.env.catalog
        res1 = catalog.addResource(PID1, RID1, RAW_XML, name='test.xml')
        res2 = catalog.addResource(PID1, RID1, RAW_XML, name='test2.xml')
        try:
            catalog.renameResource(res1, 'test2.xml')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        try:
            catalog.renameResource(res2, 'test.xml')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        catalog.renameResource(res1, 'test.xml')
        catalog.deleteResource(res1)
        catalog.deleteResource(res2)

    def test_IResourceManager(self):
        catalog = self.env.catalog
        res = catalog.addResource(PID1, RID1, RAW_XML, uid='testuser', name='testfilename.xml')
        r = catalog.getResource(PID1, RID1, res.name)
        self.assertEquals(RAW_XML, r.document.data)
        self.assertEquals('testuser', r.document.meta.uid)
        self.assertEquals('testfilename.xml', r.name)
        catalog.renameResource(res, 'changed.xml')
        r = catalog.getResource(PID1, RID1, 'changed.xml')
        self.assertEquals('changed.xml', r.name)
        catalog.deleteResource(r)
        r = catalog.getAllResources(PID1, RID1)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0].package.package_id, PID1)
        self.assertEqual(r[0].resourcetype.resourcetype_id, RID1)
        self.assertEqual(r[0].document.data, self.res1.document.data)
        self.assertEqual(r[1].package.package_id, PID1)
        self.assertEqual(r[1].resourcetype.resourcetype_id, RID1)
        self.assertEqual(r[1].document.data, self.res2.document.data)
        r = catalog.getAllResources(PID1)
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0].package.package_id, PID1)
        self.assertEqual(r[0].resourcetype.resourcetype_id, RID1)
        self.assertEqual(r[0].document.data, self.res1.document.data)
        self.assertEqual(r[1].package.package_id, PID1)
        self.assertEqual(r[1].resourcetype.resourcetype_id, RID1)
        self.assertEqual(r[1].document.data, self.res2.document.data)
        self.assertEqual(r[2].package.package_id, PID1)
        self.assertEqual(r[2].resourcetype.resourcetype_id, RID2)
        self.assertEqual(r[2].document.data, self.res3.document.data)
        r = catalog.getAllResources()
        assert len(r) >= 3
        r = catalog.getAllResources('unexisting package')
        self.assertEquals(len(r), 0)
        r = catalog.getAllResources(PID2)
        self.assertEqual(len(r), 0)
        r = catalog.getAllResources('testpackage', 'station')
        assert len(r) == 2
        catalog.deleteAllResources('testpackage', 'station')
        r = catalog.getAllResources('testpackage', 'station')
        assert len(r) == 0

    def test_reindexIndex(self):
        self.env.catalog.reindexIndex(self.idx1)
        self.env.catalog.reindexIndex(self.idx2)
        self.env.catalog.reindexIndex(self.idx3)

    def test_getIndexes(self):
        l = self.env.catalog.getIndexes(package_id='testpackage')
        self.assertEqual(len(l), 2)
        self.assertEqual(str(l[0]), '/testpackage/station' + IDX1)
        self.assertEqual(str(l[1]), '/testpackage/testml' + IDX2)
        l = self.env.catalog.getIndexes(package_id='degenesis')
        self.assertEqual(len(l), 1)
        self.assertEqual(str(l[0]), '/degenesis/weapon' + IDX3)
        l = self.env.catalog.getIndexes(package_id='testpackage')
        self.assertEqual(len(l), 2)
        self.assertEqual(str(l[0]), '/testpackage/station' + IDX1)
        self.assertEqual(str(l[1]), '/testpackage/testml' + IDX2)
        l = self.env.catalog.getIndexes(package_id='degenesis')
        self.assertEqual(len(l), 1)
        self.assertEqual(str(l[0]), '/degenesis/weapon' + IDX3)
        l = self.env.catalog.getIndexes(resourcetype_id='station')
        self.assertEqual(len(l), 1)
        self.assertEqual(str(l[0]), '/testpackage/station' + IDX1)
        l = self.env.catalog.getIndexes(resourcetype_id='testml')
        self.assertEqual(len(l), 1)
        self.assertEqual(str(l[0]), '/testpackage/testml' + IDX2)
        l = self.env.catalog.getIndexes(package_id='testpackage', resourcetype_id='station')
        self.assertEqual(len(l), 1)
        self.assertEqual(str(l[0]), '/testpackage/station' + IDX1)
        l = self.env.catalog.getIndexes(package_id='testpackage', resourcetype_id='weapon')
        self.assertEqual(len(l), 0)

    def test_query(self):
        """
        """
        self.env.catalog.reindexIndex(self.idx1)
        idx4 = self.env.catalog.registerIndex(PID1, RID1, '4', IDX4, 'boolean')
        self.env.catalog.reindexIndex(idx4)
        idx5 = self.env.catalog.registerIndex(PID1, RID2, '5', IDX5, 'boolean')
        self.env.catalog.reindexIndex(idx5)
        res1 = self.env.catalog.query('/testpackage/station/station ' + 'order by XY/paramXY asc limit 2', full=True)
        self.assertEqual(len(res1), 2)
        self.assertEqual(res1[0]._id, self.res2._id)
        self.assertEqual(res1[0].document._id, self.res2.document._id)
        self.assertEqual(res1[1]._id, self.res1._id)
        self.assertEqual(res1[1].document._id, self.res1.document._id)
        res1 = self.env.catalog.query('/testpackage/station/station limit 1')
        self.assertEqual(len(res1['ordered']), 1)
        self.assertEqual(res1['ordered'][0], self.res1.document._id)
        res1 = self.env.catalog.query('/testpackage/station/station ' + 'order by XY/paramXY asc')
        self.assertEqual(len(res1['ordered']), 2)
        self.assertEqual(res1['ordered'][0], self.res2.document._id)
        self.assertEqual(res1['ordered'][1], self.res1.document._id)
        res1 = self.env.catalog.query('/testpackage/station/station ' + 'order by XY/paramXY asc limit 2')
        self.assertEqual(len(res1['ordered']), 2)
        self.assertEqual(res1['ordered'][0], self.res2.document._id)
        self.assertEqual(res1['ordered'][1], self.res1.document._id)
        res3 = self.env.catalog.query('/testpackage/*/*', full=True)
        self.assertEqual(len(res3), 3)
        self.assertEqual(res3[0]._id, self.res1._id)
        self.assertEqual(res3[0].document._id, self.res1.document._id)
        self.assertEqual(res3[1]._id, self.res2._id)
        self.assertEqual(res3[1].document._id, self.res2.document._id)
        self.assertEqual(res3[2]._id, self.res3._id)
        self.assertEqual(res3[2].document._id, self.res3.document._id)
        res4 = self.env.catalog.query('/testpackage/*/station', full=True)
        self.assertEqual(res4[0].document._id, self.res1.document._id)
        self.assertEqual(res4[1].document._id, self.res2.document._id)
        res5 = self.env.catalog.query('/testpackage/testml/testml', full=True)
        self.assertEqual(len(res5), 1)
        self.assertEqual(res5[0]._id, self.res3._id)
        self.assertEqual(res5[0].document._id, self.res3.document._id)
        self.env.catalog.deleteIndex(idx4)
        self.env.catalog.deleteIndex(idx5)

    def test_indexRevision(self):
        """
        Tests indexing of a version controlled resource.
        
        Indexing of revisions is only rudimentary supported. Right now only
        the latest revision is indexed - old revisions are not represented in
        the index catalog.
        """
        self.env.registry.db_registerPackage('test-catalog')
        self.env.registry.db_registerResourceType('test-catalog', 'index', version_control=True)
        idx = self.env.catalog.registerIndex('test-catalog', 'index', 'lat', '/station/lat')
        res1 = self.env.catalog.addResource('test-catalog', 'index', RAW_XML, name='muh.xml')
        self.env.catalog.modifyResource(res1, RAW_XML)
        self.env.catalog.modifyResource(res1, RAW_XML)
        res = self.env.catalog.getResource('test-catalog', 'index', 'muh.xml')
        index_dict = self.env.catalog.getIndexData(res)
        self.assertEqual(index_dict, {'lat': {0: ['50.23200']}})
        res = self.env.catalog.getResource('test-catalog', 'index', 'muh.xml', 3)
        index_dict = self.env.catalog.getIndexData(res)
        self.assertEqual(index_dict, {'lat': {0: ['50.23200']}})
        res = self.env.catalog.getResource('test-catalog', 'index', 'muh.xml', 2)
        index_dict = self.env.catalog.getIndexData(res)
        self.assertEqual(index_dict, {'lat': {0: ['50.23200']}})
        self.env.catalog.reindexIndex(idx)
        self.env.catalog.deleteAllResources('test-catalog')
        self.env.catalog.deleteAllIndexes('test-catalog')
        self.env.registry.db_deleteResourceType('test-catalog', 'index')
        self.env.registry.db_deletePackage('test-catalog')

    def test_registerInvalidIndex(self):
        """
        SeisHub should not allow adding of an index with invalid parameters.
        """
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, 'XXX', 'rt', '1', '/station/lat')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, package_id='XXX', resourcetype_id='rt', xpath='/station/lat', label='1')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, 'package', 'XXX', '1', '/station/lat')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, package_id='package', resourcetype_id='XXX', xpath='/station/lat', label='1')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, 'package', 'rt', '1', '/station/lat', 'XXX')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, package_id='package', resourcetype_id='rt', xpath='/station/lat', type='XXX', label='1')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, 'package', 'rt', '1', '')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, package_id='package', resourcetype_id='rt', xpath='', label='1')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, 'package', 'rt', '', '/')
        self.assertRaises(SeisHubError, self.env.catalog.registerIndex, package_id='package', resourcetype_id='rt', xpath='/', label='')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')

    def test_registerIndexTwice(self):
        """
        Test for registering an index a second time.
        """
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        self.env.catalog.registerIndex('package', 'rt', 'xy', '/station/XY')
        self.env.catalog.registerIndex('package', 'rt', 'lon', '/station#lon')
        try:
            self.env.catalog.registerIndex('package', 'rt', 'xy', '/station/XY')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        try:
            self.env.catalog.registerIndex('package', 'rt', 'lon', '/station#lon')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        try:
            self.env.catalog.registerIndex('package', 'rt', 'otherlabel', '/station#lon')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        try:
            self.env.catalog.registerIndex('package', 'rt', 'otherlabel', '/station/lon')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        try:
            self.env.catalog.registerIndex('package', 'rt', 'xy', '/station/lat')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.FORBIDDEN)

        self.env.catalog.deleteAllIndexes('package', 'rt')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')

    def test_registerIndexWithInvalidLabel(self):
        """
        Test of registering indexes with invalid labels.
        """
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        self.env.catalog.registerIndex('package', 'rt', 'B' * 30, '/station/XY')
        try:
            self.env.catalog.registerIndex('package', 'rt', 'A' * 31, '/station/XY')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.BAD_REQUEST)

        try:
            self.env.catalog.registerIndex('package', 'rt', 'x/y/4', '/station#lon')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.BAD_REQUEST)

        self.env.catalog.registerIndex('package', 'rt', 'A\\B', '/station/lat')
        self.env.catalog.deleteAllIndexes('package')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')

    def test_generateViews(self):
        """
        Tests automatic view generation.
        """
        self.env.catalog.reindexIndex(self.idx1)
        idx4 = self.env.catalog.registerIndex(PID1, RID1, '4', IDX4, 'boolean')
        self.env.catalog.reindexIndex(idx4)
        idx5 = self.env.catalog.registerIndex(PID1, RID2, '5', IDX5, 'boolean')
        self.env.catalog.reindexIndex(idx5)
        sql = 'SELECT * FROM "/testpackage/station"'
        result = self.env.db.engine.execute(sql).fetchall()
        self.assertEquals(len(result), 9)
        sql = 'SELECT * FROM "/testpackage/testml"'
        result = self.env.db.engine.execute(sql).fetchall()
        self.assertEqual(len(result), 1)
        res = self.env.catalog.addResource(PID1, RID2, RAW_XML4)
        idx6 = self.env.catalog.registerIndex(PID1, RID2, 'muh', '/testml/blah1/blahblah1')
        sql = 'SELECT * FROM "/testpackage/testml"'
        result = self.env.db.engine.execute(sql).fetchall()
        self.assertEqual(len(result), 2)
        self.env.catalog.deleteIndex(idx4)
        self.env.catalog.deleteIndex(idx5)
        self.env.catalog.deleteIndex(idx6)
        self.env.catalog.deleteResource(res)

    def test_queryCatalogWithOperators(self):
        """
        Tests a lot of operators with catalog queries.
        """
        catalog = self.env.catalog
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        catalog.registerIndex('package', 'rt', 'lat', '/station/lat', type='numeric')
        catalog.registerIndex('package', 'rt', 'lon', '/station/lon', type='numeric')
        catalog.registerIndex('package', 'rt', 'paramXY', '/station/XY/paramXY')
        catalog.registerIndex('package', 'rt', 'missing', '/station/missing')
        catalog.addResource('package', 'rt', RAW_XML, name='1')
        catalog.addResource('package', 'rt', RAW_XML1, name='2')
        catalog.addResource('package', 'rt', RAW_XML2, name='3')
        query = '/package/rt/*'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/*/*'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/*/station'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt/station'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt/station[lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/*[lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[station/lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[*/lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[lat>51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/*[lat>51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[station/lat>51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[*/lat>51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[lat>49 and lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[lat<51 and lat>49]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[(lat<51 and lat>49)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/*[lat>49 and lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/*[lat<51 and lat>49]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/*[(lat<51 and lat>49)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[station/lat>49 and station/lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[station/lat<51 and station/lat>49]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[(station/lat<51 and station/lat>49)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[*/lat>49 and */lat<51]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[*/lat<51 and */lat>49]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[(station/lat<51 and */lat>49)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[lat>49 and lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[station/lat>49 and station/lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[(lat>49 and lat<56) and lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[(*/lat>49 and */lat<56) and station/lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[lat>49 and (lat<56 and lon=22.51200)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[*/lat>49 and (*/lat<56 and */lon=22.51200)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[lat>49 and (lat<56 and lon=22.51200)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[*/lat>49 and (*/lat<56 and */lon=22.51200)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[lat>49 and lat<56 and lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[*/lat>49 and */lat<56 and */lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[(lat>52 and lat<56) or lon=12.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[(*/lat>52 and */lat<56) or */lon=12.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt/station[lat>49 or lat<56 or lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[*/lat>49 or */lat<56 or station/lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt/station[lat>49 or lat<56 or lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[*/lat>49 or station/lat<56 or */lon=22.51200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt/station[missing]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[station/missing]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[*/missing]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[lat > 49 and lat < 56 and missing]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[*/lat > 49 and */lat < 56 and */missing]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[lat > 49 and missing and lat < 56]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[station/lat > 49 and */missing and */lat < 56]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        catalog.deleteAllResources('package')
        catalog.deleteAllIndexes('package')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')

    def test_queryCatalogWithEqualOperator(self):
        """
        Tests the equal operators (== and !=) at the catalog query interface.
        """
        catalog = self.env.catalog
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        catalog.registerIndex('package', 'rt', 'latitude', '/station/lat', type='numeric')
        catalog.registerIndex('package', 'rt', 'longitude', '/station/lon', type='numeric')
        catalog.addResource('package', 'rt', RAW_XML, name='1')
        catalog.addResource('package', 'rt', RAW_XML1, name='2')
        catalog.addResource('package', 'rt', RAW_XML2, name='3')
        query = '/package/rt/station[lat!=55.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[station/lat!=55.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[latitude!=55.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[lat=50.232001]'
        result = catalog.query(query, full=True)
        self.assertFalse(result)
        query = '/package/rt[station/lat=50.232001]'
        result = catalog.query(query, full=True)
        self.assertFalse(result)
        query = '/package/rt[latitude=50.232001]'
        result = catalog.query(query, full=True)
        self.assertFalse(result)
        query = '/package/rt/station[lat==50.232001]'
        result = catalog.query(query, full=True)
        self.assertFalse(result)
        query = '/package/rt[station/lat==50.232001]'
        result = catalog.query(query, full=True)
        self.assertFalse(result)
        query = '/package/rt[latitude==50.232001]'
        result = catalog.query(query, full=True)
        self.assertFalse(result)
        query = '/package/rt/station[lat=50.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[station/lat=50.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[latitude=50.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[lat==50.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[station/lat==50.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[latitude==50.23200]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        catalog.deleteAllResources('package')
        catalog.deleteAllIndexes('package')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')

    def test_queryCatalogWithNotFunction(self):
        """
        Tests the not() function at the catalog query interface.
        """
        catalog = self.env.catalog
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        catalog.registerIndex('package', 'rt', 'latitude', '/station/lat', type='numeric')
        catalog.registerIndex('package', 'rt', 'longitude', '/station/lon', type='numeric')
        catalog.registerIndex('package', 'rt', 'xy', '/station/XY/paramXY')
        catalog.registerIndex('package', 'rt', 'miss', '/station/missing')
        catalog.addResource('package', 'rt', RAW_XML, name='1')
        catalog.addResource('package', 'rt', RAW_XML1, name='2')
        catalog.addResource('package', 'rt', RAW_XML2, name='3')
        query = '/package/rt/station[not(missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/*[not(missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[not(station/missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[not(*/missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[lat > 0 and lat < 156 and not(missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[*/lat > 0 and */lat < 156 and not(*/missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[XY/paramXY != 2.5]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[station/XY/paramXY != 2.5]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[*/XY/paramXY != 2.5]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[*/*/paramXY != 2.5]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[*/*/paramXY == 2.5]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[not(XY/paramXY = 2.5)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[not(station/XY/paramXY = 2.5)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt[not(station/*/paramXY = 2.5)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '/package/rt/station[not(XY/paramXY = 2.5) and not(missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[not(station/XY/paramXY = 2.5) and not(*/missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[not(XY/paramXY = 2.5 or missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt[not(station/XY/paramXY = 2.5 or station/missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 1)
        query = '/package/rt/station[not(XY/paramXY = 2.5 and missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        query = '/package/rt[not(station/XY/paramXY = 2.5 and */missing)]'
        result = catalog.query(query, full=True)
        self.assertEqual(len(result), 3)
        catalog.deleteAllResources('package')
        catalog.deleteAllIndexes('package')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')

    def test_queryCatalogWithMacros(self):
        """
        Test macros usage with catalog queries.
        """
        self.env.registry.db_registerPackage('package')
        self.env.registry.db_registerResourceType('package', 'rt')
        self.env.catalog.registerIndex('package', 'rt', 'xy', '/station/XY/paramXY')
        self.env.catalog.addResource('package', 'rt', RAW_XML, name='1')
        self.env.catalog.addResource('package', 'rt', RAW_XML1, name='2')
        self.env.catalog.addResource('package', 'rt', RAW_XML2, name='3')
        query = '{a=XY/paramXY}/package/rt/station[{a}>10 and {a}=20.5]'
        result = self.env.catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '{a=XY/paramXY} /package/rt/station[{a}>10 and {a}=20.5]'
        result = self.env.catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = ' { b = XY/paramXY } /package/rt/station[{b}>10 and {b}=20.5]'
        result = self.env.catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '{a=XY/paramXY, b=XY/paramXY}\n                   /package/rt/station[{a}>10 and {b}=20.5]'
        result = self.env.catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '{a=XY/paramXY, b=XY/paramXY, c=XY/muh/kuh}\n                   /package/rt/station[{a}>10 and {b}=20.5]'
        result = self.env.catalog.query(query, full=True)
        self.assertEqual(len(result), 2)
        query = '{a=XY/paramXY}/package/rt/station[{b}>10 and {b}=20.5]'
        try:
            self.env.catalog.query(query, full=True)
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEquals(e.code, http.BAD_REQUEST)

        self.env.catalog.deleteAllResources('package')
        self.env.catalog.deleteAllIndexes('package')
        self.env.registry.db_deleteResourceType('package', 'rt')
        self.env.registry.db_deletePackage('package')


def suite():
    return unittest.makeSuite(XmlCatalogTest, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')