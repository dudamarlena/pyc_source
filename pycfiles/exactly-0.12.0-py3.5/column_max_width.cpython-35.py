# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/rendering/text/table/column_max_width.py
# Compiled at: 2017-12-07 08:04:08
# Size of source mod 2**32: 1005 bytes
import types

def derive_column_max_widths(cell_formatter_for_given_width: types.FunctionType, available_width: int, columns_with_cell_content: list) -> list:
    """
    :type columns_with_cell_content:[[cell]]
    :return: [int]
    """
    cell_formatter = cell_formatter_for_given_width(available_width + _ADDITIONAL_WIDTH_TO_MAKE_WIDTH_LESS_LIKELY_TO_DEPEND_ON_WORD_WRAP)
    columns_with_cell_lines_str = [[cell_formatter(cell) for cell in col] for col in columns_with_cell_content]
    columns_with_cell_lines_width = []
    for col in columns_with_cell_lines_str:
        col_lines = []
        for cell in col:
            for line in cell:
                col_lines.append(len(line))

        columns_with_cell_lines_width.append(col_lines)

    return [max(line_widths, default=0) for line_widths in columns_with_cell_lines_width]


_ADDITIONAL_WIDTH_TO_MAKE_WIDTH_LESS_LIKELY_TO_DEPEND_ON_WORD_WRAP = 100