# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy-optional/xmlschema_acue/components/xmlschema_acue/tests/xmlschema_acue_tests/testtools/TestCaseXMLSchema.py
# Compiled at: 2019-05-19 15:23:49
# Size of source mod 2**32: 8962 bytes
"""
Tests subpackage module: common definitions for unittest scripts of the 'xmlschema' package.
"""
import unittest, platform, re, os, xmlschema_acue as xmlschema
from xmlschema_acue import XMLSchema
from xmlschema_acue.compat import urlopen, URLError, unicode_type
from xmlschema_acue.exceptions import XMLSchemaValueError
from xmlschema_acue.etree import is_etree_element, etree_element, etree_register_namespace, etree_elements_assert_equal
from xmlschema_acue.resources import fetch_namespaces
from xmlschema_acue.qnames import XSD_SCHEMA
from xmlschema_acue.helpers import get_namespace
from xmlschema_acue.namespaces import XSD_NAMESPACE
from testdata.xmlschema_acue_testdata import testdata_dir

def has_network_access(*locations):
    for url in locations:
        try:
            urlopen(url, timeout=5)
        except (URLError, OSError):
            pass
        else:
            return True

    return False


SKIP_REMOTE_TESTS = not has_network_access('http://www.sissa.it', 'http://www.w3.org/', 'http://dublincore.org/')
PROTECTED_PREFIX_PATTERN = re.compile('ns\\d:')

def print_test_header():
    header1 = 'Test %r' % xmlschema
    header2 = 'with Python {} on platform {}'.format(platform.python_version(), platform.platform())
    print('{0}\n{1}\n{2}\n{0}'.format('*' * max(len(header1), len(header2)), header1, header2))


class XMLSchemaTestCase(unittest.TestCase):
    __doc__ = "\n    XMLSchema TestCase class.\n\n    Setup tests common environment. The tests parts have to use empty prefix for\n    XSD namespace names and 'ns' prefix for XMLSchema test namespace names.\n    "
    etree_register_namespace(prefix='', uri=XSD_NAMESPACE)
    etree_register_namespace(prefix='ns', uri='ns')
    SCHEMA_TEMPLATE = '<?xml version="1.0" encoding="UTF-8"?>\n    <schema xmlns:ns="ns" xmlns="http://www.w3.org/2001/XMLSchema" \n        targetNamespace="ns" elementFormDefault="unqualified" version="{0}">\n        {1}\n    </schema>'
    schema_class = XMLSchema

    @classmethod
    def setUpClass(cls):
        cls.errors = []
        cls.xsd_types = cls.schema_class.builtin_types()
        cls.content_pattern = re.compile('(<|<xs:)(sequence|choice|all)')
        cls.default_namespaces = {'xsi':'http://www.w3.org/2001/XMLSchema-instance', 
         'tns':'http://xmlschema.test/ns', 
         'ns':'ns'}
        cls.vh_dir = cls.casepath(testdata_dir + 'examples/vehicles')
        cls.vh_xsd_file = cls.casepath(testdata_dir + 'examples/vehicles/vehicles.xsd')
        cls.vh_xml_file = cls.casepath(testdata_dir + 'examples/vehicles/vehicles.xml')
        cls.vh_json_file = cls.casepath(testdata_dir + 'examples/vehicles/vehicles.json')
        cls.vh_schema = cls.schema_class(cls.vh_xsd_file)
        cls.vh_namespaces = fetch_namespaces(cls.vh_xml_file)
        cls.col_dir = cls.casepath(testdata_dir + 'examples/collection')
        cls.col_xsd_file = cls.casepath(testdata_dir + 'examples/collection/collection.xsd')
        cls.col_xml_file = cls.casepath(testdata_dir + 'examples/collection/collection.xml')
        cls.col_json_file = cls.casepath(testdata_dir + 'examples/collection/collection.json')
        cls.col_schema = cls.schema_class(cls.col_xsd_file)
        cls.col_namespaces = fetch_namespaces(cls.col_xml_file)
        cls.st_xsd_file = cls.casepath(testdata_dir + 'features/decoder/simple-types.xsd')
        cls.st_schema = cls.schema_class(cls.st_xsd_file)
        cls.models_xsd_file = cls.casepath(testdata_dir + 'features/models/models.xsd')
        cls.models_schema = cls.schema_class(cls.models_xsd_file)

    @classmethod
    def casepath(cls, path):
        """
        Returns the absolute path of a test case file.

        :param path: the relative path of the case file from base dir ``xmlschema/tests/test_cases/``.
        """
        return os.path.join(testdata_dir, path)

    def retrieve_schema_source(self, source):
        """
        Returns a schema source that can be used to create an XMLSchema instance.

        :param source: A string or an ElementTree's Element.
        :return: An schema source string, an ElementTree's Element or a full pathname.
        """
        if is_etree_element(source):
            if source.tag in (XSD_SCHEMA, 'schema'):
                return source
            if get_namespace(source.tag):
                raise XMLSchemaValueError('source %r namespace has to be empty.' % source)
            else:
                if source.tag not in frozenset({'complexType', 'attribute', 'attributeGroup', 'simpleType', 'notation', 'group', 'element'}):
                    raise XMLSchemaValueError('% is not an XSD global definition/declaration.' % source)
            root = etree_element('schema', attrib={'xmlns:ns':'ns', 
             'xmlns':'http://www.w3.org/2001/XMLSchema', 
             'targetNamespace':'ns', 
             'elementFormDefault':'qualified', 
             'version':self.schema_class.XSD_VERSION})
            root.append(source)
            return root
        else:
            source = source.strip()
            if not source.startswith('<'):
                return self.casepath(source)
            return self.SCHEMA_TEMPLATE.format(self.schema_class.XSD_VERSION, source)

    def get_schema(self, source):
        return self.schema_class(self.retrieve_schema_source(source))

    def get_element(self, name, **attrib):
        source = '<element name="{}" {}/>'.format(name, ' '.join('%s="%s"' % (k, v) for k, v in attrib.items()))
        schema = self.schema_class(self.retrieve_schema_source(source))
        return schema.elements[name]

    def check_etree_elements(self, elem, other):
        """Checks if two ElementTree elements are equal."""
        try:
            self.assertIsNone(etree_elements_assert_equal(elem, other, strict=False, skip_comments=True))
        except AssertionError as err:
            self.assertIsNone(err, None)

    def check_namespace_prefixes(self, s):
        """Checks that a string doesn't contain protected prefixes (ns0, ns1 ...)."""
        match = PROTECTED_PREFIX_PATTERN.search(s)
        if match:
            msg = 'Protected prefix {!r} found:\n {}'.format(match.group(0), s)
            self.assertIsNone(match, msg)

    def check_errors(self, path, expected):
        """
        Checks schema or validation errors, checking information completeness of the
        instances and those number against expected.

        :param path: the path of the test case.
        :param expected: the number of expected errors.
        """
        for e in self.errors:
            error_string = unicode_type(e)
            self.assertTrue(e.path, 'Missing path for: %s' % error_string)
            self.assertTrue(e.namespaces, 'Missing namespaces for: %s' % error_string)
            self.check_namespace_prefixes(error_string)

        if not self.errors:
            if expected:
                raise ValueError('{!r}: found no errors when {} expected.'.format(path, expected))
        if len(self.errors) != expected:
            num_errors = len(self.errors)
            if num_errors == 1:
                msg = '{!r}: n.{} errors expected, found {}:\n\n{}'
            else:
                if num_errors <= 5:
                    msg = '{!r}: n.{} errors expected, found {}. Errors follow:\n\n{}'
                else:
                    msg = '{!r}: n.{} errors expected, found {}. First five errors follow:\n\n{}'
                error_string = '\n++++++++++\n\n'.join([unicode_type(e) for e in self.errors[:5]])
                raise ValueError(msg.format(path, expected, len(self.errors), error_string))

    def check_schema(self, source, expected=None, **kwargs):
        """
        Create a schema for a test case.

        :param source: A relative path or a root Element or a portion of schema for a template.
        :param expected: If it's an Exception class test the schema for raise an error.         Otherwise build the schema and test a condition if expected is a callable, or make         a substring test if it's not `None` (maybe a string). Then returns the schema instance.
        """
        if isinstance(expected, type):
            if issubclass(expected, Exception):
                (self.assertRaises)(expected, (self.schema_class), (self.retrieve_schema_source(source)), **kwargs)
        else:
            schema = (self.schema_class)((self.retrieve_schema_source(source)), **kwargs)
            if callable(expected):
                self.assertTrue(expected(schema))
            return schema