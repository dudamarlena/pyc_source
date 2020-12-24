# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/moment/utils.py
# Compiled at: 2020-04-11 10:31:37
# Size of source mod 2**32: 284 bytes
"""
Added for Python 3 compatibility.
"""
import sys
STRING_TYPES = (basestring,) if sys.version_info < (3, 0) else (str,)

def _iteritems(data):
    """For Python 3 support."""
    if sys.version_info < (3, 0):
        return data.iteritems()
    return data.items()