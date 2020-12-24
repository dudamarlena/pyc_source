# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pydataportability/microformats/base/interfaces.py
# Compiled at: 2008-04-19 15:06:13
from zope.interface import Interface, Attribute

class IMicroformatsParser(Interface):
    __module__ = __name__
    name = Attribute("name of microformat it handles, e.g. 'hcard' or 'rel-tag' ")

    def parseNode():
        """parse a subtree and check it for microformats
        
        it should be called if checkNode() returns True
        
        returns a Microformat object
        
        """
        pass

    def checkNode():
        """check a node if we have a microformat to handle here
        
        returns True or False
        """
        pass


class IHTMLParser(Interface):
    """models a HTML parser"""
    __module__ = __name__

    def fromString(string):
        """returns a node from a string of HTML
        
        should return an IHTMLNode for the root element
        """
        pass

    def fromURL(url):
        """reads an HTML document from an URL
        
        should return an IHTMLNode for the root element
        """
        pass


class IHTMLNode(Interface):
    """models an HTML node"""
    __module__ = __name__
    name = Attribute('name of the tag in lower case')
    attribs = Attribute('list of (name,value) tuples of attributes for that tag')
    contents = Attribute('contents of the tag == subelements')
    text = Attribute('the text contents of a tag')

    def getiterator():
        """return an iterator over all tags"""
        pass


class IMicroformatData(Interface):
    """generic data container for microformats, supports nested data"""
    __module__ = __name__