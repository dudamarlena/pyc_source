# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\registry\tests\test_registry.py
# Compiled at: 2010-12-23 17:42:44
from seishub.core.exceptions import SeisHubError, InvalidObjectError
from seishub.core.test import SeisHubEnvironmentTestCase
from seishub.core.xmldb.resource import Resource, newXMLDocument
import unittest
TEST_SCHEMA = '<xs:schema elementFormDefault="qualified"\n    xmlns:xs="http://www.w3.org/2001/XMLSchema">\n\n    <xs:element name="armor">\n        <xs:complexType>\n            <xs:attribute name="lang" type="xs:string"/>\n            <xs:sequence>\n                <xs:element name="name" type="xs:string" use="required" />\n                <xs:element name="properties" type="xs:string" />\n                <xs:element name="headAC" type="xs:string" />\n                <xs:element name="torsoAC" type="xs:string" />\n                <xs:element name="legsAC" type="xs:string" />\n                <xs:element name="load" type="xs:string" />\n            </xs:sequence>\n        </xs:complexType>\n    </xs:element>\n\n</xs:schema>'
TEST_STYLESHEET = '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" \n    xmlns:xlink="http://www.w3.org/1999/xlink" exclude-result-prefixes="xlink"\n    version="1.0">\n    \n    <xsl:output method="text" encoding="utf-8"\n        media-type="application/json" />\n    \n    <xsl:template match="/seishub">\n        <xsl:text>{</xsl:text>\n\n            <xsl:if test="//package">\n                <xsl:text>"package":[</xsl:text>\n                <xsl:for-each select="//package">\n\n                    <xsl:text>"</xsl:text>\n                    <xsl:value-of select="@xlink:href" />\n                    <xsl:text>"</xsl:text>\n                    <xsl:if test="not (position()=last())">\n                        <xsl:text>,</xsl:text>\n                    </xsl:if>\n                </xsl:for-each>\n\n                <xsl:text>],</xsl:text>\n            </xsl:if>\n\n            <xsl:if test="//resourcetype">\n                <xsl:text>"resourcetype":[</xsl:text>\n                <xsl:for-each select="//resourcetype">\n                    <xsl:text>"</xsl:text>\n                    <xsl:value-of select="@xlink:href" />\n\n                    <xsl:text>"</xsl:text>\n                    <xsl:if test="not (position()=last())">\n                        <xsl:text>,</xsl:text>\n                    </xsl:if>\n                </xsl:for-each>\n                <xsl:text>],</xsl:text>\n            </xsl:if>\n\n            <xsl:if test="//mapping">\n                <xsl:text>"mapping":[</xsl:text>\n                <xsl:for-each select="//mapping">\n                    <xsl:text>"</xsl:text>\n                    <xsl:value-of select="@xlink:href" />\n                    <xsl:text>"</xsl:text>\n                    <xsl:if test="not (position()=last())">\n\n                        <xsl:text>,</xsl:text>\n                    </xsl:if>\n                </xsl:for-each>\n                <xsl:text>],</xsl:text>\n            </xsl:if>\n\n            <xsl:if test="//alias">\n                <xsl:text>"alias":[</xsl:text>\n\n                <xsl:for-each select="//alias">\n                    <xsl:text>"</xsl:text>\n                    <xsl:value-of select="@xlink:href" />\n                    <xsl:text>"</xsl:text>\n                    <xsl:if test="not (position()=last())">\n                        <xsl:text>,</xsl:text>\n                    </xsl:if>\n\n                </xsl:for-each>\n                <xsl:text>],</xsl:text>\n            </xsl:if>\n\n            <xsl:if test="//index">\n                <xsl:text>"index":[</xsl:text>\n                <xsl:for-each select="//index">\n                    <xsl:text>"</xsl:text>\n\n                    <xsl:value-of select="@xlink:href" />\n                    <xsl:text>"</xsl:text>\n                    <xsl:if test="not (position()=last())">\n                        <xsl:text>,</xsl:text>\n                    </xsl:if>\n                </xsl:for-each>\n                <xsl:text>],</xsl:text>\n\n            </xsl:if>\n\n            <xsl:if test="//resource">\n                <xsl:text>"resource":[</xsl:text>\n                <xsl:for-each select="//resource">\n                    <xsl:text>"</xsl:text>\n                    <xsl:value-of select="@xlink:href" />\n                    <xsl:text>"</xsl:text>\n\n                    <xsl:if test="not (position()=last())">\n                        <xsl:text>,</xsl:text>\n                    </xsl:if>\n                </xsl:for-each>\n                <xsl:text>],</xsl:text>\n            </xsl:if>\n\n        <xsl:text>}</xsl:text>\n\n    </xsl:template>\n\n</xsl:stylesheet>'
TEST_RESLIST = '<seishub xml:base="http://localhost:8080" xmlns:xlink="http://www.w3.org/1999/xlink">\n    <mapping xlink:type="simple" xlink:href="/seishub/schema/browser">browser</mapping>\n    <resource xlink:type="simple" xlink:href="/seishub/schema/3">/seishub/schema/3</resource>\n    <resource xlink:type="simple" xlink:href="/seishub/schema/4">/seishub/schema/4</resource>\n</seishub>'
RAW_XML = '<station rel_uri="bern">\n    <station_code>BERN</station_code>\n    <chan_code>1</chan_code>\n    <stat_type>0</stat_type>\n    <lon>12.51200</lon>\n    <lat>50.23200</lat>\n    <stat_elav>0.63500</stat_elav>\n    <XY>\n        <paramXY>20.5</paramXY>\n        <paramXY>11.5</paramXY>\n        <paramXY>blah</paramXY>\n    </XY>\n</station>'

class PackageRegistryTest(SeisHubEnvironmentTestCase):

    def setUp(self):
        self.env.registry.db_registerPackage('testpackage0', '1.0')
        self.env.registry.db_registerResourceType('testpackage0', 'weapon', '1.0')
        self.env.registry.db_registerResourceType('testpackage0', 'armor', '1.0')

    def tearDown(self):
        self.env.registry.db_deleteResourceType('testpackage0', 'weapon')
        self.env.registry.db_deleteResourceType('testpackage0', 'armor')
        self.env.registry.db_deletePackage('testpackage0')

    def test_split_uri(self):
        reg = self.env.registry.stylesheets
        self.assertEqual(reg._split_uri('/package/resourcetype/type'), ('package',
                                                                        'resourcetype',
                                                                        'type'))
        self.assertEqual(reg._split_uri('/package/type'), ('package', None, 'type'))
        reg = self.env.registry.schemas
        self.assertEqual(reg._split_uri('/package/resourcetype/type'), ('package',
                                                                        'resourcetype',
                                                                        'type'))
        self.assertEqual(reg._split_uri('/package/resourcetype'), ('package', 'resourcetype',
                                                                   None))
        return

    def test_InMemoryRegistry(self):
        packages = self.env.registry.getPackageIds()
        for p in packages:
            assert self.env.registry.getPackage(p).package_id == p
            resourcetypes = self.env.registry.getResourceTypeIds(p)
            for rt in resourcetypes:
                rt_object = self.env.registry.getResourceType(p, rt)
                assert rt_object.resourcetype_id == rt

    def test_DatabaseRegistry(self):
        self.env.registry.db_registerPackage('db_registered_package', '1.0')
        package = self.env.registry.db_getPackages('db_registered_package')[0]
        self.assertEqual(package.package_id, 'db_registered_package')
        self.assertEqual(package.version, '1.0')
        self.env.registry.db_deletePackage('db_registered_package')
        package = self.env.registry.db_getPackages('db_registered_package')
        assert package == list()
        self.env.registry.db_registerPackage('db_registered_package', '1.0')
        self.env.registry.db_registerResourceType('db_registered_package', 'db_regsitered_resourcetype', '1.0', True)
        restype = self.env.registry.db_getResourceTypes('db_registered_package', 'db_regsitered_resourcetype')[0]
        self.assertEqual(restype.package.package_id, 'db_registered_package')
        self.assertEqual(restype.resourcetype_id, 'db_regsitered_resourcetype')
        self.assertEqual(restype.version, '1.0')
        self.assertEqual(restype.version_control, True)
        self.assertRaises(SeisHubError, self.env.registry.db_deletePackage, 'db_registered_package')
        self.env.registry.db_deleteResourceType('db_registered_package', 'db_regsitered_resourcetype')
        restype = self.env.registry.db_getResourceTypes('db_registered_package', 'db_regsitered_resourcetype')
        assert restype == list()
        self.env.registry.db_deletePackage('db_registered_package')

    def test_SchemaRegistry(self):
        self.env.registry.schemas.register('testpackage0', 'weapon', 'xsd', TEST_SCHEMA)
        self.env.registry.schemas.register('testpackage0', 'armor', 'xsd', TEST_SCHEMA)
        schema = self.env.registry.schemas.get(package_id='testpackage0', resourcetype_id='weapon')
        self.assertEqual(schema[0].package.package_id, 'testpackage0')
        self.assertEqual(schema[0].resourcetype.resourcetype_id, 'weapon')
        self.assertEqual(schema[0].type, 'xsd')
        res = schema[0].resource
        self.assertEqual(res.document.data, TEST_SCHEMA)
        self.assertEqual(res.package.package_id, 'seishub')
        self.assertEqual(res.resourcetype.resourcetype_id, 'schema')
        schema = self.env.registry.schemas.get(uri='/testpackage0/weapon/xsd')
        self.assertEqual(schema[0].package.package_id, 'testpackage0')
        self.assertEqual(schema[0].resourcetype.resourcetype_id, 'weapon')
        self.assertEqual(schema[0].type, 'xsd')
        res = schema[0].resource
        self.assertEqual(res.document.data, TEST_SCHEMA)
        self.assertEqual(res.package.package_id, 'seishub')
        self.assertEqual(res.resourcetype.resourcetype_id, 'schema')
        self.assertRaises(SeisHubError, self.env.registry.schemas.register, 'testpackage0', None, 'xsd', TEST_SCHEMA)
        schemas = self.env.registry.schemas.get(package_id='testpackage0')
        self.assertEqual(len(schemas), 2)
        self.assertEqual(schemas[0].package.package_id, 'testpackage0')
        self.assertEqual(schemas[0].resourcetype.resourcetype_id, 'weapon')
        self.assertEqual(schemas[0].type, 'xsd')
        self.assertEqual(schemas[1].package.package_id, 'testpackage0')
        self.assertEqual(schemas[1].resourcetype.resourcetype_id, 'armor')
        self.assertEqual(schemas[1].type, 'xsd')
        schemas = self.env.registry.schemas.get(uri='/testpackage0/xsd')
        self.assertEqual(len(schemas), 0)
        schemas = self.env.registry.schemas.get(uri='/testpackage0/weapon')
        self.assertEqual(len(schemas), 1)
        schemas = self.env.registry.schemas.get(uri='/testpackage0/weapon/xsd')
        self.assertEqual(len(schemas), 1)
        schemas = self.env.registry.schemas
        self.assertEqual(len(schemas), 2)
        self.env.registry.schemas.delete(schema[0].package.package_id, schema[0].resourcetype.resourcetype_id, schema[0].type)
        schema = self.env.registry.schemas.get(package_id='testpackage0')
        self.assertEqual(len(schema), 1)
        self.assertEqual(schema[0].resourcetype.resourcetype_id, 'armor')
        self.env.registry.schemas.delete(uri='/testpackage0/armor')
        schema = self.env.registry.schemas.get(package_id='testpackage0')
        self.assertEqual(len(schema), 0)
        return

    def test_StylesheetRegistry(self):
        self.env.registry.stylesheets.register('testpackage0', 'weapon', 'xhtml', TEST_STYLESHEET)
        self.env.registry.stylesheets.register('testpackage0', None, 'xhtml', TEST_STYLESHEET)
        stylesheet = self.env.registry.stylesheets.get(package_id='testpackage0', resourcetype_id='weapon')
        self.assertEqual(len(stylesheet), 1)
        self.assertEqual(stylesheet[0].package.package_id, 'testpackage0')
        self.assertEqual(stylesheet[0].resourcetype.resourcetype_id, 'weapon')
        self.assertEqual(stylesheet[0].type, 'xhtml')
        self.assertEquals(stylesheet[0].content_type, 'application/json')
        stylesheet_nort = self.env.registry.stylesheets.get(package_id='testpackage0')
        self.assertEqual(len(stylesheet_nort), 1)
        self.assertEqual(stylesheet_nort[0].package.package_id, 'testpackage0')
        self.assertEqual(stylesheet_nort[0].resourcetype.resourcetype_id, None)
        res_list = Resource(document=newXMLDocument(TEST_RESLIST))
        self.assertEquals(stylesheet[0].transform(res_list), '{"mapping":["/seishub/schema/browser"],"resource"' + ':["/seishub/schema/3","/seishub/schema/4"],}')
        self.assertEquals(stylesheet[0].transform(TEST_RESLIST), '{"mapping":["/seishub/schema/browser"],"resource"' + ':["/seishub/schema/3","/seishub/schema/4"],}')
        res = stylesheet[0].resource
        self.assertEqual(res.document.data, TEST_STYLESHEET)
        self.assertEqual(res.package.package_id, 'seishub')
        self.assertEqual(res.resourcetype.resourcetype_id, 'stylesheet')
        self.env.registry.stylesheets.delete(stylesheet[0].package.package_id, stylesheet[0].resourcetype.resourcetype_id, stylesheet[0].type)
        stylesheet = self.env.registry.stylesheets.get(package_id='testpackage0', resourcetype_id='weapon')
        self.assertEqual(len(stylesheet), 0)
        self.env.registry.stylesheets.delete('testpackage0', None, 'xhtml')
        stylesheet_nort = self.env.registry.stylesheets.get(package_id='testpackage0')
        self.assertEqual(len(stylesheet_nort), 0)
        return

    def test_AliasRegistry(self):
        self.env.registry.aliases.register('arch1', '/weapon[./name = Bogen]')
        self.env.registry.aliases.register('arch2', '/*[./name = Bogen]')
        alias = self.env.registry.aliases.get(uri='arch1')
        self.assertEqual(len(alias), 1)
        self.assertEqual(alias[0].uri, 'arch1')
        self.assertEqual(alias[0].expr, '/weapon[./name = Bogen]')
        alias = self.env.registry.aliases.get(expr='/*[./name = Bogen]')
        self.assertEqual(len(alias), 1)
        self.assertEqual(alias[0].uri, 'arch2')
        self.assertEqual(alias[0].expr, '/*[./name = Bogen]')
        all = self.env.registry.aliases.get()
        assert len(all) >= 2
        self.env.registry.aliases.delete('arch1')
        alias = self.env.registry.aliases.get(uri='arch1')
        self.assertEquals(alias, list())
        self.env.registry.aliases.delete('arch2')
        alias = self.env.registry.aliases.get()
        self.assertEquals(alias, list())

    def test_addInvalidSchema(self):
        """
        Adding an invalid schema should be catched if registering the schema.
        """
        self.env.registry.db_registerPackage('test-catalog')
        self.env.registry.db_registerResourceType('test-catalog', 'schema')
        self.assertRaises(InvalidObjectError, self.env.registry.schemas.register, 'test-catalog', 'schema', 'XMLSchema', '<invalid>')
        self.env.catalog.addResource('test-catalog', 'schema', RAW_XML, name='muh.xml')
        self.env.registry.db_deleteResourceType('test-catalog', 'schema')
        self.env.registry.db_deletePackage('test-catalog')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PackageRegistryTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')