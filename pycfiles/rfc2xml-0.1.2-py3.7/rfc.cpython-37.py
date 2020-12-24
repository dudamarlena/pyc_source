# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/rfc.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 1212 bytes
from typing import List
from lxml import etree
from . import *
from .front import Front
from .middle import Middle
from .back import Back
from .toc import Toc
from .toc_item import TocItem

class Rfc(Element):
    tag_name = 'rfc'
    tag_name: str
    compliant = False
    compliant: bool
    docname = None
    docname: str
    toc = None
    toc: 'Toc'
    front = Front()
    front: 'Front'
    middle = Middle()
    middle: 'Middle'
    back = Back()
    back: 'Back'

    def __init__(self, compliant=False):
        super().__init__()
        self.compliant = compliant

    def set_toc_children(self, children: List[TocItem]):
        if self.toc is None:
            self.toc = Toc()
        self.toc.children = children

    def get_attributes(self):
        attributes = {}
        if self.docname is not None:
            attributes['docName'] = self.docname
        return attributes

    def to_xml(self):
        element = etree.Element(str(self.tag_name), self.get_attributes())
        if not self.compliant:
            if self.toc is not None:
                element.append(self.toc.to_xml())
        element.append(self.front.to_xml())
        element.append(self.middle.to_xml())
        self.children_to_xml(element)
        return element