# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/FinisAfricae/validators/XmlValidators.py
# Compiled at: 2008-05-28 16:46:08
from lxml import etree
from StringIO import StringIO
from Products.validation.interfaces.IValidator import IValidator
from Products.CMFCore.utils import getToolByName

class xmlSyntaxValidator:
    __implements__ = IValidator

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        f = StringIO(value)
        try:
            doc = etree.parse(f)
        except etree.XMLSyntaxError, e:
            return 'XML Syntax Invalid. Error: %s' % e

        return


class xmlSchemaValidator:
    __implements__ = IValidator

    def __init__(self, name, *args, **kw):
        self.name = name
        self.xsd = kw.get('xsd', None)
        self.errmsg = kw.get('errmsg', 'fails tests of %s' % name)
        return

    def __call__(self, value, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        try:
            f = StringIO(value)
            doc = etree.parse(f)
        except etree.XMLSyntaxError, e:
            return 'XML Syntax Invalid. Error: %s' % e

        try:
            xsdSchema = self.restrictedTraverse(self.xsd)._readFile(0)
            xsd_stringio = StringIO(xsdSchema)
            xsd_doc = etree.parse(xslt_stringio)
            xsd_schema = etree.XMLSchema(xsd_doc)
        except AttributeError, e:
            return "INTERNAL ERROR '%s' not found! Schema validation failed! %s" % (self.xsd, str(e))
        except etree.XMLSyntaxError, e:
            return "INTERNAL ERROR '%s' is not valid! Schema validation failed! %s" % (self.xsd, str(e))

        if xsd_schema.validate(doc):
            return
        else:
            return '%s\n%s' % (self.errmsg, xsd_schema.error_log)
        return