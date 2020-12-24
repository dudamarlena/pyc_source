# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freegenes/utils/convert.py
# Compiled at: 2019-09-24 12:48:26
# Size of source mod 2**32: 640 bytes
"""

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from freegenes.logger import bot
from io import StringIO
import csv

def str2csv(string, newline='\n', delim=','):
    """given a string with csv content, read in as csv and return rows,
       with the header in the first row.
    """
    rows = []
    reader = csv.reader((string.split(newline)), delimiter=delim)
    for row in reader:
        if row:
            rows.append(row)

    return rows