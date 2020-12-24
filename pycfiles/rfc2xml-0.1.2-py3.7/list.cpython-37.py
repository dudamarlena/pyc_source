# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/list.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 620 bytes
from . import Element
from typing import List as TypingList, Union, Dict

class List(Element):
    tag_name = 'list'
    tag_name: str
    style = None
    style: str

    def __init__(self, children=None, style=None):
        super().__init__()
        if children is None:
            children = []
        self.children = children
        self.style = style

    def __str__(self):
        return str(self.children)

    def get_attributes(self) -> Dict[(str, str)]:
        attributes = {}
        if self.style is not None:
            attributes['style'] = self.style
        return attributes