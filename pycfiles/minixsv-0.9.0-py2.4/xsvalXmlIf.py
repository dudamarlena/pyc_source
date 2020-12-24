# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\minixsv\xsvalXmlIf.py
# Compiled at: 2008-08-08 10:44:20
from types import TupleType
from genxmlif.xmlifApi import XmlElementWrapper

class XsvXmlElementWrapper(XmlElementWrapper):
    __module__ = __name__

    def __init__(self, element, treeWrapper, curNs=[], initAttrSeq=1):
        XmlElementWrapper.__init__(self, element, treeWrapper, curNs, initAttrSeq)
        self.schemaRootNode = None
        self.xsdNode = None
        self.xsdAttrNodes = {}
        return

    def cloneNode(self, deep, cloneCallback=None):
        return XmlElementWrapper.cloneNode(self, deep, self.cloneCallback)

    def cloneCallback(self, nodeCopy):
        nodeCopy.schemaRootNode = self.schemaRootNode
        nodeCopy.xsdNode = self.xsdNode
        nodeCopy.xsdAttrNodes = self.xsdAttrNodes.copy()

    def getSchemaRootNode(self):
        """Retrieve XML schema root node which this element node belongs to
           (e.g. for accessing target namespace attribute).
        
        Returns XML schema root node which this element node belongs to
        """
        return self.schemaRootNode

    def setSchemaRootNode(self, schemaRootNode):
        """Store XML schema root node which this element node belongs to.
        
        Input parameter:
            schemaRootNode:    schema root node which this element node belongs to
        """
        self.schemaRootNode = schemaRootNode

    def getXsdNode(self):
        """Retrieve XML schema node responsible for this element node.
        
        Returns XML schema node responsible for this element node.
        """
        return self.xsdNode

    def setXsdNode(self, xsdNode):
        """Store XML schema node responsible for this element node.
        
        Input parameter:
            xsdNode:    responsible XML schema ElementWrapper
        """
        self.xsdNode = xsdNode

    def getXsdAttrNode(self, tupleOrAttrName):
        """Retrieve XML schema node responsible for the requested attribute.

        Input parameter:
            tupleOrAttrName:  tuple '(namespace, attributeName)' or 'attributeName' if no namespace is used
        Returns XML schema node responsible for the requested attribute.
        """
        try:
            return self.xsdAttrNodes[tupleOrAttrName]
        except:
            if isinstance(tupleOrAttrName, TupleType):
                if tupleOrAttrName[1] == '*' and len(self.xsdAttrNodes) == 1:
                    return self.xsdAttrNodes.values()[0]
            return

        return

    def setXsdAttrNode(self, tupleOrAttrName, xsdAttrNode):
        """Store XML schema node responsible for the given attribute.
        
        Input parameter:
            tupleOrAttrName:  tuple '(namespace, attributeName)' or 'attributeName' if no namespace is used
            xsdAttrNode:      responsible XML schema ElementWrapper
        """
        self.xsdAttrNodes[tupleOrAttrName] = xsdAttrNode