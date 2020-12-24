# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/section.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 817 bytes
from .element import Element
from typing import List

class Section(Element):
    tag_name = 'section'
    tag_name: str
    title = None
    title: str
    number = None
    number: str

    def __init__(self, title=None, number=None):
        super().__init__()
        self.title = title
        self.number = number

    def get_sections(self) -> List['Section']:
        o = []
        for child in self.children:
            if isinstance(child, Section):
                o.append(child)

        return o

    def get_attributes(self):
        attributes = {}
        if self.title is not None:
            attributes['title'] = self.title
        if self.number is not None:
            attributes['number'] = self.number
        return attributes

    def __str__(self):
        return str(self.number) + '. ' + str(self.title)