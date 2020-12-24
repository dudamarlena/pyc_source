# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/sphinx_util.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 4277 bytes
"""
Provides utility function for generating Sphinx-based documentation.
"""
from beehive.textutil import compute_words_maxsize
from beehive.compat import unicode
import codecs

class DocumentWriter(object):
    __doc__ = '\n    Provides a simple "ReStructured Text Writer" to generate\n    Sphinx-based documentation.\n    '
    heading_styles = ['=', '=', '-', '~']
    default_encoding = 'utf-8'
    default_toctree_title = '**Contents:**'

    def __init__(self, stream, filename=None, should_close=True):
        self.stream = stream
        self.filename = filename
        self.should_close = should_close

    @classmethod
    def open(cls, filename, encoding=None):
        encoding = encoding or cls.default_encoding
        stream = codecs.open(filename, 'wt', encoding)
        return cls(stream, filename)

    def write(self, *args):
        return self.stream.write(*args)

    def close(self):
        if self.stream:
            if self.should_close:
                self.stream.close()
        self.stream = None

    def write_heading(self, heading, level=0, index_id=None):
        assert self.stream
        assert heading, 'Heading should not be empty'
        assert 0 <= level < len(self.heading_styles)
        if level >= len(self.heading_styles):
            level = len(self.heading_styles) - 1
        heading_size = len(heading)
        heading_style = self.heading_styles[level]
        if level == 0:
            if heading_size < 70:
                heading_size = 70
        separator = heading_style * heading_size
        if index_id:
            if isinstance(index_id, (list, tuple)):
                index_id = ', '.join(index_id)
            self.stream.write('.. index:: %s\n\n' % index_id)
        if level == 0:
            self.stream.write('%s\n' % separator)
        self.stream.write('%s\n' % heading)
        self.stream.write('%s\n' % separator)
        self.stream.write('\n')

    def write_toctree(self, entries, title=None, maxdepth=2):
        if title is None:
            title = self.default_toctree_title
        line_prefix = '    '
        if title:
            self.stream.write('%s\n\n' % title)
        self.stream.write('.. toctree::\n')
        self.stream.write('%s:maxdepth: %d\n\n' % (line_prefix, maxdepth))
        for entry in entries:
            self.stream.write('%s%s\n' % (line_prefix, entry))

        self.stream.write('\n')

    def write_table(self, table):
        """
        Write a ReST simple table.

        EXAMPLE:
        ========================================= ===== ===== ===== =====
        Step Definition                           Given When  Then  Step
        ========================================= ===== ===== ===== =====
        Given a file named "{filename}" contains
        Then the file "{filename}" should ...
        ========================================= ===== ===== ===== =====

        :param table:   Table to render (as `beehive.model.Table`)

        .. todo::
            Column alignments
        """
        assert self.stream
        cols_size = []
        separator_parts = []
        row_schema_parts = []
        for col_index, heading in enumerate(table.headings):
            column = [unicode(row[col_index]) for row in table.rows]
            column.append(heading)
            column_size = compute_words_maxsize(column)
            cols_size.append(column_size)
            separator_parts.append('=' * column_size)
            row_schema_parts.append('%-' + str(column_size) + 's')

        separator = ' '.join(separator_parts) + '\n'
        row_schema = ' '.join(row_schema_parts) + '\n'
        self.stream.write('\n')
        self.stream.write(separator)
        self.stream.write(row_schema % tuple(table.headings))
        self.stream.write(separator)
        for row in table.rows:
            self.stream.write(row_schema % tuple(row))

        self.stream.write(separator)
        self.stream.write('\n')