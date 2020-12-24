# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uche/dev/amara/test/tree/test_basics.py
# Compiled at: 2011-01-03 15:32:39
import unittest
from amara import parse
from xml.dom import Node
from amara import tree
import os, tempfile
MONTY_XML = '<monty><python spam="eggs">What do you mean "bleh"</python><python ministry="abuse">But I was looking for argument</python></monty>'
NS_XML = '<doc xmlns:a="urn:bogus:a" xmlns:b="urn:bogus:b">\n  <a:monty/>\n  <b:python/>\n</doc>'
TEST_URL = 'http://cvs.4suite.org/viewcvs/*checkout*/4Suite/test/Xml/Core/disclaimer.xml'

class Test_parse_functions_1(unittest.TestCase):
    """Testing local sources"""

    def run_checks(self, doc):
        """Parse with string"""
        self.assertEqual(len(doc.xml_children), 1)
        self.assertEqual(doc.xml_children[0].xml_type, tree.element.xml_type)
        self.assertEqual(doc.xml_children[0].xml_qname, 'monty')
        self.assertEqual(doc.xml_children[0].xml_namespace, None)
        self.assertEqual(doc.xml_children[0].xml_prefix, None)
        self.assertEqual(len(doc.xml_first_child.xml_children), 2)
        self.assertEqual(doc.xml_children[0].xml_children[0].xml_type, tree.element.xml_type)
        self.assertEqual(doc.xml_children[0].xml_children[0].xml_qname, 'python')
        self.assertEqual(doc.xml_children[0].xml_children[0].xml_namespace, None)
        self.assertEqual(doc.xml_children[0].xml_children[0].xml_prefix, None)
        self.assertEqual(len(list(doc.xml_select('//python'))), 2)
        self.assertEqual((';').join([ e.xml_qname for e in doc.xml_select('//python') ]), 'python;python')
        return

    def test_parse_with_string(self):
        """Parse with string"""
        doc = parse(MONTY_XML)
        self.run_checks(doc)

    def test_parse_with_stream(self):
        """Parse with stream"""
        fname = tempfile.mktemp('.xml')
        fout = open(fname, 'w')
        fout.write(MONTY_XML)
        fout.close()
        fout = open(fname, 'r')
        doc = parse(fout)
        fout.close()
        self.run_checks(doc)

    def test_parse_with_file_path(self):
        """Parse with file path"""
        fname = tempfile.mktemp('.xml')
        fout = open(fname, 'w')
        fout.write(MONTY_XML)
        fout.close()
        doc = parse(fname)
        self.run_checks(doc)


class Test_parse_functions_2(unittest.TestCase):
    """Convenience parse functions, part 2. 
    May be slow; requires Internet connection"""

    def Xtest_parse_with_url(self):
        doc = parse(TEST_URL)
        self.assertEqual(len(doc.xml_children), 1)
        self.assertEqual(doc.xml_children[0].xml_type, tree.element.xml_type)
        self.assertEqual(doc.xml_children[0].xml_qname, 'disclaimer')
        self.assertEqual(doc.xml_children[0].xml_namespace, None)
        self.assertEqual(doc.xml_children[0].xml_prefix, None)
        return


class Test_attributes(unittest.TestCase):

    def test_ticket_8(self):
        """Test for ticket #8 bug"""
        text = '<row a="" b="" c="" d="" e="" f=""/>'
        doc = parse(text)
        row = doc.xml_select('row')[0]
        attrs = row.xml_attributes
        for k in attrs.keys():
            self.assertTrue(k in attrs)
            self.assertEqual(attrs[k], '')
            self.assertEqual(getattr(row, k[1]), '')

        for k in [(None, 'g'), (None, 'h'), (None, 'z')]:
            self.assertFalse(k in attrs)

        return


if __name__ == '__main__':
    raise SystemExit('use nosetests')