# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/views.py
# Compiled at: 2019-06-28 12:15:36
# Size of source mod 2**32: 922 bytes
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from .utils import get_device_model
from .serializers import DeviceSerializer

class CreateDeleteDeviceView(CreateAPIView, DestroyModelMixin):
    __doc__ = '\n    An endpoint for creating & deleting devices.\n    '
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        instance.invalidate()

    def delete(self, request, *args, **kwargs):
        return (self.destroy)(request, *args, **kwargs)

    def get_object(self):
        """
        Override get_object for delete endpoint
        """
        device_model = get_device_model()
        return get_object_or_404((device_model._default_manager), push_token=(self.request.data.get('push_token')), user=(self.request.user))