# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/proofreader/utils/print_table.py
# Compiled at: 2018-03-13 09:30:54
from collections import defaultdict

class PrintTable(object):
    COLUMN_MARK = '+'
    COLUMN_SEP = '|'
    DASH = '-'
    PADDING = 1

    def __init__(self, headers):
        self.headers = headers
        self._rows = []
        self._col_widths = []

    def add_row(self, row):
        self._rows.append(row)

    @property
    def col_widths(self):
        """Get MAX possible width of each column in the table.

        :return: defaultdict
        """
        _widths = defaultdict(int)
        all_rows = [
         self.headers]
        all_rows.extend(self._rows)
        for row in all_rows:
            for idx, col in enumerate(row):
                _col_l = len(col)
                if _col_l > _widths[idx]:
                    _widths[idx] = _col_l

        return _widths

    def _marker_line(self):
        """Generate a correctly sized marker line.

        e.g.

        '+------------------+---------+----------+---------+'

        :return: str
        """
        output = ''
        for col in sorted(self.col_widths):
            line = self.COLUMN_MARK + self.DASH * (self.col_widths[col] + self.PADDING * 2)
            output += line

        output += self.COLUMN_MARK + '\n'
        return output

    @property
    def pad(self):
        return ' ' * self.PADDING

    def _row_to_str(self, row):
        """Converts a list of strings to a correctly spaced and formatted
        row string.

        e.g.

        ['some', 'foo', 'bar'] --> '| some | foo |  bar  |'

        :param row: list
        :return: str
        """
        _row_text = ''
        for col, width in self.col_widths.items():
            _row_text += self.COLUMN_SEP
            l_pad, r_pad = self._split_int(width - len(row[col]))
            _row_text += ('{0}{1}{2}').format(' ' * (l_pad + self.PADDING), row[col], ' ' * (r_pad + self.PADDING))

        _row_text += self.COLUMN_SEP + '\n'
        return _row_text

    @staticmethod
    def _split_int(num):
        split = num // 2
        return (split + num % 2, split)

    def _table_to_str(self):
        """Return single formatted table string.

        :return: str
        """
        _marker_line = self._marker_line()
        output = _marker_line + self._row_to_str(self.headers) + _marker_line
        for row in self._rows:
            output += self._row_to_str(row)

        output += _marker_line
        return output

    def __str__(self):
        return self._table_to_str()