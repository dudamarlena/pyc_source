# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/narani/Projects/django-zen-queries/zen_queries/utils.py
# Compiled at: 2020-03-13 12:34:20
# Size of source mod 2**32: 67 bytes


def fetch(queryset):
    queryset._fetch_all()
    return queryset