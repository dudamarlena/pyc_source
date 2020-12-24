# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/structure/table.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1543 bytes
from typing import List
from exactly_lib.util.textformat.structure.core import ParagraphItem

class TableFormat:

    def __init__(self, column_separator: str='  ',
                 first_row_is_header: bool=False,
                 first_column_is_header: bool=False):
        self._column_separator = column_separator
        self._first_row_is_header = first_row_is_header
        self._first_column_is_header = first_column_is_header

    @property
    def column_separator(self) -> str:
        return self._column_separator

    @property
    def first_row_is_header(self) -> bool:
        return self._first_row_is_header

    @property
    def first_column_is_header(self) -> bool:
        return self._first_column_is_header


class TableCell(tuple):

    def __new__(cls, paragraph_items: List[ParagraphItem]):
        return tuple.__new__(cls, (paragraph_items,))

    @property
    def paragraph_items(self) -> List[ParagraphItem]:
        return self[0]


class Table(ParagraphItem):

    def __init__(self, format_: TableFormat, rows: List[List[TableCell]]):
        self._format = format_
        self._rows = list(rows)

    @property
    def format(self) -> TableFormat:
        return self._format

    @property
    def rows(self) -> List[List[TableCell]]:
        return self._rows


def single_paragraph_cell(paragraph_item: ParagraphItem) -> TableCell:
    return TableCell([paragraph_item])


def empty_cell() -> TableCell:
    return TableCell([])