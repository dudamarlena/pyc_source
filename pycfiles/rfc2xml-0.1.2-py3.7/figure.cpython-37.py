# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/figure.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 693 bytes
from . import Element
from typing import Union

class Figure(Element):
    tag_name = 'figure'
    tag_name: str
    title = None
    title: str

    def __init__(self, title=None, child=None):
        super().__init__()
        self.title = title
        if child is not None:
            self.add_child(child)

    def get_attributes(self):
        attributes = {}
        if self.title is not None:
            attributes['title'] = self.title
        return attributes

    def __str__(self):
        o = ''
        for child in self.children:
            o += child.__str__()

        if self.title is not None:
            o += '\n\nFigure: ' + str(self.title)
        return o