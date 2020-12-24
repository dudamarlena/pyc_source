# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/model_describe.py
# Compiled at: 2014-10-30 12:25:10
# Size of source mod 2**32: 3367 bytes
"""
Provides textual descriptions for :mod:`beehive.model` elements.
"""
from beehive.textutil import indent

def escape_cell(cell):
    """
    Escape table cell contents.
    :param cell:  Table cell (as unicode string).
    :return: Escaped cell (as unicode string).
    """
    cell = cell.replace('\\', '\\\\')
    cell = cell.replace('\n', '\\n')
    cell = cell.replace('|', '\\|')
    return cell


def escape_triple_quotes(text):
    """
    Escape triple-quotes, used for multi-line text/doc-strings.
    """
    return text.replace('"""', '\\"\\"\\"')


class ModelDescriptor(object):

    @staticmethod
    def describe_table(table, indentation=None):
        """
        Provide a textual description of the table (as used w/ Gherkin).

        :param table:  Table to use (as :class:`beehive.model.Table`)
        :param indentation:  Line prefix to use (as string, if any).
        :return: Textual table description (as unicode string).
        """
        cell_lengths = []
        all_rows = [
         table.headings] + table.rows
        for row in all_rows:
            lengths = [len(escape_cell(c)) for c in row]
            cell_lengths.append(lengths)

        max_lengths = []
        for col in range(0, len(cell_lengths[0])):
            max_lengths.append(max([c[col] for c in cell_lengths]))

        lines = []
        for r, row in enumerate(all_rows):
            line = '|'
            for c, (cell, max_length) in enumerate(zip(row, max_lengths)):
                pad_size = max_length - cell_lengths[r][c]
                line += ' %s%s |' % (escape_cell(cell), ' ' * pad_size)

            line += '\n'
            lines.append(line)

        if indentation:
            return indent(lines, indentation)
        return ''.join(lines)

    @staticmethod
    def describe_docstring(doc_string, indentation=None):
        """
        Provide a textual description of the multi-line text/triple-quoted
        doc-string (as used w/ Gherkin).

        :param doc_string:  Multi-line text to use.
        :param indentation:  Line prefix to use (as string, if any).
        :return: Textual table description (as unicode string).
        """
        text = escape_triple_quotes(doc_string)
        text = '"""\n' + text + '\n"""\n'
        if indentation:
            text = indent(text, indentation)
        return text


class ModelPrinter(ModelDescriptor):

    def __init__(self, stream):
        super(ModelPrinter, self).__init__()
        self.stream = stream

    def print_table(self, table, indentation=None):
        self.stream.write(self.describe_table(table, indentation))
        self.stream.flush()

    def print_docstring(self, text, indentation=None):
        self.stream.write(self.describe_docstring(text, indentation))
        self.stream.flush()