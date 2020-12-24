# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pydataportability/microformats/base/htmlparsers/beautifulsoup.py
# Compiled at: 2008-04-19 15:06:13
from zope.component import adapts
from zope.interface import implements
from pydataportability.microformats.base.interfaces import IHTMLNode, IHTMLParser
from pydataportability.microformats.base.parser import MicroformatsParser
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag, NavigableString

class BeautifulSoupHTMLParser(object):
    """an HTML Parser based on BeautifulSoup"""
    __module__ = __name__
    implements(IHTMLParser)

    def __init__(self):
        """initialize this parser"""
        self.initialized = False
        self.soup = None
        return

    def fromString(self, string, **kwargs):
        """returns a node from a string of HTML
        
        should return an IHTMLNode for the root element
        """
        self.soup = BeautifulSoup(string)
        self.initialized = True
        return MicroformatsParser(self.soup, **kwargs)

    def fromFile(self, filename, **kwargs):
        """open a file and parse the document"""
        fp = open(filename, 'r')
        self.soup = BeautifulSoup(fp)
        fp.close()
        self.initialized = True
        return MicroformatsParser(self.soup, **kwargs)

    def fromURL(self, url, **kwargs):
        """reads an HTML document from an URL
        
        should return an IHTMLNode for the root element
        """
        page = urllib2.urlopen(url)
        self.soup = BeautifulSoup(page)
        self.initialized = True
        return MicroformatsParser(self.soup, **kwargs)


class BeautifulSoupHTMLNode(object):
    """an adapter form an BeautifulSoupHTMLNode node to an IHTMLNode"""
    __module__ = __name__
    implements(IHTMLNode)
    adapts(Tag)

    def __init__(self, context):
        self.context = context

    @property
    def tag(self):
        """return the tag name"""
        return self.context.name

    @property
    def attrib(self):
        """return the attributes of that tag in tuple format (name,value)"""
        d = {}
        for (a, v) in self.context.attrs:
            d[a] = v

        return d

    def getiterator(self):
        """return the subelements"""
        return self.context.findAll()

    @property
    def text(self):
        """return the textual representation"""
        return self.context.text