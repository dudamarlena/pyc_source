# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dominic/__init__.py
# Compiled at: 2010-06-09 02:10:27
version = '0.1.3-unreleased'
import xpath
from xml.dom import minidom
from dominic.css import XPathTranslator

class BaseHandler(object):

    def xpath(self, path):
        finder = xpath.XPath(path)
        return ElementSet(finder.find(self.element))

    def find(self, selector):
        xpather = XPathTranslator(selector)
        return self.xpath(xpather.path)

    def get(self, selector):
        return self.find(selector)[0]

    def _get_element_text(self):
        ret = self.element.childNodes[0].wholeText
        return ret.encode('utf-8')

    def text(self, new=None):
        if isinstance(new, basestring):
            self.element.childNodes[0].replaceWholeText(new)
        return self._get_element_text()

    def html(self, new=None):
        if isinstance(new, basestring):
            while self.element.childNodes:
                self.element.childNodes.pop()

            html = minidom.parseString(new)
            node = html.childNodes[0]
            self.element.parentNode.replaceChild(node, self.element)
            self.element = node
        return self.element.toxml()

    def _fetch_attributes(self, element):
        keys = element.attributes.keys()
        return dict([ (k, element.getAttribute(k)) for k in keys ])


class ElementSet(list):

    def __init__(self, items):
        super(ElementSet, self).__init__(map(Element, items))

    def first(self):
        return self[0]

    def last(self):
        return self[(-1)]

    @property
    def length(self):
        return len(self)


class Element(BaseHandler):

    def __init__(self, element):
        self.element = element
        self.attribute = self._fetch_attributes(element)
        self.tag = element.tagName


class DOM(BaseHandler):

    def __init__(self, raw):
        self.raw = raw
        self.document = minidom.parseString(raw)
        self.element = self.document.childNodes[0]