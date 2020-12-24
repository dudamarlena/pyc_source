# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/notifications/api/views.py
# Compiled at: 2020-01-31 08:32:40
# Size of source mod 2**32: 2652 bytes
import datetime
from rest_framework import filters
from rest_framework import mixins, serializers, viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import UserNotification, Notification
from .serializers import UserNotificationSerializer, UserNotificationPutSerializer, NotificationSerializer

class UserNotificationViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserNotification.objects.filter(Q(notification__expires=None) | Q(notification__expires__gte=(datetime.datetime.now()))).order_by('-id')
    permission_classes = (
     permissions.IsAuthenticated,)
    filter_backends = (
     filters.SearchFilter, DjangoFilterBackend)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            serializer_class = UserNotificationPutSerializer
        else:
            serializer_class = UserNotificationSerializer
        return serializer_class

    def list(self, request):
        queryset = self.queryset.filter(user=(self.request.user)).exclude(answer=True).prefetch_related('notification', 'user')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user != request.user:
            raise serializers.ValidationError('User can only change his own usernotifications')
        serializer = self.get_serializer(instance, data=(request.data), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class NotificationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.all()
    permission_classes = (
     permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    serializer_class = NotificationSerializer

    def list(self, request):
        queryset = Notification.objects.filter()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)