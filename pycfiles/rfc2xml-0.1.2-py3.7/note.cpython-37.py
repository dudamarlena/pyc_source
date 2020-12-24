# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/note.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 501 bytes
from . import Element
from typing import List, Union

class Note(Element):
    tag_name = 'note'
    tag_name: str
    title = None
    title: str

    def get_attributes(self):
        attributes = {}
        if self.title is not None:
            attributes['title'] = self.title
        return attributes

    def __init__(self, title=None, children=None):
        super().__init__()
        self.title = title
        if children is not None:
            self.children = children