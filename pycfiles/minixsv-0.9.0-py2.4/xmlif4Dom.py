# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\genxmlif\xmlif4Dom.py
# Compiled at: 2008-08-08 10:47:58
import urllib
from xml.dom.ext.reader.Sax2 import Reader, XmlDomGenerator
from xml.sax._exceptions import SAXParseException
from genxmlif import XMLIF_4DOM, GenXmlIfError
from xmlifUtils import convertToAbsUrl
from xmlifDom import XmlInterfaceDom, XmlIfBuilderExtensionDom, InternalDomTreeWrapper, InternalDomElementWrapper

class XmlInterface4Dom(XmlInterfaceDom):
    __module__ = __name__

    def __init__(self, verbose, useCaching, processXInclude):
        XmlInterfaceDom.__init__(self, verbose, useCaching, processXInclude)
        self.xmlIfType = XMLIF_4DOM
        if self.verbose:
            print 'Using 4Dom interface module...'

    def parse(self, file, baseUrl='', internalOwnerDoc=None):
        absUrl = convertToAbsUrl(file, baseUrl)
        fp = urllib.urlopen(absUrl)
        return self._parseStream(fp, file, absUrl, internalOwnerDoc)

    def parseString(self, text, baseUrl='', internalOwnerDoc=None):
        import cStringIO
        fp = cStringIO.StringIO(text)
        absUrl = convertToAbsUrl('', baseUrl)
        return self._parseStream(fp, '', absUrl, internalOwnerDoc)

    def _parseStream(self, fp, file, absUrl, internalOwnerDoc):
        reader = Reader(validate=0, keepAllWs=0, catName=None, saxHandlerClass=ExtXmlDomGenerator, parser=None)
        reader.handler.extinit(file, absUrl, reader.parser, self)
        if internalOwnerDoc != None:
            ownerDoc = internalOwnerDoc.document
        else:
            ownerDoc = None
        try:
            tree = reader.fromStream(fp, ownerDoc)
            fp.close()
        except SAXParseException, errInst:
            fp.close()
            raise GenXmlIfError, '%s: SAXParseException: %s' % (file, str(errInst))

        treeWrapper = reader.handler.treeWrapper
        if self.processXInclude:
            if internalOwnerDoc == None:
                internalOwnerDoc = treeWrapper.getTree()
            self.xInclude(treeWrapper.getRootNode(), absUrl, internalOwnerDoc)
        return treeWrapper


class ExtXmlDomGenerator(XmlDomGenerator, XmlIfBuilderExtensionDom):
    __module__ = __name__

    def __init__(self, keepAllWs=0):
        XmlDomGenerator.__init__(self, keepAllWs)
        self.treeWrapper = None
        return

    def extinit(self, filePath, absUrl, parser, xmlIf):
        self.filePath = filePath
        self.absUrl = absUrl
        self.parser = parser
        self.xmlIf = xmlIf

    def startElement(self, name, attribs):
        XmlDomGenerator.startElement(self, name, attribs)
        if not self.treeWrapper:
            self.treeWrapper = self.xmlIf.treeWrapperClass(self, InternalDomTreeWrapper(self._rootNode), self.xmlIf.useCaching)
            XmlIfBuilderExtensionDom.__init__(self, self.filePath, self.absUrl, self.treeWrapper, self.xmlIf.elementWrapperClass)
        curNode = self._nodeStack[(-1)]
        internal4DomElementWrapper = InternalDomElementWrapper(curNode, self.treeWrapper.getTree())
        curNs = self._namespaces.items()
        try:
            curNs.remove((None, None))
        except:
            pass

        XmlIfBuilderExtensionDom.startElementHandler(self, internal4DomElementWrapper, self.parser.getLineNumber(), curNs)
        return

    def endElement(self, name):
        curNode = self._nodeStack[(-1)]
        XmlIfBuilderExtensionDom.endElementHandler(self, curNode.xmlIfExtInternalWrapper, self.parser.getLineNumber())
        XmlDomGenerator.endElement(self, name)