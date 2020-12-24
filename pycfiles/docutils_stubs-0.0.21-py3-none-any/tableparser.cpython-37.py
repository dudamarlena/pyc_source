# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/parsers/rst/tableparser.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 21041 bytes
"""
This module defines table parser classes,which parse plaintext-graphic tables
and produce a well-formed data structure suitable for building a CALS table.

:Classes:
    - `GridTableParser`: Parse fully-formed tables represented with a grid.
    - `SimpleTableParser`: Parse simple tables, delimited by top & bottom
      borders.

:Exception class: `TableMarkupError`

:Function:
    `update_dict_of_lists()`: Merge two dictionaries containing list values.
"""
__docformat__ = 'reStructuredText'
import re, sys
from docutils import DataError
from docutils.utils import strip_combining_chars

class TableMarkupError(DataError):
    __doc__ = "\n    Raise if there is any problem with table markup.\n\n    The keyword argument `offset` denotes the offset of the problem\n    from the table's start line.\n    "

    def __init__(self, *args, **kwargs):
        self.offset = kwargs.pop('offset', 0)
        (DataError.__init__)(self, *args)


class TableParser:
    __doc__ = '\n    Abstract superclass for the common parts of the syntax-specific parsers.\n    '
    head_body_separator_pat = None
    double_width_pad_char = '\x00'

    def parse(self, block):
        """
        Analyze the text `block` and return a table data structure.

        Given a plaintext-graphic table in `block` (list of lines of text; no
        whitespace padding), parse the table, construct and return the data
        necessary to construct a CALS table or equivalent.

        Raise `TableMarkupError` if there is any problem with the markup.
        """
        self.setup(block)
        self.find_head_body_sep()
        self.parse_table()
        structure = self.structure_from_cells()
        return structure

    def find_head_body_sep(self):
        """Look for a head/body row separator line; store the line index."""
        for i in range(len(self.block)):
            line = self.block[i]
            if self.head_body_separator_pat.match(line):
                if self.head_body_sep:
                    raise TableMarkupError(('Multiple head/body row separators (table lines %s and %s); only one allowed.' % (
                     self.head_body_sep + 1, i + 1)),
                      offset=i)
                else:
                    self.head_body_sep = i
                    self.block[i] = line.replace('=', '-')

        if self.head_body_sep == 0 or self.head_body_sep == len(self.block) - 1:
            raise TableMarkupError('The head/body row separator may not be the first or last line of the table.', offset=i)


class GridTableParser(TableParser):
    __doc__ = "\n    Parse a grid table using `parse()`.\n\n    Here's an example of a grid table::\n\n        +------------------------+------------+----------+----------+\n        | Header row, column 1   | Header 2   | Header 3 | Header 4 |\n        +========================+============+==========+==========+\n        | body row 1, column 1   | column 2   | column 3 | column 4 |\n        +------------------------+------------+----------+----------+\n        | body row 2             | Cells may span columns.          |\n        +------------------------+------------+---------------------+\n        | body row 3             | Cells may  | - Table cells       |\n        +------------------------+ span rows. | - contain           |\n        | body row 4             |            | - body elements.    |\n        +------------------------+------------+---------------------+\n\n    Intersections use '+', row separators use '-' (except for one optional\n    head/body row separator, which uses '='), and column separators use '|'.\n\n    Passing the above table to the `parse()` method will result in the\n    following data structure::\n\n        ([24, 12, 10, 10],\n         [[(0, 0, 1, ['Header row, column 1']),\n           (0, 0, 1, ['Header 2']),\n           (0, 0, 1, ['Header 3']),\n           (0, 0, 1, ['Header 4'])]],\n         [[(0, 0, 3, ['body row 1, column 1']),\n           (0, 0, 3, ['column 2']),\n           (0, 0, 3, ['column 3']),\n           (0, 0, 3, ['column 4'])],\n          [(0, 0, 5, ['body row 2']),\n           (0, 2, 5, ['Cells may span columns.']),\n           None,\n           None],\n          [(0, 0, 7, ['body row 3']),\n           (1, 0, 7, ['Cells may', 'span rows.', '']),\n           (1, 1, 7, ['- Table cells', '- contain', '- body elements.']),\n           None],\n          [(0, 0, 9, ['body row 4']), None, None, None]])\n\n    The first item is a list containing column widths (colspecs). The second\n    item is a list of head rows, and the third is a list of body rows. Each\n    row contains a list of cells. Each cell is either None (for a cell unused\n    because of another cell's span), or a tuple. A cell tuple contains four\n    items: the number of extra rows used by the cell in a vertical span\n    (morerows); the number of extra columns used by the cell in a horizontal\n    span (morecols); the line offset of the first line of the cell contents;\n    and the cell contents, a list of lines of text.\n    "
    head_body_separator_pat = re.compile('\\+=[=+]+=\\+ *$')

    def setup(self, block):
        self.block = block[:]
        self.block.disconnect()
        self.bottom = len(block) - 1
        self.right = len(block[0]) - 1
        self.head_body_sep = None
        self.done = [-1] * len(block[0])
        self.cells = []
        self.rowseps = {0: [0]}
        self.colseps = {0: [0]}

    def parse_table(self):
        """
        Start with a queue of upper-left corners, containing the upper-left
        corner of the table itself. Trace out one rectangular cell, remember
        it, and add its upper-right and lower-left corners to the queue of
        potential upper-left corners of further cells. Process the queue in
        top-to-bottom order, keeping track of how much of each text column has
        been seen.

        We'll end up knowing all the row and column boundaries, cell positions
        and their dimensions.
        """
        corners = [
         (0, 0)]
        while corners:
            top, left = corners.pop(0)
            if top == self.bottom or left == self.right or top <= self.done[left]:
                continue
            result = self.scan_cell(top, left)
            if not result:
                continue
            bottom, right, rowseps, colseps = result
            update_dict_of_lists(self.rowseps, rowseps)
            update_dict_of_lists(self.colseps, colseps)
            self.mark_done(top, left, bottom, right)
            cellblock = self.block.get_2D_block(top + 1, left + 1, bottom, right)
            cellblock.disconnect()
            cellblock.replace(self.double_width_pad_char, '')
            self.cells.append((top, left, bottom, right, cellblock))
            corners.extend([(top, right), (bottom, left)])
            corners.sort()

        if not self.check_parse_complete():
            raise TableMarkupError('Malformed table; parse incomplete.')

    def mark_done(self, top, left, bottom, right):
        """For keeping track of how much of each text column has been seen."""
        before = top - 1
        after = bottom - 1
        for col in range(left, right):
            assert self.done[col] == before
            self.done[col] = after

    def check_parse_complete(self):
        """Each text column should have been completely seen."""
        last = self.bottom - 1
        for col in range(self.right):
            if self.done[col] != last:
                return False

        return True

    def scan_cell(self, top, left):
        """Starting at the top-left corner, start tracing out a cell."""
        assert self.block[top][left] == '+'
        result = self.scan_right(top, left)
        return result

    def scan_right(self, top, left):
        """
        Look for the top-right corner of the cell, and make note of all column
        boundaries ('+').
        """
        colseps = {}
        line = self.block[top]
        for i in range(left + 1, self.right + 1):
            if line[i] == '+':
                colseps[i] = [
                 top]
                result = self.scan_down(top, left, i)
                if result:
                    bottom, rowseps, newcolseps = result
                    update_dict_of_lists(colseps, newcolseps)
                    return (bottom, i, rowseps, colseps)
                elif line[i] != '-':
                    return

    def scan_down(self, top, left, right):
        """
        Look for the bottom-right corner of the cell, making note of all row
        boundaries.
        """
        rowseps = {}
        for i in range(top + 1, self.bottom + 1):
            if self.block[i][right] == '+':
                rowseps[i] = [
                 right]
                result = self.scan_left(top, left, i, right)
                if result:
                    newrowseps, colseps = result
                    update_dict_of_lists(rowseps, newrowseps)
                    return (i, rowseps, colseps)
                elif self.block[i][right] != '|':
                    return

    def scan_left(self, top, left, bottom, right):
        """
        Noting column boundaries, look for the bottom-left corner of the cell.
        It must line up with the starting point.
        """
        colseps = {}
        line = self.block[bottom]
        for i in range(right - 1, left, -1):
            if line[i] == '+':
                colseps[i] = [
                 bottom]

        if line[left] != '+':
            return
        result = self.scan_up(top, left, bottom, right)
        if result is not None:
            rowseps = result
            return (rowseps, colseps)

    def scan_up(self, top, left, bottom, right):
        """
        Noting row boundaries, see if we can return to the starting point.
        """
        rowseps = {}
        for i in range(bottom - 1, top, -1):
            if self.block[i][left] == '+':
                rowseps[i] = [
                 left]

        return rowseps

    def structure_from_cells(self):
        """
        From the data collected by `scan_cell()`, convert to the final data
        structure.
        """
        rowseps = list(self.rowseps.keys())
        rowseps.sort()
        rowindex = {}
        for i in range(len(rowseps)):
            rowindex[rowseps[i]] = i

        colseps = list(self.colseps.keys())
        colseps.sort()
        colindex = {}
        for i in range(len(colseps)):
            colindex[colseps[i]] = i

        colspecs = [colseps[i] - colseps[(i - 1)] - 1 for i in range(1, len(colseps))]
        onerow = [None for i in range(len(colseps) - 1)]
        rows = [onerow[:] for i in range(len(rowseps) - 1)]
        remaining = (len(rowseps) - 1) * (len(colseps) - 1)
        for top, left, bottom, right, block in self.cells:
            rownum = rowindex[top]
            colnum = colindex[left]
            assert rows[rownum][colnum] is None, 'Cell (row %s, column %s) already used.' % (
             rownum + 1, colnum + 1)
            morerows = rowindex[bottom] - rownum - 1
            morecols = colindex[right] - colnum - 1
            remaining -= (morerows + 1) * (morecols + 1)
            rows[rownum][colnum] = (
             morerows, morecols, top + 1, block)

        if not remaining == 0:
            raise AssertionError('Unused cells remaining.')
        elif self.head_body_sep:
            numheadrows = rowindex[self.head_body_sep]
            headrows = rows[:numheadrows]
            bodyrows = rows[numheadrows:]
        else:
            headrows = []
            bodyrows = rows
        return (
         colspecs, headrows, bodyrows)


class SimpleTableParser(TableParser):
    __doc__ = "\n    Parse a simple table using `parse()`.\n\n    Here's an example of a simple table::\n\n        =====  =====\n        col 1  col 2\n        =====  =====\n        1      Second column of row 1.\n        2      Second column of row 2.\n               Second line of paragraph.\n        3      - Second column of row 3.\n\n               - Second item in bullet\n                 list (row 3, column 2).\n        4 is a span\n        ------------\n        5\n        =====  =====\n\n    Top and bottom borders use '=', column span underlines use '-', column\n    separation is indicated with spaces.\n\n    Passing the above table to the `parse()` method will result in the\n    following data structure, whose interpretation is the same as for\n    `GridTableParser`::\n\n        ([5, 25],\n         [[(0, 0, 1, ['col 1']),\n           (0, 0, 1, ['col 2'])]],\n         [[(0, 0, 3, ['1']),\n           (0, 0, 3, ['Second column of row 1.'])],\n          [(0, 0, 4, ['2']),\n           (0, 0, 4, ['Second column of row 2.',\n                      'Second line of paragraph.'])],\n          [(0, 0, 6, ['3']),\n           (0, 0, 6, ['- Second column of row 3.',\n                      '',\n                      '- Second item in bullet',\n                      '  list (row 3, column 2).'])],\n          [(0, 1, 10, ['4 is a span'])],\n          [(0, 0, 12, ['5']),\n           (0, 0, 12, [''])]])\n    "
    head_body_separator_pat = re.compile('=[ =]*$')
    span_pat = re.compile('-[ -]*$')

    def setup(self, block):
        self.block = block[:]
        self.block.disconnect()
        self.block[0] = self.block[0].replace('=', '-')
        self.block[-1] = self.block[(-1)].replace('=', '-')
        self.head_body_sep = None
        self.columns = []
        self.border_end = None
        self.table = []
        self.done = [-1] * len(block[0])
        self.rowseps = {0: [0]}
        self.colseps = {0: [0]}

    def parse_table(self):
        """
        First determine the column boundaries from the top border, then
        process rows.  Each row may consist of multiple lines; accumulate
        lines until a row is complete.  Call `self.parse_row` to finish the
        job.
        """
        self.columns = self.parse_columns(self.block[0], 0)
        self.border_end = self.columns[(-1)][1]
        firststart, firstend = self.columns[0]
        offset = 1
        start = 1
        text_found = None
        while offset < len(self.block):
            line = self.block[offset]
            if self.span_pat.match(line):
                self.parse_row(self.block[start:offset], start, (
                 line.rstrip(), offset))
                start = offset + 1
                text_found = None
            else:
                if line[firststart:firstend].strip():
                    if text_found:
                        if offset != start:
                            self.parse_row(self.block[start:offset], start)
                    start = offset
                    text_found = 1
                else:
                    if not text_found:
                        start = offset + 1
            offset += 1

    def parse_columns(self, line, offset):
        """
        Given a column span underline, return a list of (begin, end) pairs.
        """
        cols = []
        end = 0
        while True:
            begin = line.find('-', end)
            end = line.find(' ', begin)
            if begin < 0:
                break
            if end < 0:
                end = len(line)
            cols.append((begin, end))

        if self.columns:
            if cols[(-1)][1] != self.border_end:
                raise TableMarkupError(('Column span incomplete in table line %s.' % (offset + 1)),
                  offset=offset)
            cols[-1] = (cols[(-1)][0], self.columns[(-1)][1])
        return cols

    def init_row(self, colspec, offset):
        i = 0
        cells = []
        for start, end in colspec:
            morecols = 0
            try:
                assert start == self.columns[i][0]
                while end != self.columns[i][1]:
                    i += 1
                    morecols += 1

            except (AssertionError, IndexError):
                raise TableMarkupError(('Column span alignment problem in table line %s.' % (offset + 2)),
                  offset=(offset + 1))

            cells.append([0, morecols, offset, []])
            i += 1

        return cells

    def parse_row(self, lines, start, spanline=None):
        """
        Given the text `lines` of a row, parse it and append to `self.table`.

        The row is parsed according to the current column spec (either
        `spanline` if provided or `self.columns`).  For each column, extract
        text from each line, and check for text in column margins.  Finally,
        adjust for insignificant whitespace.
        """
        if not lines:
            if not spanline:
                return
        elif spanline:
            columns = (self.parse_columns)(*spanline)
            span_offset = spanline[1]
        else:
            columns = self.columns[:]
            span_offset = start
        self.check_columns(lines, start, columns)
        row = self.init_row(columns, start)
        for i in range(len(columns)):
            start, end = columns[i]
            cellblock = lines.get_2D_block(0, start, len(lines), end)
            cellblock.disconnect()
            cellblock.replace(self.double_width_pad_char, '')
            row[i][3] = cellblock

        self.table.append(row)

    def check_columns(self, lines, first_line, columns):
        """
        Check for text in column margins and text overflow in the last column.
        Raise TableMarkupError if anything but whitespace is in column margins.
        Adjust the end value for the last column if there is text overflow.
        """
        columns.append((sys.maxsize, None))
        lastcol = len(columns) - 2
        lines = [strip_combining_chars(line) for line in lines]
        for i in range(len(columns) - 1):
            start, end = columns[i]
            nextstart = columns[(i + 1)][0]
            offset = 0
            for line in lines:
                if i == lastcol and line[end:].strip():
                    text = line[start:].rstrip()
                    new_end = start + len(text)
                    main_start, main_end = self.columns[(-1)]
                    columns[i] = (start, max(main_end, new_end))
                    if new_end > main_end:
                        self.columns[-1] = (
                         main_start, new_end)
                else:
                    if line[end:nextstart].strip():
                        raise TableMarkupError(('Text in column margin in table line %s.' % (first_line + offset + 1)),
                          offset=(first_line + offset))
                    offset += 1

        columns.pop()

    def structure_from_cells(self):
        colspecs = [end - start for start, end in self.columns]
        first_body_row = 0
        if self.head_body_sep:
            for i in range(len(self.table)):
                if self.table[i][0][2] > self.head_body_sep:
                    first_body_row = i
                    break

        return (
         colspecs, self.table[:first_body_row],
         self.table[first_body_row:])


def update_dict_of_lists(master, newdata):
    """
    Extend the list values of `master` with those from `newdata`.

    Both parameters must be dictionaries containing list values.
    """
    for key, values in list(newdata.items()):
        master.setdefault(key, []).extend(values)