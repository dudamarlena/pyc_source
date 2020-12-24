# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kentcoble/Documents/workspace/easysnmp/easysnmp/helpers.py
# Compiled at: 2016-04-23 17:04:30
from __future__ import unicode_literals
import re
OID_INDEX_RE = re.compile(b'(\n            \\.?\\d+(?:\\.\\d+)*              # numeric OID\n            |                             # or\n            (?:\\w+(?:[-:]*\\w+)+)          # regular OID\n            |                             # or\n            (?:\\.?iso(?:\\.\\w+[-:]*\\w+)+)  # fully qualified OID\n        )\n        \\.?(.*)                           # OID index\n     ', re.VERBOSE)

def normalize_oid(oid, oid_index=None):
    """
    Ensures that the index is set correctly given an OID definition.

    :param oid: the OID to normalize
    :param oid_index: the OID index to normalize
    """
    if oid_index is None and oid is not None:
        match = OID_INDEX_RE.match(oid)
        if match:
            oid, oid_index = match.group(1, 2)
    return (
     oid, oid_index)