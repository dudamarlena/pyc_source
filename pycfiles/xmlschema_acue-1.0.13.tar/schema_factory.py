# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/xmlschema_acue/components/xmlschema_acue/tests/xmlschema_acue_tests/testtools/schema_factory.py
# Compiled at: 2019-05-19 13:15:11
"""
This module runs tests concerning the building of XSD schemas with the 'xmlschema' package.
"""
from __future__ import print_function, unicode_literals
import pdb, os, pickle, time, warnings
from xmlschema_acue import XMLSchemaBase
from xmlschema_acue.compat import PY3, unicode_type
from xmlschema_acue.etree import lxml_etree
from xmlschema_acue.etree import py_etree_element
from xmlschema_acue.validators import XsdValidator
from xmlschema_acue.xpath import ElementPathContext
from tests.xmlschema_acue_tests.testtools.schema_observers import SchemaObserver
from tests.xmlschema_acue_tests.testtools.TestCaseXMLSchema import XMLSchemaTestCase

def make_schema_test_class(test_file, test_args, test_num, schema_class, check_with_lxml):
    """
    Creates a schema test class.

    :param test_file: the schema test file path.
    :param test_args: line arguments for test case.
    :param test_num: a positive integer number associated with the test case.
    :param schema_class: the schema class to use.
    :param check_with_lxml: if `True` compare with lxml XMLSchema class, reporting anomalies.     Works only for XSD 1.0 tests.
    """
    xsd_file = os.path.relpath(test_file)
    expected_errors = test_args.errors
    expected_warnings = test_args.warnings
    inspect = test_args.inspect
    locations = test_args.locations
    defuse = test_args.defuse
    debug_mode = test_args.debug

    class TestSchema(XMLSchemaTestCase):

        @classmethod
        def setUpClass(cls):
            cls.schema_class = schema_class
            cls.errors = []
            cls.longMessage = True
            if debug_mode:
                print(b'\n##\n## Testing %r schema in debug mode.\n##' % xsd_file)
                pdb.set_trace()

        def check_schema(self):
            if expected_errors > 0:
                xs = schema_class(xsd_file, validation=b'lax', locations=locations, defuse=defuse)
            else:
                xs = schema_class(xsd_file, locations=locations, defuse=defuse)
            self.errors.extend(xs.maps.all_errors)
            if inspect:
                components_ids = set([ id(c) for c in xs.maps.iter_components() ])
                missing = [ c for c in SchemaObserver.components if id(c) not in components_ids ]
                if any([ c for c in missing ]):
                    raise ValueError(b'schema missing %d components: %r' % (len(missing), missing))
            if not inspect and PY3:
                try:
                    obj = pickle.dumps(xs)
                    deserialized_schema = pickle.loads(obj)
                except pickle.PicklingError:
                    for e in xs.maps.iter_components():
                        elem = getattr(e, b'elem', getattr(e, b'root', None))
                        if isinstance(elem, py_etree_element):
                            break
                    else:
                        raise

                else:
                    self.assertTrue(isinstance(deserialized_schema, XMLSchemaBase))
                    self.assertEqual(xs.built, deserialized_schema.built)

            if not inspect and not self.errors:
                context = ElementPathContext(xs)
                elements = [ x for x in xs.iter() ]
                context_elements = [ x for x in context.iter() if isinstance(x, XsdValidator) ]
                self.assertEqual(context_elements, [ x for x in context.iter_descendants() ])
                self.assertEqual(context_elements, elements)
            return

        def check_lxml_schema(self, xmlschema_time):
            start_time = time.time()
            lxs = lxml_etree.parse(xsd_file)
            try:
                lxml_etree.XMLSchema(lxs.getroot())
            except lxml_etree.XMLSchemaParseError as err:
                if not self.errors:
                    print((b'\nSchema error with lxml.etree.XMLSchema for file {!r} ({}): {}').format(xsd_file, self.__class__.__name__, unicode_type(err)))

            if self.errors:
                print((b'\nUnrecognized errors with lxml.etree.XMLSchema for file {!r} ({}): {}').format(xsd_file, self.__class__.__name__, (b'\n++++++\n').join([ unicode_type(e) for e in self.errors ])))
            lxml_schema_time = time.time() - start_time
            if lxml_schema_time >= xmlschema_time:
                print((b'\nSlower lxml.etree.XMLSchema ({:.3f}s VS {:.3f}s) with file {!r} ({})').format(lxml_schema_time, xmlschema_time, xsd_file, self.__class__.__name__))

        def test_xsd_schema(self):
            if inspect:
                SchemaObserver.clear()
            del self.errors[:]
            start_time = time.time()
            if expected_warnings > 0:
                with warnings.catch_warnings(record=True) as (ctx):
                    warnings.simplefilter(b'always')
                    self.check_schema()
                    self.assertEqual(len(ctx), expected_warnings, b'%r: Wrong number of include/import warnings' % xsd_file)
            else:
                self.check_schema()
            if check_with_lxml and lxml_etree is not None:
                self.check_lxml_schema(xmlschema_time=time.time() - start_time)
            self.check_errors(xsd_file, expected_errors)
            return

    TestSchema.__name__ = TestSchema.__qualname__ = str((b'TestSchema{0:03}').format(test_num))
    return TestSchema