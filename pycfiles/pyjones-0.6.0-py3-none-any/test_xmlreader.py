# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyjon/descriptors/tests/test_xmlreader.py
# Compiled at: 2015-01-20 10:16:16
from six import next
import unittest
from pyjon.descriptors.tests.test_utils import get_descriptor, basetestdir
from pyjon.descriptors.tests.test_utils import open_file
from pyjon.descriptors.readers import XMLReader
from pyjon.descriptors.exceptions import MissingFieldError
from pyjon.descriptors.exceptions import InvalidDescriptorError
from xml.etree import cElementTree as ET

class TestXMLReader(unittest.TestCase):

    def test_descriptor_xml(self):
        """test that XML descriptors work as expected
        """
        schema_filename = '%s/xml_desc_thirdparty.xml' % basetestdir
        sourcefilename = '%s/xml_thirdparty_exemple.xml' % basetestdir
        d = get_descriptor(schema_filename, 'utf-8')
        source = open_file(sourcefilename, 'rb')
        items = d.read(source)
        for item in items:
            assert item.name == 'some name'
            assert item.thirdparty_id == 'uniqueid'
            assert item.account_code == 'accountcode'
            assert item.type == 'client'
            assert item.address4 == 'addr4'

    def test_descriptor_xml_xpath(self):
        """test that XML descriptors work as expected with xpath expressions
        """
        schema_filename = '%s/xml_desc_thirdparty_xpath.xml' % basetestdir
        sourcefilename = '%s/xml_thirdparty_xpath_exemple.xml' % basetestdir
        d = get_descriptor(schema_filename, 'utf-8')
        source = open_file(sourcefilename, 'rb')
        items = d.read(source)
        for item in items:
            assert item.name == 'some name'
            assert item.thirdparty_id == 'uniqueid'
            assert item.account_code == 'accountcode'
            assert item.type == 'client'
            assert item.analysis6 == 'an6'
            assert item.bankfield2 == 'bkf2'
            assert item.address4 == 'addr4'

    def test_xreader_exception_when_mandatory_field_is_missing(self):
        schema_filename = '%s/xml_desc_ledger_exemple_0.xml' % basetestdir
        sourcefilename = '%s/xml_ledger_exemple_0.xml' % basetestdir
        d = get_descriptor(schema_filename, 'iso-8859-1')
        source = open_file(sourcefilename, 'rb')
        item_iter = d.read(source)
        self.assertRaises(MissingFieldError, lambda : next(item_iter))

    def test_xreader_no_exc_when_non_mandatory_field_missing(self):
        schema_filename = '%s/xml_desc_ledger_exemple_1.xml' % basetestdir
        sourcefilename = '%s/xml_ledger_exemple_1.xml' % basetestdir
        d = get_descriptor(schema_filename, 'iso-8859-1')
        source = open_file(sourcefilename, 'rb')
        item_iter = d.read(source)
        item = next(item_iter)
        assert None == item.JournalType
        return

    def test_xmlreader_notext(self):
        """test that the InvalidDescriptorError exception is returned
        on specific invalid schema
        """
        schema_filename = '%s/xml_desc_ledger_invaliddatanode.xml' % basetestdir
        encoding = 'utf-8'
        schema = ET.parse(schema_filename)
        self.assertRaises(InvalidDescriptorError, XMLReader, encoding, schema)