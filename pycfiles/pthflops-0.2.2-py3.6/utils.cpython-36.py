# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pthflops/utils.py
# Compiled at: 2020-01-18 08:36:07
# Size of source mod 2**32: 821 bytes


def print_table(rows, header=['Operation', 'OPS']):
    """Simple helper function to print a list of lists as a table

    :param rows: a :class:`list` of :class:`list` containing the data to be printed. Each entry in the list
    represents an individual row
    :param input: (optional) a :class:`list` containing the header of the table
    """
    if len(rows) == 0:
        return
    col_max = [max([len(str(val[i])) for val in rows]) + 3 for i in range(len(rows[0]))]
    row_format = ''.join(['{:<' + str(length) + '}' for length in col_max])
    if len(header) > 0:
        print((row_format.format)(*header))
        print((row_format.format)(*['-' * (val - 2) for val in col_max]))
    for row in rows:
        print((row_format.format)(*row))

    print((row_format.format)(*['-' * (val - 3) for val in col_max]))