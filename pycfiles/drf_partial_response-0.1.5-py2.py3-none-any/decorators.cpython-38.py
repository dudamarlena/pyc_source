# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thongnguyen/training/asoft/thongnguyen/python-tools/drf-partial-response/drf_partial_response/decorators.py
# Compiled at: 2020-03-20 04:00:38
# Size of source mod 2**32: 332 bytes
from __future__ import unicode_literals
from functools import wraps

def data_predicate(*field_names):

    def _data_predicate(fnc):
        fnc._data_function_predicates = field_names

        @wraps(fnc)
        def inner(self, queryset):
            return fnc(self, queryset)

        return inner

    return _data_predicate