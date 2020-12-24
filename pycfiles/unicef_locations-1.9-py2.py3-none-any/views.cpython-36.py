# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/views.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 3077 bytes
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.generics import ListAPIView
from .cache import etag_cached
from .models import CartoDBTable, GatewayType, Location
from .serializers import CartoDBTableSerializer, GatewayTypeSerializer, LocationLightSerializer, LocationSerializer

class CartoDBTablesView(ListAPIView):
    __doc__ = '\n    Gets a list of CartoDB tables for the mapping system\n    '
    queryset = CartoDBTable.objects.all()
    serializer_class = CartoDBTableSerializer


class LocationTypesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n    Returns a list off all Location types\n    '
    queryset = GatewayType.objects.all()
    serializer_class = GatewayTypeSerializer


class LocationsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n    CRUD for Locations\n    '
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @etag_cached('locations')
    def list(self, request, *args, **kwargs):
        return (super(LocationsViewSet, self).list)(request, *args, **kwargs)

    def get_object(self):
        if 'p_code' in self.kwargs:
            obj = get_object_or_404((self.get_queryset()), p_code=(self.kwargs['p_code']))
            self.check_object_permissions(self.request, obj)
            return obj
        else:
            return super(LocationsViewSet, self).get_object()

    def get_queryset(self):
        queryset = Location.objects.all()
        if 'values' in self.request.query_params.keys():
            try:
                ids = [int(x) for x in self.request.query_params.get('values').split(',')]
            except ValueError:
                raise ValidationError('ID values must be integers')
            else:
                queryset = queryset.filter(id__in=ids)
        return queryset


class LocationsLightViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n    Returns a list of all Locations with restricted field set.\n    '
    queryset = Location.objects.defer('geom')
    serializer_class = LocationLightSerializer

    @etag_cached('locations')
    def list(self, request, *args, **kwargs):
        return (super(LocationsLightViewSet, self).list)(request, *args, **kwargs)


class LocationQuerySetView(ListAPIView):
    model = Location
    serializer_class = LocationLightSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q')
        qs = self.model.objects.defer('geom')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs.all()[:7]