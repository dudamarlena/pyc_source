# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/tablepprint.py
# Compiled at: 2019-08-19 15:09:29
"""Adapted from http://code.activestate.com/recipes/267662/"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str
from builtins import range
from functools import reduce
import operator, re, math
__docformat__ = 'restructuredtext'

def indent(rows, hasHeader=False, headerChar='-', delim=' | ', justify='left', separateRows=False, prefix='', postfix='', wrapfunc=lambda x: x):
    """Indents a table by column.
    :param rows: A sequence of sequences of items, one sequence per row.
    :param hasHeader: True if the first row consists of the columns' names.
    :param headerChar: Character to be used for the row separator line
    (if hasHeader==True or separateRows==True).
    :param delim: The column delimiter.
    :param justify: Determines how are data justified in their column.
    Valid values are 'left','right' and 'center'.
    :param separateRows: True if rows are to be separated by a line of
    'headerChar's.
    :param prefix: A string prepended to each printed row.
    :param postfix: A string appended to each printed row.
    :param wrapfunc: A function f(text) for wrapping text;
    each element in the table is first wrapped by this function.
    :return: a list of strings. One for each row of the table
    """

    def rowWrapper(row):
        newRows = [ wrapfunc(item).split('\n') for item in row ]
        return [ [ substr or '' for substr in item ] for item in list(*newRows) ]

    logicalRows = [ rowWrapper(row) for row in rows ]
    columns = list(*reduce(operator.add, logicalRows))
    maxWidths = [ max([ len(str(item)) for item in column ]) for column in columns
                ]
    if separateRows or hasHeader:
        rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) + len(delim) * (len(maxWidths) - 1))
    else:
        rowSeparator = '<ERR>'
    justify = {'center': str.center, 'right': str.rjust, 'left': str.ljust}[justify.lower()]
    output = []
    if separateRows:
        output.append(rowSeparator)
    for physicalRows in logicalRows:
        for row in physicalRows:
            line = prefix
            line += delim.join([ justify(str(item), width) for item, width in zip(row, maxWidths)
                               ])
            line += postfix
            output.append(line)

        if separateRows or hasHeader:
            output.append(rowSeparator)
            hasHeader = False

    return output


def wrap_onspace(text, width):
    r"""A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' % (
     line,
     ' \n'[(len(line[line.rfind('\n') + 1:]) + len(word.split('\n', 1)[0]) >= width)],
     word), text.split(' '))


def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
       words longer than width are split."""
    wordRegex = re.compile('\\S{' + str(width) + ',}')
    return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(), width), text), width)


def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
       It doesn't split the text in words."""
    return ('\n').join([ text[width * i:width * (i + 1)] for i in range(int(math.ceil(1.0 * len(text) / width)))
                       ])


if __name__ == '__main__':
    labels = ('First Name', 'Last Name', 'Age', 'Position')
    data = 'John,Smith,24,Software Engineer\n       Mary,Brohowski,23,Sales Manager\n       Aristidis,Papageorgopoulos,28,Senior Reseacher'
    rows = [ row.strip().split(',') for row in data.splitlines() ]
    print('Without wrapping function\n')
    for l in indent([labels] + rows, hasHeader=True):
        print(l)

    width = 10
    for wrapper in (wrap_always, wrap_onspace, wrap_onspace_strict):
        print('Wrapping function: %s(x,width=%d)\n' % (wrapper.__name__, width))
        o = indent([labels] + rows, headerChar='=', hasHeader=True, separateRows=False, prefix='|', postfix='|', delim=' ', wrapfunc=lambda x: wrapper(x, width))
        for l in o:
            print(l)