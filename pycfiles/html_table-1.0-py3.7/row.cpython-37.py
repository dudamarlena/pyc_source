# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/HTMLTable/row.py
# Compiled at: 2019-04-08 22:07:56
# Size of source mod 2**32: 968 bytes
"""
FileName:   row.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

"""
from .cell import HTMLTableCell
from .common import HTMLTag

class HTMLTableRow(list, HTMLTag):

    def __init__(self, cells=(), is_header=False):
        list.__init__(self)
        HTMLTag.__init__(self, tag='tr')
        self.is_header = is_header
        self.append_cells(cells=cells)

    def append_cells(self, cells):
        cell_tag = 'th' if self.is_header else 'td'
        for cell in cells:
            self.append(HTMLTableCell(tag=cell_tag,
              value=cell))

    def set_cell_style(self, style):
        for cell in self:
            cell.set_style(style=style)

    def to_html_inner_chips(self):
        chips = []
        for cell in self:
            chips.extend(cell.to_html_chips())

        return chips