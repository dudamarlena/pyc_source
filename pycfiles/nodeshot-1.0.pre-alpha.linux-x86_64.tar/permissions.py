# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/net/permissions.py
# Compiled at: 2013-08-25 11:51:18
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        action = ''
        if request.method in ('PUT', 'PATCH'):
            action = 'change'
        elif request.method in ('DELETE', ):
            action = 'delete'
        elif request.method == 'POST':
            action = 'add'
        class_name = obj.__class__.__name__
        return obj.owner == request.user or request.user.has_perm('net.%s_%s' % (action, class_name.lower()))