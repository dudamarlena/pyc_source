# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/input/extraction.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 742 bytes
from collections import OrderedDict
from eddington.exceptions import InvalidDataFile

def extract_data_from_rows(rows, file_name, sheet=None):
    headers = rows[0]
    if is_headers(headers):
        content = rows[1:]
    else:
        headers = range(len(headers))
        content = rows
    try:
        content = [map(float, row) for row in content]
        columns = zip(*content)
        return OrderedDict(zip(headers, columns))
    except ValueError:
        raise InvalidDataFile(file_name, sheet=sheet)


def is_headers(headers):
    return all([header != '' and not is_number(header) for header in headers])


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False