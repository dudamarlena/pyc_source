# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/views/user.py
# Compiled at: 2017-05-23 10:04:18
# Size of source mod 2**32: 2992 bytes
from ovp_users import serializers
from ovp_users import models
from rest_framework import decorators
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework import permissions
import json

class UserResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n  UserResourceViewSet resource endpoint\n  '
    queryset = models.User.objects.all()
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'

    def current_user_get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset, context=self.get_serializer_context())
        return response.Response(serializer.data)

    def current_user_patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    @decorators.list_route(url_path='current-user', methods=['GET', 'PATCH'])
    def current_user(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.current_user_get(request, *args, **kwargs)
        if request.method == 'PATCH':
            return self.current_user_patch(request, *args, **kwargs)

    def get_object(self):
        request = self.get_serializer_context()['request']
        if self.action == 'current_user':
            return self.get_queryset().get(pk=request.user.pk)
        return super(UserResourceViewSet, self).get_object()

    def get_permissions(self):
        request = self.get_serializer_context()['request']
        if self.action == 'create':
            self.permission_classes = []
        elif self.action in ('current_user', ):
            self.permission_classes = [
             permissions.IsAuthenticated]
        return super(UserResourceViewSet, self).get_permissions()

    def get_serializer_class(self):
        request = self.get_serializer_context()['request']
        if self.action == 'create':
            return serializers.UserCreateSerializer
        if self.action == 'current_user':
            if request.method == 'GET':
                return serializers.CurrentUserSerializer
            if request.method in ('PUT', 'PATCH'):
                pass
            return serializers.UserUpdateSerializer


class PublicUserResourceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n  PublicUserResourceViewSet resource endpoint\n  '
    queryset = models.User.objects.filter(public=True)
    serializer_class = serializers.LongUserPublicRetrieveSerializer
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'