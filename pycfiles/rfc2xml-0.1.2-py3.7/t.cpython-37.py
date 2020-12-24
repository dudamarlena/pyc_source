# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/t.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 621 bytes
from . import Element
from typing import List, Union, Dict

class T(Element):
    tag_name = 't'
    tag_name: str
    hang_text = None
    hang_text: str

    def __init__(self, children=None, hang_text=None):
        super().__init__()
        if children is None:
            children = []
        self.children = children
        self.hang_text = hang_text

    def get_attributes(self) -> Dict[(str, str)]:
        attributes = {}
        if self.hang_text is not None:
            attributes['hangText'] = self.hang_text
        return attributes

    def __str__(self):
        return str(self.children)