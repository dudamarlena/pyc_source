# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boo_box/tests/test.py
# Compiled at: 2008-05-19 10:38:41
import boo_box
from boo_box.affiliates import submarino
from xml.dom.minidom import parseString, Document
from nose.tools import raises

class TestBooBox(object):
    __module__ = __name__

    def test_json(self):
        boo = boo_box.Box(submarino, '173097').get('JSON', 'livros json')
        assert boo.startswith('jsonBooboxApi')

    def test_xml(self):
        boo = boo_box.Box(submarino, '173097').get('XML', 'livros xml')
        xmltree = parseString(boo)
        assert isinstance(xmltree, Document)

    def test_object(self):
        boo = boo_box.Box(submarino, '173097').get('object', 'livros xml')
        assert isinstance(boo, dict)

    @raises(NotImplementedError)
    def test_pdf(self):
        boo = boo_box.Box(submarino, '173097').get('pdf', 'livros xml')