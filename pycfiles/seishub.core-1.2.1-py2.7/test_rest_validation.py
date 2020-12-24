# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest_validation.py
# Compiled at: 2010-12-23 17:42:43
"""
A test suite for validating PUT requests on REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.exceptions import SeisHubError
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.packages.installer import registerSchema
from seishub.core.processor import PUT, DELETE, Processor
from seishub.core.processor.resources import RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import os, unittest
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n%s'
XML_VALID_SCHEMATRON = '<?xml version="1.0" encoding="utf-8"?>\n\n<Total>\n   <Percent>20</Percent>\n   <Percent>30</Percent>\n   <Percent>50</Percent>\n</Total>'
XML_INVALID_SCHEMATRON = '<?xml version="1.0" encoding="utf-8"?>\n\n<Total>\n   <Percent>21</Percent>\n   <Percent>30</Percent>\n   <Percent>50</Percent>\n</Total>'

class APackage(Component):
    """
    A test package.
    """
    implements(IPackage)
    package_id = 'validation-test'


class SchematronResourceType(Component):
    """
    A test resource type which includes a Schematron validation schema.
    """
    implements(IResourceType)
    package_id = 'validation-test'
    resourcetype_id = 'schematron'
    registerSchema('data' + os.sep + 'validation' + os.sep + 'schematron.sch', 'Schematron')


class RelaxNGResourceType(Component):
    """
    A test resource type which includes a RelaxNG validation schema.
    """
    implements(IResourceType)
    package_id = 'validation-test'
    resourcetype_id = 'relaxng'
    registerSchema('data' + os.sep + 'validation' + os.sep + 'relaxng.rng', 'RelaxNG')


class XMLSchemaResourceType(Component):
    """
    A test resource type including a XMLSchema validation schema.
    """
    implements(IResourceType)
    package_id = 'validation-test'
    resourcetype_id = 'xmlschema'
    registerSchema('data' + os.sep + 'validation' + os.sep + 'xmlschema.xsd', 'XMLSchema')


class MultipleXMLSchemaResourceType(Component):
    """
    A test resource type including multiple validation schema.
    """
    implements(IResourceType)
    package_id = 'validation-test'
    resourcetype_id = 'multi'
    registerSchema('data' + os.sep + 'validation' + os.sep + 'xmlschema.xsd', 'XMLSchema')
    registerSchema('data' + os.sep + 'validation' + os.sep + 'relaxng.rng', 'RelaxNG')


class RestValidationTests(SeisHubEnvironmentTestCase):
    """
    A test suite for validating PUT requests on REST resources.
    """

    def setUp(self):
        self.env.enableComponent(APackage)
        self.env.enableComponent(XMLSchemaResourceType)
        self.env.enableComponent(MultipleXMLSchemaResourceType)
        self.env.enableComponent(RelaxNGResourceType)
        self.env.enableComponent(SchematronResourceType)
        self.env.tree = RESTFolder()

    def tearDown(self):
        for schema in self.env.registry.schemas.get('validation-test'):
            self.env.registry.schemas.delete(document_id=schema.document_id)

        for rt in self.env.registry.getResourceTypeIds('validation-test'):
            self.env.registry.db_deleteResourceType('validation-test', rt)

        self.env.registry.db_deletePackage('validation-test')

    def test_validateRelaxNG(self):
        """
        Validate uploaded resource with RelaxNG.
        """
        proc = Processor(self.env)
        proc.run(PUT, '/validation-test/relaxng/valid.xml', StringIO(XML_DOC % '<a><b></b></a>'))
        try:
            proc.run(PUT, '/validation-test/relaxng/invalid.xml', StringIO(XML_DOC % '<a><c></c></a>'))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.CONFLICT)

        proc.run(DELETE, '/validation-test/relaxng/valid.xml')
        try:
            proc.run(DELETE, '/validation-test/relaxng/invalid.xml')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_validateSchematron(self):
        """
        Validate uploaded resource with Schematron.
        """
        proc = Processor(self.env)
        proc.run(PUT, '/validation-test/schematron/valid.xml', StringIO(XML_VALID_SCHEMATRON))
        try:
            proc.run(PUT, '/validation-test/schematron/invalid.xml', StringIO(XML_INVALID_SCHEMATRON))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.CONFLICT)

        proc.run(DELETE, '/validation-test/schematron/valid.xml')
        try:
            proc.run(DELETE, '/validation-test/schematron/invalid.xml')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_validateXMLSchema(self):
        """
        Validate uploaded resource with XMLSchema.
        """
        proc = Processor(self.env)
        proc.run(PUT, '/validation-test/xmlschema/valid.xml', StringIO(XML_DOC % '<a><b></b></a>'))
        try:
            proc.run(PUT, '/validation-test/xmlschema/invalid.xml', StringIO(XML_DOC % '<b><a/></b>'))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.CONFLICT)

        proc.run(DELETE, '/validation-test/xmlschema/valid.xml')
        try:
            proc.run(DELETE, '/validation-test/xmlschema/invalid.xml')
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.NOT_FOUND)

    def test_validateMultipleSchemas(self):
        """
        Validate uploaded resource with multiple schemas.
        """
        proc = Processor(self.env)
        proc.run(PUT, '/validation-test/multi/valid.xml', StringIO(XML_DOC % '<a><b></b></a>'))
        try:
            proc.run(PUT, '/validation-test/multi/invalid.xml', StringIO(XML_DOC % '<b><a/></b>'))
            self.fail('Expected SeisHubError')
        except SeisHubError as e:
            self.assertEqual(e.code, http.CONFLICT)

        proc.run(DELETE, '/validation-test/multi/valid.xml')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestValidationTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')