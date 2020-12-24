# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/django_sortable/helpers.py
# Compiled at: 2012-04-12 19:40:47
from sortable import Sortable

def sortable_helper(request, objects, fields=None):
    """Helper used to make sortable slightly less verbose."""
    field_name = request.GET.get('sort', None)
    direction = request.GET.get('dir', 'asc')
    if not field_name:
        return objects
    else:
        sortable = Sortable(objects, fields)
        return sortable.sorted(field_name, direction)