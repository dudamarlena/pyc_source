# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/api/permissions.py
# Compiled at: 2015-09-15 16:02:15
from rest_framework.permissions import BasePermission

class UserTicketPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class StaffTicketPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff