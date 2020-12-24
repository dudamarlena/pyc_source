# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/shared/xml_parser.py
# Compiled at: 2008-02-21 11:38:58
import xml.sax
from xml.sax.handler import ContentHandler

class XmlElement:
    """Representgs an XML tag."""
    __module__ = __name__

    def __init__(self, elem, attrs=None, nsUri=None):
        """An XmlElement instance may represent:
           - an already parsed tag (in this case, p_elem may be prefixed with a
             namespace);
           - the definition of an XML element (in this case, no namespace can be
             found in p_elem; but a namespace URI may be defined in p_nsUri)."""
        self.elem = elem
        self.attrs = attrs
        if elem.find(':') != -1:
            (self.ns, self.name) = elem.split(':')
        else:
            self.ns = ''
            self.name = elem
            self.nsUri = nsUri

    def equalsTo(self, other, namespaces=None):
        """Does p_elem == p_other? If a p_namespaces dict is given, p_other must
           define a nsUri."""
        res = None
        if namespaces:
            res = self.elem == '%s:%s' % (namespaces[other.nsUri], other.name)
        else:
            res = self.elem == other.elem
        return res

    def __repr__(self):
        return self.elem

    def getFullName(self, namespaces=None):
        """Gets the name of the element including the namespace prefix."""
        if not namespaces:
            res = self.elem
        else:
            res = '%s:%s' % (namespaces[self.nsUri], self.name)
        return res


class XmlEnvironment:
    """An XML environment remembers a series of elements during a SAX parsing.
       This class is an abstract class that gathers basic things like
       namespaces."""
    __module__ = __name__

    def __init__(self):
        self.namespaces = {}
        self.currentElem = None
        self.parser = None
        return

    def manageNamespaces(self, attrs):
        """Manages namespaces definitions encountered in p_attrs."""
        for (attrName, attrValue) in attrs.items():
            if attrName.startswith('xmlns:'):
                self.namespaces[attrValue] = attrName[6:]

    def ns(self, nsUri):
        """Returns the namespace corresponding to o_nsUri."""
        return self.namespaces[nsUri]


class XmlParser(ContentHandler):
    """Basic XML content handler that does things like :
      - remembering the currently parsed element;
      - managing namespace declarations."""
    __module__ = __name__

    def __init__(self, env, caller=None):
        """p_env should be an instance of a class that inherits from
           XmlEnvironment: it specifies the environment to use for this SAX
           parser."""
        ContentHandler.__init__(self)
        self.env = env
        self.env.parser = self
        self.caller = caller

    def setDocumentLocator(self, locator):
        self.locator = locator
        return self.env

    def endDocument(self):
        return self.env

    def startElement(self, elem, attrs):
        self.env.manageNamespaces(attrs)
        if self.env.currentElem == None:
            self.env.currentElem = XmlElement(elem, attrs)
        else:
            self.env.currentElem.__init__(elem, attrs)
        return self.env

    def endElement(self, elem):
        self.env.currentElem.__init__(elem)
        return self.env

    def characters(self, content):
        return self.env

    def parse(self, xmlContent, source='string'):
        """Parsers the XML file or string p_xmlContent."""
        if source == 'string':
            xml.sax.parseString(xmlContent, self)
        else:
            raise 'Not implemented yet! Please specify source=string for the moment.'