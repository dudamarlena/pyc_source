# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/table.py
# Compiled at: 2018-12-02 17:44:03
# Size of source mod 2**32: 1094 bytes
"""
table related directives.
"""
import attr
from .base import Directive

@attr.s
class ListTable(Directive):
    __doc__ = '\n    Example::\n\n        .. list-table:: Title of the table\n            :widths: 10 10 10\n            :header-rows: 1\n\n            * - Header1\n              - Header2\n              - Header3\n            * - Value1\n              - Value2\n              - Value3\n    '
    data = attr.ib(default=None)
    title = attr.ib(default='')
    index = attr.ib(default=False)
    header = attr.ib(default=True)
    align = attr.ib(default=None)
    meta_directive_keyword = 'list-table'
    meta_not_none_fields = ('data', )

    class AlignOptions(object):
        left = 'left'
        center = 'center'
        right = 'right'

    @align.validator
    def check_align(self, attribute, value):
        if value not in (None, 'left', 'center', 'right'):
            raise ValueError("ListTable.align has to be one of 'left', 'center', 'right'!")

    @property
    def arg(self):
        return self.title