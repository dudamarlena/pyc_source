# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/verify/asserts/tabular.py
# Compiled at: 2018-04-20 03:19:42
import re

def get_first_line(output):
    match = re.search('^(.*)$', output, flags=re.MULTILINE)
    if match is None:
        return
    else:
        return match.group(1)
        return


def assert_has_n_columns(output, n, sep='\t'):
    """ Asserts the tabular output contains n columns. The optional
    sep argument specifies the column seperator used to determine the
    number of columns."""
    n = int(n)
    first_line = get_first_line(output)
    assert first_line is not None, 'Was expecting output with %d columns, but output was empty.' % n
    assert len(first_line.split(sep)) == n, 'Output does not have %d columns.' % n
    return