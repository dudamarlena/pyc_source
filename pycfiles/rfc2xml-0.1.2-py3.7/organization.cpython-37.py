# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/organization.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 195 bytes
from . import Element

class Organization(Element):
    tag_name = 'organization'
    tag_name: str

    def __init__(self, value=None):
        super().__init__()
        self.children.append(value)