# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/element.py
# Compiled at: 2007-07-16 07:02:51
"""A partial implementation of ElementTree and some extensions."""
__revision__ = '$Rev: 492 $'
__date__ = '$Date: 2007-07-06 21:38:45 -0400 (Fri, 06 Jul 2007) $'
__author__ = 'Ryan Tomayko (rtomayko@gmail.com)'
__copyright__ = 'Copyright 2004-2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
import re
__all__ = [
 'Element', 'SubElement', 'Comment', 'ProcessingInstruction', 'Fragment', 'QName', 'namespaces', 'escape_map', 'encode_entity', 'raise_serialization_error']

class Element(object):
    """A class representing an XML element."""
    __module__ = __name__
    text = None
    tail = None

    def __init__(self, tag, attrib={}, **extra):
        attrib = attrib.copy()
        attrib.update(extra)
        self.tag = tag
        self.attrib = attrib
        self._children = []

    def __repr__(self):
        return '<Element %s at %x>' % (self.tag, id(self))

    def __len__(self):
        return len(self._children)

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, element):
        assert isinstance(element, Element)
        self._children[index] = element

    def __delitem__(self, index):
        del self._children[index]

    def __getslice__(self, start, stop):
        return self._children[start:stop]

    def __setslice__(self, start, stop, elements):
        for element in elements:
            assert isinstance(element, Element)

        self._children[start:stop] = list(elements)

    def __delslice__(self, start, stop):
        del self._children[start:stop]

    def append(self, element):
        assert isinstance(element, Element)
        self._children.append(element)

    def insert(self, index, element):
        assert isinstance(element, Element)
        self._children.insert(index, element)

    def remove(self, element):
        assert isinstance(element, Element)
        self._children.remove(element)

    def getchildren(self):
        return self._children

    def clear(self):
        self.attrib.clear()
        self._children = []
        self.text = self.tail = None
        return

    def get(self, key, value=None):
        return self.attrib.get(key, value)

    def set(self, key, value):
        self.attrib[key] = value

    def keys(self):
        return self.attrib.keys()

    def items(self):
        return self.attrib.items()


def SubElement(parent, tag, attrib={}, **extra):
    attrib = attrib.copy()
    attrib.update(extra)
    element = Element(tag, attrib)
    parent.append(element)
    return element


def Comment(text=None):
    """Comment element factory."""
    elem = Element(Comment)
    elem.text = text
    return elem


def ProcessingInstruction(target, text=None):
    """PI element factory."""
    elem = Element(ProcessingInstruction)
    elem.text = target
    if text:
        elem.text += ' ' + text
    return elem


def Fragment(text=''):
    """XML fragment factory.

    Fragments hold TEXT and children but do not have a tag or attributes.
    """
    elem = Element(Fragment)
    elem.text = text
    return elem


class QName:
    __module__ = __name__

    def __init__(self, text_or_uri, tag=None):
        if tag:
            text_or_uri = '{%s}%s' % (text_or_uri, tag)
        self.text = text_or_uri

    def __str__(self):
        return self.text


def namespaces(elem, remove=False):
    """Get the namespace declarations for an Element.

    This function looks for attributes on the Element provided that have the
    following characteristics:

       * Begin with 'xmlns:' and have no namespace URI.
       * Are named 'xmlns' and have no namespace URI.

    The result is a dictionary containing namespace prefix -> URI mappings.
    Default namespace attributes result in a key of ''.

    If remove is truthful, namespace declaration attributes are removed
    from the passed in Element.

    """
    names = {}
    for k in elem.keys():
        if k.startswith('xmlns:'):
            names[k[6:]] = elem.get(k)
            if remove:
                del elem.attrib[k]
        elif k == 'xmlns':
            names[''] = elem.get(k)
            if remove:
                del elem.attrib[k]

    return names


escape_map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}
re_escape = re.compile(eval('u"[&<>\\"\\u0080-\\uffff]+"'))

def encode_entity(text, pattern=re_escape, entities=None):
    if entities is None:
        entities = escape_map

    def escape_entities(m, entities=entities):
        out = []
        for char in m.group():
            text = entities.get(char)
            if text is None:
                text = '&#%d;' % ord(char)
            out.append(text)

        return ('').join(out)
        return

    try:
        return pattern.sub(escape_entities, text).encode('ascii')
    except TypeError:
        raise_serialization_error(text)

    return


def raise_serialization_error(text):
    raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))