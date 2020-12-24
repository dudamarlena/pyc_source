# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\genxmlif\xmlifBase.py
# Compiled at: 2008-08-08 10:48:06
__author__ = 'Roland Leuthe <roland@leuthe-net.de>'
__date__ = '28 July 2008'
__version__ = '0.9'
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE
from xmlifUtils import NsNameTupleFactory, convertToAbsUrl

class XmlIfBuilderExtensionBase:
    """XmlIf builder extension base class.
    
    This class provides additional data (e.g. line numbers or caches) 
    for an element node which are stored in the element node object during parsing.
    """
    __module__ = __name__

    def __init__(self, filePath, absUrl, treeWrapper, elementWrapperClass):
        """Constructor for this class
        
        Input parameter:
            filePath:      contains the file path of the corresponding XML file
            absUrl:        contains the absolute URL of the corresponding XML file
        """
        self.filePath = filePath
        self.absUrl = absUrl
        self.baseUrlStack = [absUrl]
        self.treeWrapper = treeWrapper
        self.elementWrapperClass = elementWrapperClass

    def startElementHandler(self, curNode, startLineNumber, curNs, attributes=[]):
        """Called by the XML parser at creation of an element node.
        
        Input parameter:
            curNode:          current element node
            startLineNumber:  first line number of the element tag in XML file
            curNs:            namespaces visible for this element node
            attributes:       list of attributes and their values for this element node 
                              (same sequence as int he XML file)
        """
        elementWrapper = self.elementWrapperClass(curNode, self.treeWrapper, curNs, initAttrSeq=0)
        elementWrapper.baseUrl = self.__getBaseUrl(elementWrapper)
        elementWrapper.absUrl = self.absUrl
        elementWrapper.filePath = self.filePath
        elementWrapper.startLineNumber = startLineNumber
        elementWrapper.curNs.extend([('xml', XML_NAMESPACE), ('xmlns', XMLNS_NAMESPACE)])
        if attributes != []:
            for i in range(0, len(attributes), 2):
                elementWrapper.attributeSequence.append(attributes[i])

        else:
            attrList = elementWrapper.getAttributeDict().keys()
            attrList.sort()
            elementWrapper.attributeSequence.extend(attrList)
        self.baseUrlStack.insert(0, elementWrapper.baseUrl)

    def endElementHandler(self, curNode, endLineNumber):
        """Called by the XML parser after creation of an element node.
        
        Input parameter:
            curNode:          current element node
            endLineNumber:    last line number of the element tag in XML file
        """
        curNode.xmlIfExtElementWrapper.endLineNumber = endLineNumber
        self.baseUrlStack.pop(0)

    def __getBaseUrl(self, elementWrapper):
        """Retrieve base URL for the given element node.
        
        Input parameter:
            elementWrapper:    wrapper of current element node
        """
        nsNameBaseAttr = NsNameTupleFactory((XML_NAMESPACE, 'base'))
        if elementWrapper.hasAttribute(nsNameBaseAttr):
            return convertToAbsUrl(elementWrapper.getAttribute(nsNameBaseAttr), self.baseUrlStack[0])
        else:
            return self.baseUrlStack[0]