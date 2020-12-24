# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/artwork.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 777 bytes
from . import Element
from lxml import etree

class Artwork(Element):
    tag_name = 'artwork'
    tag_name: str
    text = None
    text: str

    def __init__(self, text=None):
        super().__init__()
        text = text.rstrip()
        lines = text.split('\n')
        ws = len(lines[0]) - len(lines[0].lstrip(' '))
        for l in lines[1:]:
            v = len(l) - len(l.lstrip(' '))
            if v < ws:
                ws = v

        self.text = ''
        for l in lines:
            self.text += l[ws:] + '\n'

    def to_xml(self):
        element = etree.Element(str(self.tag_name), self.get_attributes())
        if self.text is not None:
            element.text = etree.CDATA('\n' + self.text)
        return element

    def __str__(self):
        return self.text