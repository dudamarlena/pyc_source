# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/load.py
# Compiled at: 2020-01-18 11:47:38
from defusedxml.sax import make_parser
from xml.sax import handler
from xml.sax.xmlreader import InputSource
import xml.sax.saxutils
from odf.element import Element
from odf.namespaces import OFFICENS
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

class LoadParser(handler.ContentHandler):
    """ Extract headings from content.xml of an ODT file """
    triggers = (
     (
      OFFICENS, 'automatic-styles'), (OFFICENS, 'body'),
     (
      OFFICENS, 'font-face-decls'), (OFFICENS, 'master-styles'),
     (
      OFFICENS, 'meta'), (OFFICENS, 'scripts'),
     (
      OFFICENS, 'settings'), (OFFICENS, 'styles'))

    def __init__(self, document):
        self.doc = document
        self.data = []
        self.level = 0
        self.parse = False

    def characters(self, data):
        if self.parse == False:
            return
        self.data.append(data)

    def startElementNS(self, tag, qname, attrs):
        if tag in self.triggers:
            self.parse = True
        if self.doc._parsing != 'styles.xml' and tag == (OFFICENS, 'font-face-decls'):
            self.parse = False
        if self.parse == False:
            return
        self.level = self.level + 1
        content = ('').join(self.data)
        if content:
            self.parent.addText(content, check_grammar=False)
            self.data = []
        attrdict = {}
        for att, value in attrs.items():
            attrdict[att] = value

        try:
            e = Element(qname=tag, qattributes=attrdict, check_grammar=False)
            self.curr = e
        except AttributeError as v:
            print 'Error: %s' % v

        if tag == (OFFICENS, 'automatic-styles'):
            e = self.doc.automaticstyles
        elif tag == (OFFICENS, 'body'):
            e = self.doc.body
        elif tag == (OFFICENS, 'master-styles'):
            e = self.doc.masterstyles
        elif tag == (OFFICENS, 'meta'):
            e = self.doc.meta
        elif tag == (OFFICENS, 'scripts'):
            e = self.doc.scripts
        elif tag == (OFFICENS, 'settings'):
            e = self.doc.settings
        elif tag == (OFFICENS, 'styles'):
            e = self.doc.styles
        elif self.doc._parsing == 'styles.xml' and tag == (OFFICENS, 'font-face-decls'):
            e = self.doc.fontfacedecls
        elif hasattr(self, 'parent'):
            self.parent.addElement(e, check_grammar=False)
        self.parent = e

    def endElementNS(self, tag, qname):
        if self.parse == False:
            return
        self.level = self.level - 1
        str = ('').join(self.data)
        if str:
            self.curr.addText(str, check_grammar=False)
        self.data = []
        self.curr = self.curr.parentNode
        self.parent = self.curr
        if tag in self.triggers:
            self.parse = False