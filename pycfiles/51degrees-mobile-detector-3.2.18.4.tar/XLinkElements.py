# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XLink\XLinkElements.py
# Compiled at: 2005-09-14 16:38:44
__doc__ = '\nClasses representing XLink elements\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from xml.dom import Node
from Ft.Xml import Domlette
from Ft.Xml.XLink import XLINK_NAMESPACE

def Create(node, baseUri):
    """
    Given an XLink element node, returns an object (one of the classes
    defined in this module) that contains the node, its principal XLink
    attribute values, and a 'process' method that can be invoked in order
    to process (follow or otherwise act upon) the element.

    Used by the Ft.Xml.XLink.Processor.Processor.
    """
    elemType = node.getAttributeNS(XLINK_NAMESPACE, 'type')
    return TypeMap.get(elemType, Literal)(node, baseUri)


class Literal:
    """
    Base class for an XLink element.
    """
    __module__ = __name__
    type = None

    def __init__(self, node, iSrc):
        self.resource = node
        self.input_source = iSrc

    def process(self):
        return


class Simple(Literal):
    """
    A 'simple'-type XLink element.
    """
    __module__ = __name__
    type = 'simple'

    def __init__(self, node, iSrc):
        Literal.__init__(self, node, iSrc)
        self.href = node.getAttributeNS(XLINK_NAMESPACE, 'href')
        self.role = node.getAttributeNS(XLINK_NAMESPACE, 'role')
        self.arcrole = node.getAttributeNS(XLINK_NAMESPACE, 'arcrole')
        self.title = node.getAttributeNS(XLINK_NAMESPACE, 'title')
        self.show = node.getAttributeNS(XLINK_NAMESPACE, 'show')
        self.actuate = node.getAttributeNS(XLINK_NAMESPACE, 'actuate')
        self.attributes = filter(lambda x: x.namespaceURI != XLINK_NAMESPACE, node.attributes.values())

    def process(self):
        """
        Processes a simple XLink element according to the following
        guidelines:

        If xlink:actuate='onLoad' and xlink:show='replace', then the remote
        resource's document element's content (not the document element itself)
        and the content of the XLink element (if any) will together replace the
        XLink element.

        If xlink:actuate='onLoad' and xlink:show='embed', then the remote
        resource's document element will replace the XLink element.

        Any other XLink attribute combinations are ignored.

        These behaviors constitute a reasonable approximation of the resource
        loading suggestions in XLink 1.0 sec. 5.6.1.
        """
        resource = self.resource
        if self.actuate == 'onLoad':
            doc = resource.rootNode
            if self.show == 'replace':
                newSrc = self.input_source.resolve(self.href, hint='XLink')
                newDoc = Domlette.NonvalidatingReader.parse(newSrc)
                for node in self.attributes:
                    newDoc.documentElement.setAttributeNS(node.namespaceURI, node.nodeName, node.value)

                for child in resource.childNodes[:]:
                    nChild = doc.importNode(child, True)
                    newDoc.documentElement.appendChild(nChild)

                if resource.parentNode is not None:
                    parent = resource.parentNode
                else:
                    parent = doc
                for child in newDoc.documentElement.childNodes[:]:
                    newDoc.documentElement.removeChild(child)
                    child = doc.importNode(child, True)
                    parent.insertBefore(child, resource)

                parent.removeChild(resource)
            elif self.show == 'embed':
                newSrc = self.input_source.resolve(self.href, hint='XLink')
                newDoc = Domlette.NonvalidatingReader.parse(newSrc)
                child = doc.importNode(newDoc.documentElement, True)
                if resource.parentNode is not None:
                    resource.parentNode.replaceChild(child, resource)
                else:
                    doc.replaceChild(child, resource)
        return


class Extended(Literal):
    __module__ = __name__
    type = 'extended'


class Locator(Literal):
    __module__ = __name__
    type = 'locator'


class Arc(Literal):
    __module__ = __name__
    type = 'arc'


class Resource(Literal):
    __module__ = __name__
    type = 'resource'


class Title(Literal):
    __module__ = __name__
    type = 'title'


TypeMap = {'simple': Simple, 'extended': Extended, 'locator': Locator, 'arc': Arc, 'resource': Resource, 'title': Title}