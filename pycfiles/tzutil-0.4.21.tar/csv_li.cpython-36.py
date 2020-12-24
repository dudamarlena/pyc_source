# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/csv_li.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 295 bytes
import io, csv

def csv_li(txt, verify=None):
    f = io.StringIO(txt)
    reader = csv.reader(f, delimiter=',')
    li = []
    for pos, row in enumerate(reader):
        if not row:
            pass
        else:
            row = verify(row)
            if row:
                li.append(row)

    return li