# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/cli/formatter.py
# Compiled at: 2017-10-18 16:20:05
# Size of source mod 2**32: 3910 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import time, math
from wasp_general.verify import verify_type
from wasp_general.datetime import local_datetime

def local_datetime_formatter(dt):
    return '%s%s' % (local_datetime(dt=dt).isoformat(), time.strftime('%Z'))


@verify_type(none_value=(str, None))
def na_formatter(value, str_fn=None, none_value=None):
    fn = str_fn if str_fn is not None else str
    if value is not None:
        return fn(value)
    if none_value is not None:
        return none_value
    return '(not available)'


@verify_type(size=int)
def data_size_formatter(size):
    suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    suffix_index = int(math.floor(math.log2(size) / 10))
    if suffix_index >= len(suffixes):
        suffix_index = len(suffixes) - 1
    return '{:.2f} {}'.format(size / (1 << suffix_index * 10), suffixes[suffix_index])


class WConsoleTableFormatter:
    __default_delimiter__ = '*'

    @verify_type(table_headers=str)
    def __init__(self, *table_headers):
        self._WConsoleTableFormatter__headers = table_headers
        self._WConsoleTableFormatter__rows = []
        self._WConsoleTableFormatter__cells_length = WConsoleTableFormatter.cells_length(*table_headers)

    @staticmethod
    def cells_length(*cells):
        return tuple([len(x) for x in cells])

    def add_row(self, *cells):
        self._WConsoleTableFormatter__rows.append(cells)
        row_length = WConsoleTableFormatter.cells_length(*cells)
        min_cells, max_cells = row_length, self._WConsoleTableFormatter__cells_length
        if len(cells) > len(max_cells):
            min_cells, max_cells = max_cells, min_cells
        result = [max(min_cells[i], max_cells[i]) for i in range(len(min_cells))]
        result.extend([max_cells[i] for i in range(len(min_cells), len(max_cells))])
        self._WConsoleTableFormatter__cells_length = tuple(result)

    def format(self, delimiter=None):
        if delimiter is None:
            delimiter = self.__default_delimiter__
        cell_count = len(self._WConsoleTableFormatter__cells_length)
        if cell_count == 0:
            raise RuntimeError('Empty table')
        separator_length = (cell_count - 1) * 3 + 4
        for cell_length_iter in self._WConsoleTableFormatter__cells_length:
            separator_length += cell_length_iter

        separator = delimiter * separator_length + '\n'
        left_border = '%s ' % delimiter
        int_border = ' %s ' % delimiter
        right_border = ' %s\n' % delimiter

        def render_row(*cells):
            row_result = ''
            for i in range(cell_count):
                cell_length = self._WConsoleTableFormatter__cells_length[i]
                if i < len(cells):
                    single_cell = cells[i]
                    row_result += single_cell
                    delta = cell_length - len(single_cell)
                else:
                    delta = cell_length
                row_result += ' ' * delta
                if i < cell_count - 1:
                    row_result += int_border
                    continue

            return row_result

        result = separator
        result += left_border
        result += render_row(*self._WConsoleTableFormatter__headers)
        result += right_border
        result += separator
        for row in self._WConsoleTableFormatter__rows:
            result += left_border
            result += render_row(*row)
            result += right_border

        result += separator
        return result