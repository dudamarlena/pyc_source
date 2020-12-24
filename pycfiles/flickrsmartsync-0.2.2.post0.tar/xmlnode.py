# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faisal/Developer/Projects/github/flickrsmartsync/flickrapi/xmlnode.py
# Compiled at: 2014-06-18 08:36:36
"""FlickrAPI uses its own in-memory XML representation, to be able to easily
use the info returned from Flickr.

There is no need to use this module directly, you'll get XMLNode instances
from the FlickrAPI method calls.
"""
import xml.dom.minidom
__all__ = ('XMLNode', )

class XMLNode:
    """XMLNode -- generic class for holding an XML node

    >>> xml_str = '''<xml foo="32">
    ... <taggy bar="10">Name0</taggy>
    ... <taggy bar="11" baz="12">Name1</taggy>
    ... </xml>'''
    >>> f = XMLNode.parse(xml_str)
    >>> f.name
    u'xml'
    >>> f['foo']
    u'32'
    >>> f.taggy[0].name
    u'taggy'
    >>> f.taggy[0]["bar"]
    u'10'
    >>> f.taggy[0].text
    u'Name0'
    >>> f.taggy[1].name
    u'taggy'
    >>> f.taggy[1]["bar"]
    u'11'
    >>> f.taggy[1]["baz"]
    u'12'

    """

    def __init__(self):
        """Construct an empty XML node."""
        self.name = ''
        self.text = ''
        self.attrib = {}
        self.xml = None
        return

    def __setitem__(self, key, item):
        """Store a node's attribute in the attrib hash."""
        self.attrib[key] = item

    def __getitem__(self, key):
        """Retrieve a node's attribute from the attrib hash."""
        return self.attrib[key]

    @classmethod
    def __parse_element(cls, element, this_node):
        """Recursive call to process this XMLNode."""
        this_node.name = element.nodeName
        for i in range(element.attributes.length):
            an = element.attributes.item(i)
            this_node[an.name] = an.nodeValue

        for a in element.childNodes:
            if a.nodeType == xml.dom.Node.ELEMENT_NODE:
                child = XMLNode()
                if not hasattr(this_node, a.nodeName) or a.nodeName == 'name':
                    setattr(this_node, a.nodeName, [])
                children = getattr(this_node, a.nodeName)
                children.append(child)
                cls.__parse_element(a, child)
            elif a.nodeType == xml.dom.Node.TEXT_NODE:
                this_node.text += a.nodeValue

        return this_node

    @classmethod
    def parse(cls, xml_str, store_xml=False):
        """Convert an XML string into a nice instance tree of XMLNodes.

        xml_str -- the XML to parse
        store_xml -- if True, stores the XML string in the root XMLNode.xml

        """
        dom = xml.dom.minidom.parseString(xml_str)
        root_node = XMLNode()
        if store_xml:
            root_node.xml = xml_str
        return cls.__parse_element(dom.firstChild, root_node)