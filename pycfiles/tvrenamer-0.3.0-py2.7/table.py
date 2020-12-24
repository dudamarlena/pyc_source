# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/common/table.py
# Compiled at: 2015-11-08 18:31:47
"""Output formatters using prettytable."""
from __future__ import print_function
import prettytable, six
COLUMNS = [
 'status', 'original', 'formatted', 'reason']
ALIGNMENTS = {int: 'r', 
   str: 'l', 
   float: 'r'}
try:
    ALIGNMENTS[unicode] = 'l'
except NameError:
    pass

def write_output(data):
    tab = prettytable.PrettyTable(COLUMNS, print_empty=False)
    tab.padding_width = 1
    tab.max_width = 60
    data_iter = iter(data)
    first_row = next(data_iter)
    for value, name in zip(first_row, COLUMNS):
        alignment = ALIGNMENTS.get(type(value), 'l')
        tab.align[name] = alignment

    tab.add_row(first_row)
    for row in data_iter:
        row = [ r.replace('\r\n', '\n').replace('\r', ' ') if isinstance(r, six.string_types) else r for r in row
              ]
        tab.add_row(row)

    formatted = tab.get_string(fields=COLUMNS)
    print(formatted)
    print('\n')