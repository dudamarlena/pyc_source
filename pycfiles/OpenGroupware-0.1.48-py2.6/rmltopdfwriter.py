# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/doc/rmltopdfwriter.py
# Compiled at: 2012-10-12 07:02:39
import zope.interface
from lxml import etree
from z3c.rml import document as RMLDocument
from z3c.rml import interfaces
zope.interface.moduleProvides(interfaces.IRML2PDF)

class RMLToPDFWriter(object):

    def __init__(self, rfile):
        root = etree.parse(rfile).getroot()
        self.doc = RMLDocument.Document(root)

    def write(self, wfile):
        self.doc.process(wfile)

    def close(self):
        self.doc = None
        return