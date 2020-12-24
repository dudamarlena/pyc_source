# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/text_table.py
# Compiled at: 2018-06-11 12:57:38
# Size of source mod 2**32: 26379 bytes
__all__ = [
 'text_table']
import cgi, csv, sys
try:
    import StringIO
except ImportError:
    import io as StringIO

def pad_list(l, n, value=None):
    """
    pad_list( list, n, value=None) - append value to list until it list[n] exists
    """
    while n >= len(l):
        l.append(value)


class text_table_cell:
    __doc__ = '\n    private - single cell of a text_table\n    '

    def __init__(self):
        self.text = None
        self.code = False
        self.sort_key = None
        self.link = None
        self.html = None
        self.html_attributes = None

    def __repr__(self):
        return repr(self.text)

    def set_value(self, text=None, link=None, html=None, sort_key=None, code=False):
        self.text = text
        self.link = link
        self.html = html
        self.code = code
        if sort_key is None:
            self.sort_key = text
        else:
            self.sort_key = sort_key

    def get_text(self):
        return self.text


class text_table_row:
    __doc__ = '\n    private - single row of a text_table\n    '

    def __init__(self):
        self.lst = []
        self.sort_order = [
         0]

    if sys.version_info < (3, 0):

        def __cmp__(self, other):
            for x in self.sort_order:
                if x < 0:
                    r = -1
                else:
                    r = 1
                if self.lst[x].sort_key < other.lst[x].sort_key:
                    return -r
                if self.lst[x].sort_key > other.lst[x].sort_key:
                    return r

            return 0

    else:

        def __lt__(self, other):
            r = 0
            for x in self.sort_order:
                if self.lst[x].sort_key < other.lst[x].sort_key:
                    return r - 1

            return r

        def __gt__(self, other):
            r = 0
            for x in self.sort_order:
                if self.lst[x].sort_key > other.lst[x].sort_key:
                    return r + 1

            return r

        def __eq__(self, other):
            r = 0
            for x in self.sort_order:
                if self.lst[x].sort_key == other.lst[x].sort_key:
                    return r

            return r

    def def_sort_order(self, sort_order):
        self.sort_order = sort_order

    def pad(self, n):
        l = self.lst
        while len(l) < n:
            l.append(text_table_cell())

        x = 0
        while x < n:
            if l[x] is None:
                l[x] = text_table_cell()
            x += 1


class text_table:
    __doc__ = '\n    text_table - a row/column table creator\n\n    A text_table is a table of rows and columns.  You create the table,\n    fill the individual cells, then extract the table in various formats.\n\n    Supported output formats include\n        HTML\n        CSV\n        awk\n            Columns of text are separated by tabs.\n\n    Create the table with the class constructor:\n\n        t = text_table.text_table()\n\n    The table begins as 0 rows and 0 columns.  New rows and columns appear\n    when set.  Each row may have a different number of columns.\n\n    Declare column names if necessary:\n        t.define_column("Thing")    # next available column\n        t.define_column("Thing",0)  # title for column 0\n\n    Fill column values:\n        t.set_value(row=0, col=0, value="foo")\n\n    Extract the output:\n        print t.get_html()\n\n\n    Methods: (see individual method documentation for details)\n\n    define_column()\n        defines the name of a column\n\n    set_value()\n        sets the value in a row/column; values are normally text, but\n        this is not required.\n\n    set_html_table_attributes()\n        set a string to be included in the <table> directive\n\n    set_html_cell_attributes()\n        set a string to be included in the <td> directive\n\n    sort()\n        sort the table\n\n    pad()\n        force all rows to have as many columns as the widest row\n\n    join()\n        combine another text_table into this one, with new columns to\n        the right.\n\n    get_html()\n    get_csv()\n    get_awk()\n        return the table content as a string in selected defined format.\n\n    '

    def __init__(self):
        self.colmap = {}
        self.number_of_columns = 0
        self.rows = []
        self.html_table_attributes = ''
        self.suppressed = []
        self.titles = []
        self.title_links = []
        self.title_html = []

    def define_column(self, name, num=-1, link=None, html=None, showname=None):
        if num < 0:
            if name in self.colmap:
                num = self.colmap[name]
            else:
                num = self.number_of_columns
                self.number_of_columns = self.number_of_columns + 1
        else:
            self.colmap[name] = int(num)
            pad_list(self.titles, num, '')
            pad_list(self.title_links, num, None)
            pad_list(self.title_html, num, None)
            if showname is not None:
                self.titles[num] = showname
            else:
                self.titles[num] = name
        self.title_links[num] = link
        self.title_html[num] = html
        return num

    def set_value(self, row, col, text=None, link=None, html=None, sort_key=None, code=False):
        o = self._row_col_cell(row, col)
        o.set_value(text, link, html, sort_key, code)

    def get_cell(self, row, col):
        if row >= len(self.rows):
            return
        else:
            row = self.rows[row]
            if col >= len(row.lst):
                return
            return row.lst[col]

    def get_title(self, col):
        if col in self.colmap:
            col = self.colmap[col]
        return self.titles[col].get_text()

    def get_row_count(self):
        return len(self.rows)

    def set_html_table_attributes(self, attr):
        self.html_table_attributes = attr

    def set_html_cell_attributes(self, row, col, attr):
        o = self._row_col_cell(row, col)
        o.html_attributes = attr

    def sort(self, sort_order, reverse=False):
        so = []
        for x in sort_order:
            if isinstance(x, type('')):
                if x in self.colmap:
                    so.append(self.colmap[x])
            else:
                so.append(x)

        for x in self.rows:
            x.def_sort_order(so)

        self.pad()
        self.rows.sort(reverse=reverse)

    def set_sort_key(self, col, func):
        fail = 0
        for row in range(0, len(self.rows)):
            o = self._row_col_cell(row, col)
            try:
                o.sort_key = func(o.text)
            except Exception as e:
                o.sort_key = o.text
                fail = fail + 1

        conv = len(self.rows) - fail

    def pad(self):
        count = 0
        for r in self.rows:
            this_width = len(r.lst)
            if this_width > count:
                count = this_width

        self.number_of_columns = count
        for i, r in enumerate(self.rows):
            if r is None:
                self.rows[i] = r = text_table_row()
            r.pad(count)

    def join(self, other):
        self.pad()
        if len(other.rows) == 0:
            return
        x = len(self.rows)
        while x < len(other.rows):
            self.set_value(x, 0, '')
            x = x + 1

        x = len(other.rows)
        while x < len(self.rows):
            other.set_value(x, 0, '')
            x = x + 1

        x = 0
        while x < len(self.rows):
            self.rows[x].lst.extend(other.rows[x].lst)
            x = x + 1

        for x in other.colmap:
            if x not in self.colmap:
                self.colmap[x] = other.colmap[x] + self.number_of_columns

        self.titles.extend(other.titles)
        self.title_links.extend(other.title_links)
        self.title_html.extend(other.title_html)
        self.number_of_columns = len(self.titles)

    def _row_object(self, row):
        while len(self.rows) <= row:
            self.rows.append(text_table_row())

        return self.rows[row]

    def _row_col_cell(self, row, col):
        o = self._row_object(row)
        this_row = o.lst
        if col in self.colmap:
            col = self.colmap[col]
        try:
            col = int(col)
        except ValueError:
            self.define_column(col)
            col = self.colmap[col]

        while len(this_row) <= col:
            this_row.append(text_table_cell())

        if col > self.number_of_columns:
            self.number_of_columns = col + 1
        return this_row[col]

    def suppress(self, col, flag=1):
        """
        Declare whether this column should be displayed in the output.

        col     - column number or name
        flag    - true=suppress, false=display
        """
        if col in self.colmap:
            col = self.colmap[col]
        while len(self.suppressed) <= col:
            self.suppressed.append(0)

        self.suppressed[col] = flag

    def is_suppressed(self, colcount):
        """
        Return whether this column should be displayed in the output.

        true=suppressed, false=displayed
        """
        while colcount >= len(self.suppressed):
            self.suppressed.append(0)

        return self.suppressed[colcount]

    def get_html(self, headings=True, color_rows=0):
        """"
        Return HTML of the table.

        str = o.get_html( headings=True )
        headings    - True=show headings, False=do not show headings

        If the table rows are not all the same length, the display will
        not look good on most browsers.  use o.pad() first.

        See also:
            define_column - determines table headings
            set_html_table_attributes - values in <table> directive
            set_html_cell_attributes - values in <td> directive

        """
        s = StringIO.StringIO()
        s.write('<table ' + self.html_table_attributes + '>\n')
        if headings:
            s.write('<tr>')
            colcount = -1
            for r in self.titles:
                colcount = colcount + 1
                if self.is_suppressed(colcount):
                    pass
                else:
                    s.write('<th>')
                    if self.title_html[colcount]:
                        s.write(self.title_html[colcount])
                    else:
                        if self.title_links[colcount]:
                            s.write("<a href='" + self.title_links[colcount] + "'>")
                            s.write(cgi.escape(str(r)))
                            s.write('</a>')
                        else:
                            s.write(r)
                    s.write('</th>')

            s.write('</tr>\n')
        row = 0
        for r in self.rows:
            row = row + 1
            if color_rows:
                if row % color_rows == 0:
                    s.write('<tr bgcolor=lightgray>')
            else:
                s.write('<tr>')
            r = r.lst
            if r is None:
                pass
            else:
                colcount = -1
                for c in r:
                    colcount = colcount + 1
                    if self.is_suppressed(colcount):
                        pass
                    else:
                        if c is None:
                            s.write('<td>&nbsp</td>\n')
                        else:
                            if c.html_attributes:
                                s.write('<td ')
                                if 'valign' not in c.html_attributes:
                                    s.write('valign=top ')
                                s.write(c.html_attributes)
                                s.write('>')
                            else:
                                s.write('<td valign=top>')
                    if c.link:
                        s.write("<a href='" + c.link + "'>")
                    if c.html:
                        if c.html == '':
                            s.write('&nbsp;')
                        else:
                            s.write(c.html)
                    else:
                        if c.text is not None:
                            if c.code:
                                s.write('<pre>{}</pre>'.format(c.text))
                            elif c.text is not None:
                                if not c.code:
                                    s.write(cgi.escape(str(c.text)))
                            else:
                                s.write('&nbsp;')
                        elif c.link:
                            s.write('</a>')
                        s.write('</td>\n')

            s.write('</tr>\n')

        s.write('</table>')
        rval = s.getvalue()
        s.close()
        del s
        return rval

    def get_csv(self, newline='\n', headings=False):
        """
        str = o.get_csv()
        str = o.get_csv(newline='
')

        Generate table output in CSV format, using the standard python csv module.
        The newline parameter specifies the line terminator, default is "
".

        Returns a string.

        """
        s = StringIO.StringIO()
        w = csv.writer(s, lineterminator=newline)
        if headings:
            l = []
            colcount = -1
            for r in self.titles:
                colcount = colcount + 1
                if self.is_suppressed(colcount):
                    pass
                else:
                    l.append(r)

            w.writerow(l)
        for r in self.rows:
            r = r.lst
            if r is None:
                w.writerow([])
            else:
                l = []
                colcount = -1
                for c in r:
                    colcount = colcount + 1
                    if self.is_suppressed(colcount):
                        pass
                    else:
                        if c is None:
                            l.append('')
                        else:
                            l.append(c.text)

                w.writerow(l)

        rval = s.getvalue()
        s.close()
        return rval

    def get_awk(self, blank='-', tabwidth=8, separator='\t', headings=False):
        """
        string = o.get_awk(blank="-", tabwidth=8, separator="   " )

        Generate table output suitable for processing by awk:
            - each column is printed as plain text
            - separator is printed between columns
            - tabs in the text are converted to spaces (with 8 column tab stops)
            - newline

        Columns are separated by tabs.

        Parameter blank is printed for columns that are empty.
        Columns that are missing (i.e. this row is not as wide
        as some other row) are not printed.

        Data values that contain tabs have tabs expanded to spaces
        according to parameter tabwidth.

        """
        s = StringIO.StringIO()
        if headings:
            for col, x in enumerate(self.titles):
                if self.is_suppressed(col):
                    pass
                else:
                    s.write(x)
                    s.write(separator)

            s.write('\n')
        for r in self.rows:
            if r:
                if r.lst:
                    for col, cell in enumerate(r.lst):
                        if self.is_suppressed(col):
                            pass
                        else:
                            if cell is None or cell.text is None or cell.text == '':
                                s.write(blank)
                            else:
                                s.write(str(cell.text).expandtabs(tabwidth))
                            s.write(separator)

            s.write('\n')

        rval = s.getvalue()
        s.close()
        return rval

    def _rst_border(self, col_widths):
        l = []
        for col, wid in enumerate(col_widths):
            if self.is_suppressed(col):
                pass
            else:
                l.append('=' * wid)
                l.append('  ')

        l.append('\n')
        return ''.join(l)

    def get_rst(self, include_border=True, headings=False):
        """
        string = o.get_rst()

        generate table output suitable for use in restructured text

        uses ==== above and below the table

        """
        s = StringIO.StringIO()
        col_widths = []
        if headings:
            for x in self.titles:
                col_widths.append(len(x))

        for r in self.rows:
            if r and r.lst:
                for col in range(0, len(r.lst)):
                    while col >= len(col_widths):
                        col_widths.append(0)

                    l = len(str(r.lst[col].text))
                    if col_widths[col] < l:
                        col_widths[col] = l

        if include_border:
            border = self._rst_border(col_widths)
            s.write(border)
        if headings:
            for col, title in enumerate(self.titles):
                if self.is_suppressed(col):
                    pass
                else:
                    s.write('%-*s' % (col_widths[col], str(title)))
                    s.write('  ')

            s.write('\n')
        for r in self.rows:
            if r:
                if r.lst:
                    for col in range(0, len(r.lst)):
                        if self.is_suppressed(col):
                            pass
                        else:
                            s.write('%-*s' % (col_widths[col], str(r.lst[col].text)))
                            s.write('  ')

            s.write('\n')

        if include_border:
            s.write(border)
        rval = s.getvalue()
        s.close()
        return rval

    def get_text(self):
        """
        string = o.get_text()

        generate table output suitable for use in plain text
        """
        return self.get_rst(include_border=False)

    def get_trac_wiki(self, headings=False):
        """
        string = o.get_trac_wiki()

        generate table output suitable for use in a trac wiki

        """
        col_widths = [0 for x in self.titles]
        s = StringIO.StringIO()
        if headings:
            for col, x in enumerate(self.titles):
                if self.is_suppressed(col):
                    pass
                else:
                    col_widths[col] = len(str(x))

        for r in self.rows:
            if r and r.lst:
                for x in range(0, len(r.lst)):
                    while x >= len(col_widths):
                        col_widths.append(0)

                    l = len(str(r.lst[x].text))
                    if col_widths[x] < l:
                        col_widths[x] = l

        if headings:
            for col, x in enumerate(self.titles):
                if self.is_suppressed(col):
                    pass
                else:
                    s.write('|| %-*s ' % (col_widths[col], str(x)))

            s.write('||\n')
        for r in self.rows:
            if r:
                if r.lst:
                    for col in range(0, len(r.lst)):
                        if self.is_suppressed(col):
                            pass
                        else:
                            s.write('|| %-*s ' % (
                             col_widths[col], str(r.lst[col].text)))

            s.write('||\n')

        rval = s.getvalue()
        s.close()
        return rval

    def get(self, format='rst', headings=False):
        if format == 'html':
            return self.get_html(headings=headings)
        else:
            if format == 'csv':
                return self.get_csv(headings=headings)
            else:
                if format == 'awk':
                    return self.get_awk(headings=headings)
                if format == 'rst' or format == 'text':
                    return self.get_rst(headings=headings)
                if format == 'trac_wiki' or format == 'tw':
                    return self.get_trac_wiki(headings=headings)
            return 'Format %s not recognized in text_table.get' % format


def sequence_to_table(l):
    t = text_table()
    for row, x in enumerate(l):
        for col, y in enumerate(x):
            t.set_value(row, col, y)

    return t


if __name__ == '__main__':
    import sys
    t = text_table()
    t.set_html_table_attributes('border=1 bgcolor=blue')
    l = [
     ('a', 1),
     ('z', 5),
     ('z', 7),
     ('b', 9),
     ('a', 2),
     ('b', 4),
     ('x', 6),
     ('a', 8)]
    c = 0
    for x in l:
        v1, v2 = x
        v2 = v2 + 10
        t.set_value(c, 0, c)
        t.set_value(c, 1, v1)
        t.set_value(c, 2, v2)
        t.set_html_cell_attributes(c, 1, 'bgcolor=gray')
        c += 1

    c = c + 2
    t.set_value(c, 0, c)
    t.set_value(c, 1, 'arf')
    t.set_html_cell_attributes(3, 2, 'bgcolor=red')
    t.pad()
    print('')
    s = t.get_html()
    print(s)
    print('')
    s = t.get_awk()
    print(s)
    print('')
    t.sort([-1, 2])
    s = t.get_awk()
    print(s)
    print('')
    t.sort([0])
    s = t.get_awk()
    print(s)
    print('')
    print(t.get_csv())
    t = text_table()
    t.set_value(0, 0, '4')
    t.set_value(1, 0, '3')
    t.set_value(2, 0, '2')
    t.set_value(3, 0, '1')
    t.set_value(4, 0, '')
    t.set_value(5, 0, 'C')
    t.set_value(6, 0, 'B')
    t.set_value(7, 0, 'A')
    t.set_sort_key(0, float)
    print('XX')
    print(t.get_awk())
    print('XX')
    t.sort([0], reverse=True)
    print(t.get_awk())
    print('XX')
    t.sort([0], reverse=False)
    print(t.get_awk())
    print('XX')
    print('')
    s = t.get_rst()
    print(s)
    print('')
    s = t.get_trac_wiki()
    print(s)