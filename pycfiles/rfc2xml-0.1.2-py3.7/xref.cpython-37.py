# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/xref.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 360 bytes
from . import Element

class Xref(Element):
    tag_name = 'xref'
    tag_name: str
    target = None
    target: str

    def __init__(self, target=None):
        super().__init__()
        self.target = target

    def get_attributes(self):
        attributes = {}
        if self.target is not None:
            attributes['target'] = self.target
        return attributes