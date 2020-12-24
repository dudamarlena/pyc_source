# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/users/viewsets.py
# Compiled at: 2016-10-26 05:12:13
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_extras.users.permissions import UserPermissions
from rest_framework_extras.users.serializers import UserSerializerForSuperUser, UserSerializerForStaff, UserSerializerForUser

class UsersViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (UserPermissions,)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser:
            return UserSerializerForSuperUser
        if user.is_staff:
            return UserSerializerForStaff
        return UserSerializerForUser