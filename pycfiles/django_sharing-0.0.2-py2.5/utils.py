# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sharing/utils.py
# Compiled at: 2010-09-29 02:10:18


def limit_queryset_by_permission(qs, perm, user):
    """
    Filter queryset by user permission.
    """
    filtered_object_ids = []
    for obj in qs:
        if obj == user:
            filtered_object_ids.append(obj.id)
            continue
        if user.has_perm(perm, obj):
            filtered_object_ids.append(obj.id)

    return qs.filter(id__in=filtered_object_ids)