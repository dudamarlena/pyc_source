# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/queryset/lookups.py
# Compiled at: 2015-07-01 01:59:56
from __future__ import absolute_import, division, print_function, unicode_literals
COMPARISON_OPERATORS = ('gt', 'gte', 'lt', 'lte', 'in')
LOOKUP_SEP = b'__'

def convert_lookups(**query):
    """
    Transform a query from Django-style format to Datasore format.

    :return: An iterable of filters suitable to pass to :meth:`~gcloudoem.datastore.query.Query.add_filter`.
    """
    filters = []
    for key, value in sorted(query.items()):
        parts = key.rsplit(LOOKUP_SEP)
        parts = [ part for part in parts if not part.isdigit() ]
        op = b'eq'
        if len(parts) > 1 and parts[(-1)] in COMPARISON_OPERATORS:
            op = parts.pop()
        if parts[0] == b'pk':
            parts[0] = b'key'
        filters.append((parts[0], op, value))

    return filters