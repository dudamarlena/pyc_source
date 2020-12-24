# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/title.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 445 bytes
from . import Element
from typing import Dict

class Title(Element):
    tag_name = 'title'
    tag_name: str
    abbrev = None
    abbrev: str

    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self.children.append(value)

    def get_attributes(self) -> Dict[(str, str)]:
        attributes = {}
        if self.abbrev is not None:
            attributes['abbrev'] = self.abbrev
        return attributes