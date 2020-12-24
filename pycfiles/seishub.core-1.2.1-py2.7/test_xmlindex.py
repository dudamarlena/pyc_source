# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\xmldb\tests\test_xmlindex.py
# Compiled at: 2010-12-23 17:42:44
from datetime import datetime
from obspy.core import UTCDateTime
from seishub.core.exceptions import SeisHubError
from seishub.core.test import SeisHubEnvironmentTestCase
from seishub.core.xmldb import index
from seishub.core.xmldb.index import NumericIndexElement, XmlIndex
from seishub.core.xmldb.resource import XmlDocument, newXMLDocument
import unittest
RAW_XML1 = '\n<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <paramXY>20.5</paramXY>\n        <paramXY>11.5</paramXY>\n        <paramXY>blah</paramXY>\n    </XY>\n    <creation_date>%s</creation_date>\n    <bool>%s</bool>\n</station>\n'
RAW_XML2 = '\n<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <X>1</X>\n        <Y id = "1">2</Y>\n        <Z>\n            <value>3</value>\n        </Z>\n    </XY>\n    <XY>\n        <X>4</X>\n        <Y id = "2">5</Y>\n        <Z>\n            <value>6</value>\n        </Z>\n    </XY>\n    <creation_date>%s</creation_date>\n    <bool>%s</bool>\n</station>\n'

class XmlIndexTest(SeisHubEnvironmentTestCase):

    def setUp(self):
        self.pkg1 = self.env.registry.db_registerPackage('testpackage')
        self.rt1 = self.env.registry.db_registerResourceType('testpackage', 'station')

    def tearDown(self):
        self.env.registry.db_deleteResourceType('testpackage', 'station')
        self.env.registry.db_deletePackage('testpackage')

    def testIndexCommon(self):
        si = XmlIndex(self.rt1, xpath='/station/station_code')
        mi = XmlIndex(self.rt1, xpath='/station/XY/paramXY')
        ni = XmlIndex(self.rt1, xpath='/station/network')
        test_doc = newXMLDocument(RAW_XML1)

        class Foo(object):
            pass

        self.assertRaises(TypeError, si.eval, Foo())
        self.assertRaises(SeisHubError, si.eval, XmlDocument())
        res = si.eval(test_doc, self.env)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0].index, si)
        self.assertEquals(res[0].document, test_doc)
        self.assertEquals(res[0].key, 'BERN')
        res = mi.eval(test_doc, self.env)
        self.assertEquals(len(res), 3)
        self.assertEquals(res[0].index, mi)
        self.assertEquals(res[0].document, test_doc)
        self.assertEquals(res[0].key, '20.5')
        self.assertEquals(res[1].index, mi)
        self.assertEquals(res[1].document, test_doc)
        self.assertEquals(res[1].key, '11.5')
        self.assertEquals(res[2].index, mi)
        self.assertEquals(res[2].document, test_doc)
        self.assertEquals(res[2].key, 'blah')
        res = ni.eval(test_doc, self.env)
        self.assertEquals(res[0].index, ni)
        self.assertEquals(res[0].document, test_doc)
        self.assertFalse(res[0].key, None)
        return

    def testTextIndex(self):
        test_doc = newXMLDocument(RAW_XML1)
        idx = XmlIndex(self.rt1, '/station/lon', index.TEXT_INDEX)
        res = idx.eval(test_doc, self.env)[0]
        self.assertEquals(type(res), index.TextIndexElement)
        self.assertEquals(type(res.key), unicode)
        self.assertEquals(res.key, '12.51200')

    def testNumericIndex(self):
        test_doc = newXMLDocument(RAW_XML1)
        idx = XmlIndex(self.rt1, '/station/lon', index.NUMERIC_INDEX)
        res = idx.eval(test_doc, self.env)[0]
        self.assertEquals(type(res), NumericIndexElement)
        self.assertEquals(res.key, '12.51200')
        idx = XmlIndex(self.rt1, '/station/XY/paramXY', index.NUMERIC_INDEX)
        res = idx.eval(test_doc, self.env)
        self.assertEquals(len(res), 2)

    def test_DateTimeIndex(self):
        """
        Tests indexing of datetimes.
        """
        dt = datetime(2008, 10, 23, 11, 53, 12, 54000)
        dt2 = datetime(2008, 10, 23, 11, 53, 12)
        dt3 = datetime(2008, 10, 23)
        dt4 = datetime(2008, 10, 23, 11)
        dt5 = datetime(2008, 10, 23, 11, 53)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt.strftime('%Y%m%dT%H:%M:%S') + '.054000'
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt.strftime('%Y-%m-%dT%H:%M:%S') + '.054000'
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt.strftime('%Y%m%dT%H:%M:%S') + '.054000Z'
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt.strftime('%Y%m%d %H:%M:%S') + '.054000'
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt2.strftime('%Y%m%dT%H:%M:%S')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt2)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt3.strftime('%Y-%m-%d')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt3)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt4.strftime('%Y-%m-%dT%H')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt4)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX)
        timestr = dt5.strftime('%Y-%m-%dT%H:%M')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt5)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATETIME_INDEX, '%H:%M:%S - %Y%m%d')
        timestr = dt.strftime('%H:%M:%S - %Y%m%d')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt.replace(microsecond=0))

    def test_TimestampIndex(self):
        """
        Tests indexing of timestamps.
        """
        dt = UTCDateTime(2008, 10, 23, 11, 53, 12, 54000)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.TIMESTAMP_INDEX)
        timestr = '%f' % dt.timestamp
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)
        dt = UTCDateTime(2008, 10, 23, 11, 53, 12)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.TIMESTAMP_INDEX)
        timestr = '%f' % dt.timestamp
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)
        dt = UTCDateTime(1969, 12, 31, 23, 36, 39, 500000)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.TIMESTAMP_INDEX)
        timestr = '%f' % dt.timestamp
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt)

    def test_DateIndex(self):
        """
        Tests indexing of dates.
        """
        dt = datetime(2008, 10, 10, 11, 53, 0, 54000)
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATE_INDEX)
        timestr = dt.strftime('%Y%m%d')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt.date())
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATE_INDEX)
        timestr = dt.strftime('%Y-%m-%d')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt.date())
        idx = XmlIndex(self.rt1, '/station/creation_date', index.DATE_INDEX, options='%d.%m.%Y')
        timestr = dt.strftime('%d.%m.%Y')
        doc = newXMLDocument(RAW_XML1 % (timestr, ''))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, dt.date())

    def testBooleanIndex(self):
        idx = XmlIndex(self.rt1, '/station/bool', index.BOOLEAN_INDEX)
        doc = newXMLDocument(RAW_XML1 % ('', 'True'))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, True)
        doc = newXMLDocument(RAW_XML1 % ('', 'False'))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, False)
        doc = newXMLDocument(RAW_XML1 % ('', '1'))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, True)
        doc = newXMLDocument(RAW_XML1 % ('', '0'))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, False)
        doc = newXMLDocument(RAW_XML1 % ('', 'something'))
        res = idx.eval(doc, self.env)[0]
        self.assertEqual(res.key, True)

    def testIndexGrouping(self):
        doc = newXMLDocument(RAW_XML2)
        idx1 = XmlIndex(self.rt1, '/station/XY/X', index.NUMERIC_INDEX, group_path='/station/XY')
        res = idx1.eval(doc, self.env)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].key, '1')
        self.assertEqual(res[0].group_pos, 0)
        self.assertEqual(res[1].key, '4')
        self.assertEqual(res[1].group_pos, 1)
        idx2 = XmlIndex(self.rt1, '/station/XY/Y', index.NUMERIC_INDEX, group_path='/station/XY')
        res = idx2.eval(doc, self.env)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].key, '2')
        self.assertEqual(res[0].group_pos, 0)
        self.assertEqual(res[1].key, '5')
        self.assertEqual(res[1].group_pos, 1)
        idx3 = XmlIndex(self.rt1, '/station/XY/Y/@id', index.NUMERIC_INDEX, group_path='/station/XY')
        res = idx3.eval(doc, self.env)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].key, '1')
        self.assertEqual(res[0].group_pos, 0)
        self.assertEqual(res[1].key, '2')
        self.assertEqual(res[1].group_pos, 1)
        idx4 = XmlIndex(self.rt1, '/station/XY/Z/value', index.NUMERIC_INDEX, group_path='/station/XY')
        res = idx4.eval(doc, self.env)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].key, '3')
        self.assertEqual(res[0].group_pos, 0)
        self.assertEqual(res[1].key, '6')
        self.assertEqual(res[1].group_pos, 1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XmlIndexTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')