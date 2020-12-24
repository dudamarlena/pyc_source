# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/comparator/exceptions.py
# Compiled at: 2018-11-07 11:43:18
"""
    Exception classes specific to comparator
"""

class QueryFormatError(Exception):
    pass


class InvalidCompSetException(Exception):
    pass