# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/paulmitchell-gears/git/peoplewise-enable/env/lib/python3.5/site-packages/serialization_spec/utils.py
# Compiled at: 2019-10-22 17:18:03
# Size of source mod 2**32: 296 bytes


def extend_queryset(queryset, fields):
    """ Extend an already-`.only()`d queryset with more fields """
    existing, defer = queryset.query.deferred_loading
    existing_set = set(existing)
    existing_set.update(fields)
    queryset.query.deferred_loading = (frozenset(existing_set), defer)