# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/views/devices/devices.py
# Compiled at: 2019-10-28 01:58:06
# Size of source mod 2**32: 2987 bytes
from __future__ import unicode_literals
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from irekua_database import models
from irekua_rest_api import filters
from irekua_rest_api import utils
from irekua_rest_api import serializers
from irekua_rest_api.permissions import IsAdmin
from irekua_rest_api.permissions import IsAuthenticated

class DeviceViewSet(utils.CustomViewSetMixin, ModelViewSet):
    queryset = models.Device.objects.all()
    filterset_class = filters.devices.Filter
    search_fields = filters.devices.search_fields
    serializer_mapping = utils.SerializerMapping.from_module(serializers.devices.devices).extend(types=(serializers.object_types.devices.ListSerializer),
      add_type=(serializers.object_types.devices.CreateSerializer),
      brands=(serializers.devices.brands.ListSerializer),
      add_brand=(serializers.devices.brands.CreateSerializer),
      physical_devices=(serializers.devices.physical_devices.ListSerializer),
      add_physical_device=(serializers.devices.physical_devices.CreateSerializer))
    permission_mapping = utils.PermissionMapping({utils.Actions.UPDATE: IsAdmin, 
     utils.Actions.DESTROY: IsAdmin, 
     'add_type': IsAdmin},
      default=IsAuthenticated)

    def get_queryset(self):
        if self.action == 'types':
            return models.DeviceType.objects.all()
        if self.action == 'brands':
            return models.DeviceBrand.objects.all()
        if self.action == 'physical_devices':
            return models.PhysicalDevice.objects.all()
        return super().get_queryset()

    @action(detail=False,
      methods=[
     'GET'],
      filterset_class=(filters.device_types.Filter),
      search_fields=(filters.device_types.search_fields))
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(detail=False,
      methods=[
     'GET'],
      filterset_class=(filters.device_brands.Filter),
      search_fields=(filters.device_brands.search_fields))
    def brands(self, request):
        return self.list_related_object_view()

    @brands.mapping.post
    def add_brand(self, request):
        return self.create_related_object_view()

    @action(detail=False,
      methods=[
     'GET'],
      filterset_class=(filters.physical_devices.Filter),
      search_fields=(filters.physical_devices.search_fields))
    def physical_devices(self, request):
        return self.list_related_object_view()

    @physical_devices.mapping.post
    def add_physical_device(self, request):
        return self.create_related_object_view()