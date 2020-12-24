# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/views/users/roles.py
# Compiled at: 2019-10-28 01:58:06
# Size of source mod 2**32: 1449 bytes
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import utils
from irekua_rest_api.permissions import ReadOnly
from irekua_rest_api.permissions import IsAdmin

class RoleViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, utils.CustomViewSetMixin, GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_mapping = utils.SerializerMapping.from_module(serializers.users.roles).extend(add_permission=(serializers.users.roles.SelectPermissionSerializer),
      remove_permission=(serializers.users.roles.SelectPermissionSerializer))
    permission_mapping = utils.PermissionMapping(default=(IsAdmin | ReadOnly))

    @action(detail=True, methods=['POST'])
    def add_permission(self, request, pk=None):
        return self.add_related_object_view(Permission, 'permission')

    @action(detail=True, methods=['POST'])
    def remove_permission(self, request, pk=None):
        return self.remove_related_object_view('permission')