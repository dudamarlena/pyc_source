# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\Exslt\Common.py
# Compiled at: 2006-08-22 11:28:15
"""
EXSLT 2.0 - Common (http://www.exslt.org/exsl/index.html)

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import os, tempfile, shutil
from xml.dom import Node
from Ft.Lib import Uri
from Ft.Xml.XPath import Conversions, XPathTypes
from Ft.Xml.Xslt import XsltElement, OutputParameters
from Ft.Xml.Xslt import ContentInfo, AttributeInfo
from Ft.Xml.Xslt import XsltRuntimeException, Error
from Ft.Xml.Xslt.Exslt.MessageSource import Error as ExsltError
from Ft.Xml.XPath import FT_EXT_NAMESPACE
EXSL_COMMON_NS = 'http://exslt.org/common'

def NodeSet(context, obj):
    """
    The purpose of the exsl:node-set function is to return a node-set from a
    result tree fragment. If the argument is a node-set already, it is simply
    returned as is. If the argument to exsl:node-set is not a node-set or a
    result tree fragment, then it is converted to a string as by the string()
    function, and the function returns a node-set consisting of a single text
    node with that string value.

    The exsl:node-set function does not have side-effects: the result tree
    fragment used as an argument is still available as a result tree fragment
    after it is passed as an argument to exsl:node-set.
    """
    if isinstance(obj, XPathTypes.NodesetType):
        return obj
    elif getattr(obj, 'nodeType', None) == Node.DOCUMENT_NODE:
        return [
         obj]
    else:
        s = Conversions.StringValue(obj)
        return [context.node.rootNode.createTextNode(s)]
    return


def ObjectType(context, obj):
    """
    The exsl:object-type function returns a string giving the type of the
    object passed as the argument. The possible object types are: 'string',
    'number', 'boolean', 'node-set', 'RTF' or 'external'.
    """
    if isinstance(obj, XPathTypes.NodesetType):
        return 'node-set'
    elif isinstance(obj, XPathTypes.StringType):
        return 'string'
    elif isinstance(obj, tuple(XPathTypes.NumberTypes)):
        return 'number'
    elif isinstance(obj, XPathTypes.BooleanType):
        return 'boolean'
    elif getattr(obj, 'nodeType', None) == Node.DOCUMENT_NODE:
        return 'RTF'
    else:
        return 'external'
    return


class DocumentElement(XsltElement):
    """
    For the basic specification, see:
    http://www.exslt.org/exsl/elements/document/index.html
    The only URI scheme supported by 4Suite currently is 'file:'
    Security note:
    As a precaution, if you try to overwrite an existing file, it will be
    saved to a temporary file (there will be a warning with the file name).
    If this this precaution fails, the instruction will abort.  You can
    override this precaution, always allowing the function to overwrite
    a document by using the f:overwrite-okay extension attribute.
    """
    __module__ = __name__
    content = ContentInfo.Template
    legalAttrs = {'href': AttributeInfo.UriReferenceAvt(required=1), 'method': AttributeInfo.QNameAvt(), 'version': AttributeInfo.NMTokenAvt(), 'encoding': AttributeInfo.StringAvt(), 'omit-xml-declaration': AttributeInfo.YesNoAvt(), 'standalone': AttributeInfo.YesNoAvt(), 'doctype-public': AttributeInfo.StringAvt(), 'doctype-system': AttributeInfo.StringAvt(), 'cdata-section-elements': AttributeInfo.QNamesAvt(), 'indent': AttributeInfo.YesNoAvt(), 'media-type': AttributeInfo.StringAvt(), 'f:overwrite-safeguard': AttributeInfo.YesNoAvt(default='no', description="Whether or not to make backup copies of any file before it's overwritten."), 'f:utfbom': AttributeInfo.YesNoAvt(default='no', description="Whether to force output of a byte order mark (BOM).  Usually used to generate a UTF-8 BOM.  Do not use this unless you're sure you know what you're doing")}
    doesSetup = True

    def setup(self):
        self._output_parameters = OutputParameters.OutputParameters()
        return

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        self._output_parameters.avtParse(self, context)
        href = self._href.evaluate(context)
        if Uri.IsAbsolute(href):
            uri = href
        else:
            try:
                uri = Uri.Absolutize(href, Uri.OsPathToUri(processor.writer.getStream().name))
            except Exception, e:
                raise XsltRuntimeException(ExsltError.NO_EXSLTDOCUMENT_BASE_URI, context.currentInstruction, href)

            path = Uri.UriToOsPath(uri)
            if self.attributes.get((FT_EXT_NAMESPACE, 'overwrite-safeguard') == 'yes') and os.access(path, os.F_OK):
                savefile = tempfile.mktemp('', os.path.split(path)[(-1)] + '-')
                processor.warn("The file you are trying to create with exsl:document already exists.  As a safety measure it will be copied to a temporary file '%s'." % savefile)
                try:
                    shutil.copyfile(path, savefile)
                except:
                    raise XsltRuntimeException(ExsltError.ABORTED_EXSLDOCUMENT_OVERWRITE, context.currentInstruction, path, savefile)

            try:
                stream = open(path, 'w')
            except IOError:
                dirname = os.path.dirname(path)
                if not os.access(dirname, os.F_OK):
                    os.makedirs(dirname)
                    stream = open(path, 'w')
                else:
                    raise

        processor.addHandler(self._output_parameters, stream)
        try:
            self.processChildren(context, processor)
        finally:
            processor.removeHandler()
            stream.close()
        return


ExtNamespaces = {EXSL_COMMON_NS: 'exsl'}
ExtFunctions = {(EXSL_COMMON_NS, 'node-set'): NodeSet, (EXSL_COMMON_NS, 'object-type'): ObjectType}
ExtElements = {(EXSL_COMMON_NS, 'document'): DocumentElement}