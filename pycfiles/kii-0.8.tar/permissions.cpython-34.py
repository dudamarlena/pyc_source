# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/permissions.py
# Compiled at: 2014-12-31 04:01:41
# Size of source mod 2**32: 314 bytes
from rest_framework import permissions

class IsCommentModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Return `True` if `request.user` is owner of object's subject,
        `False` otherwise.
        """
        return obj.subject.owner == request.user