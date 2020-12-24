# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/toc_item.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 668 bytes
from . import Element

class TocItem(Element):
    tag_name = 'toc_item'
    tag_name: str
    section = None
    section: str
    title = None
    title: str
    page = None
    page: int

    def __init__(self, section=None, title=None, page=None):
        super().__init__()
        self.section = section
        self.title = title
        self.page = page

    def get_attributes(self):
        attributes = {}
        if self.section is not None:
            attributes['section'] = self.section
        if self.title is not None:
            attributes['title'] = self.title
        if self.page is not None:
            attributes['page'] = str(self.page)
        return attributes