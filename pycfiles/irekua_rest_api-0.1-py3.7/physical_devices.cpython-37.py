# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/views/devices/physical_devices.py
# Compiled at: 2019-10-28 01:58:06
# Size of source mod 2**32: 987 bytes
from __future__ import unicode_literals
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from irekua_database import models
from irekua_rest_api import utils
from irekua_rest_api import serializers
from irekua_rest_api.permissions import IsAdmin
import irekua_rest_api.permissions as permissions
from irekua_rest_api.permissions import ReadOnly

class PhysicalDeviceViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, utils.CustomViewSetMixin, GenericViewSet):
    queryset = models.PhysicalDevice.objects.all()
    serializer_mapping = utils.SerializerMapping.from_module(serializers.devices.physical_devices)
    permission_mapping = utils.PermissionMapping(default=(permissions.IsOwner | IsAdmin | ReadOnly))