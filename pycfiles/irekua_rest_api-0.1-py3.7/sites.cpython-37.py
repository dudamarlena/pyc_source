# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/views/sites.py
# Compiled at: 2019-10-28 02:00:01
# Size of source mod 2**32: 2314 bytes
from __future__ import unicode_literals
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from irekua_database import models
from irekua_rest_api import serializers
from irekua_rest_api import filters
from irekua_rest_api import utils
from irekua_rest_api.permissions import IsAuthenticated
from irekua_rest_api.permissions import IsAdmin
import irekua_rest_api.permissions.sites as permissions

class SiteViewSet(utils.CustomViewSetMixin, ModelViewSet):
    queryset = models.Site.objects.all()
    filterset_class = filters.sites.Filter
    search_fields = filters.sites.search_fields
    serializer_mapping = utils.SerializerMapping.from_module(serializers.sites).extend(types=(serializers.object_types.sites.ListSerializer),
      add_type=(serializers.object_types.sites.CreateSerializer))
    permission_mapping = utils.PermissionMapping({utils.Actions.UPDATE: [
                            IsAuthenticated,
                            permissions.IsCreator | IsAdmin], 
     
     utils.Actions.DESTROY: [
                             IsAuthenticated,
                             permissions.IsCreator | IsAdmin], 
     
     'add_type': [IsAuthenticated, IsAdmin]},
      default=IsAuthenticated)

    def get_serializer_class(self):
        if self.action == utils.Actions.RETRIEVE:
            user = self.request.user
            site = self.get_object()
            if site.has_coordinate_permission(user):
                return serializers.sites.FullDetailSerializer
            return serializers.sites.DetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == 'types':
            return models.SiteType.objects.all()
        return super().get_queryset()

    @action(detail=False,
      methods=[
     'GET'],
      filterset_class=(filters.site_types.Filter),
      search_fields=(filters.site_types.search_fields))
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()