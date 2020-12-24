# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/middle.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 280 bytes
from typing import List
from .section import Section

class Middle(Section):
    tag_name = 'middle'
    tag_name: str
    children = []
    children: List['Section']

    def __init__(self):
        super().__init__()

    def add_section(self, section: 'Section'):
        self.children.append(section)