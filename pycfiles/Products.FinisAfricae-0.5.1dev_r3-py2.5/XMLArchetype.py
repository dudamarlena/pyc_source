# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/FinisAfricae/content/XMLArchetype.py
# Compiled at: 2008-07-28 16:57:25
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.Archetypes.public import *
from Products.validation import V_REQUIRED
from Products.validation.config import validation
from Products.FinisAfricae import validators
from StringIO import StringIO
from lxml import etree
XMLArchetypeSchema = Schema((
 TextField('xmlData', validators=(
  (
   'isValidXmlSyntax', V_REQUIRED),), required=True, widget=TextAreaWidget(rows=45, label='XML data', label_msgid='label_email', description='Enter raw XML data here', description_msgid='help_email')),))

class XMLArchetype:
    """

    """
    _v_xslt_cache = {}

    def pretty_print_xmlData(self):
        """
        
        reformat XML data pretty printing them
        """
        xmlField = self.getField('xmlData')
        f = StringIO(xmlField.getRaw(self))
        tree = etree.parse(f, etree.XMLParser(remove_blank_text=True))
        self.setXmlData(etree.tostring(tree.getroot(), pretty_print=True))

    def getXmlTree(self):
        """
        
        """
        xmlField = self.getField('xmlData')
        f = StringIO(xmlField.getRaw(self))
        return etree.parse(f)

    def getXslT(self, styleSheet):
        """
        compiles XSL contained in 'styleSheet'
        saves compiled XSLTs with simple caching scheme
        
        returns XSLT
        """
        if self._v_xslt_cache is None:
            self._v_xslt_cache = {}
        styleSheetHash = hash(styleSheet)
        try:
            xslt_transform = self._v_xslt_cache[styleSheetHash]
        except KeyError:
            xslt_stringio = StringIO(styleSheet)
            xslt_doc = etree.parse(xslt_stringio)
            xslt_transform = etree.XSLT(xslt_doc)
            self._v_xslt_cache[styleSheetHash] = xslt_transform

        return xslt_transform

    def xslTransform(self, styleSheet=None, styleSheetName=None, description='XML->HTML transformation'):
        """
        styleSheet: string containing style sheet or
        styleSheetName: name of resource that contains it
        
        either styleSheet or styleSheetName should not be None

        returns HTML formatted error or XSL result
        """
        if styleSheet is None:
            try:
                styleSheet = self.restrictedTraverse(styleSheetName)._readFile(0)
            except AttributeError, e:
                return self.formatHtmlError('INTERNAL ERROR', "'%s' not found! %s failed!" % (styleSheetName, description), e)

        try:
            xslT = self.getXslT(styleSheet)
        except etree.XMLSyntaxError, e:
            return self.formatHtmlError('INTERNAL ERROR', '%s failed, styleSheet has errors!' % description, e)

        xmlField = self.getField('xmlData')
        f = StringIO(xmlField.getRaw(self))
        try:
            doc = etree.parse(f)
            html_data = str(xslT(doc))
        except etree.XMLSyntaxError, e:
            return self.formatHtmlError('ERROR', 'XML Data is not valid, when doing %s!' % description, e)

        return html_data

    def formatHtmlError(self, error_type, description, e):
        return '<div><b>%s:</b> %s<br/>%s</div>' % (error_type, description, str(e))