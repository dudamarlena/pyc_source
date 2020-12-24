# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/test_create.py
# Compiled at: 2008-04-01 12:07:15
import os, sys, unittest, tempfile
from lxml import etree
from StringIO import StringIO
from docbook2sla import DocBook2Sla
dirname = os.path.dirname(__file__)
scribus_schema = os.path.join(os.path.dirname(__file__), '..', 'schema', 'scribus.xsd')
xmlschema_doc = etree.parse(scribus_schema)
xmlschema = etree.XMLSchema(xmlschema_doc)

class ArticleTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        scribus = os.path.join(os.path.dirname(__file__), 'data', 'scribus', 'clean134.sla')
        article = os.path.join(os.path.dirname(__file__), 'data', 'xml', 'article+id.xml')
        self.d2s = DocBook2Sla()
        outputfn = self.d2s.create(article, scribus)
        output = open(outputfn, 'r').read()
        outputtree = etree.XML(output)
        self.output = output
        self.outputtree = outputtree

    def testValidateOutput(self):
        """ Validate output against XML Schema """
        doc = etree.parse(StringIO(self.output))
        valid = xmlschema.validate(doc)
        self.assertEqual(valid, True, xmlschema.assertValid(doc))

    def test_create_article(self):
        """ Test create() function with DocBook article """
        root_node = self.outputtree.xpath('name(/*)')
        self.assertEqual(root_node, 'SCRIBUSUTF8NEW')
        count_pageobjects = self.outputtree.xpath('count(//PAGEOBJECT)')
        self.assertEqual(count_pageobjects, 4.0)


class BookTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        scribus = os.path.join(os.path.dirname(__file__), 'data', 'scribus', 'clean134.sla')
        book = os.path.join(os.path.dirname(__file__), 'data', 'xml', 'book+id.xml')
        self.d2s = DocBook2Sla()
        outputfn = self.d2s.create(book, scribus)
        output = open(outputfn, 'r').read()
        outputtree = etree.XML(output)
        self.output = output
        self.outputtree = outputtree

    def testValidateOutput(self):
        """ Validate output against XML Schema """
        doc = etree.parse(StringIO(self.output))
        valid = xmlschema.validate(doc)
        self.assertEqual(valid, True, xmlschema.assertValid(doc))

    def test_create_book(self):
        """ Test create() function with DocBook book """
        count_pageobjects = self.outputtree.xpath('count(//PAGEOBJECT)')
        self.assertEqual(count_pageobjects, 10.0)


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ArticleTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(BookTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    return suite


if __name__ == '__main__':
    test_suite()