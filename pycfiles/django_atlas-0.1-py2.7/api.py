# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/api.py
# Compiled at: 2015-04-21 15:30:03
import heapq
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from django.conf import settings
from django.shortcuts import get_object_or_404
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from atlas.models import Country, Region, City, Location

class CountryResource(ModelResource):

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        excludes = ('border', )
        allowed_methods = ['get']
        filtering = {'country_code': ('exact', ), 
           'id': ('exact', )}


class RegionResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country')

    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'
        allowed_methods = ['get']
        filtering = {'id': ('exact', ), 
           'code': ('exact', ), 
           'country': ALL_WITH_RELATIONS}


class CityResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country')
    region = fields.ForeignKey(RegionResource, 'region')

    class Meta:
        queryset = City.objects.all()
        resource_name = 'city'
        allowed_methods = ['get']
        filtering = {'id': ('exact', ), 
           'country': ALL_WITH_RELATIONS, 
           'region': ALL_WITH_RELATIONS}


class LocationResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country')
    city = fields.ForeignKey(CityResource, 'city', null=True)

    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
        allowed_methods = ['get']
        filtering = {'country': ALL_WITH_RELATIONS, 
           'city': ALL_WITH_RELATIONS, 
           'coordinates': ('distance_lte', ), 
           'id': ('exact', )}
        max_limit = 20
        excludes = ('id', )
        default_format = 'application/json'

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        filters.pop('city', None)
        orm_filters = super(LocationResource, self).build_filters(filters)
        return orm_filters

    def get_object_list(self, request):
        qs = super(LocationResource, self).get_object_list(request)
        point = None
        if 'location' in request.GET:
            lon, lat = request.GET['location'].split(' ')
            point = fromstr('POINT (%s %s)' % (lon, lat), srid=4326)
        elif 'city' in request.GET:
            point = get_object_or_404(City, id=request.GET['city']).coordinates
        if point is not None:
            if settings.DATABASES['default']['ENGINE'].rfind('mysql') == -1:
                qs = qs.distance(point).order_by('distance')
            else:
                qs = qs.exclude(coordinates__isnull=True).extra(select={'distance': "distance_sphere(`atlas_location`.`coordinates`, geomfromtext('%s', %d))" % (
                              str(point), point.srid)}).order_by('distance')
        return qs

    def dehydrate_country(self, bundle):
        if bundle.obj.country:
            c = bundle.obj.country
            return {'name': c.name, 'country_code': c.country_code}
        else:
            return

    def dehydrate_city(self, bundle):
        if bundle.obj.city:
            return bundle.obj.city.name
        else:
            return

    def dehydrate_coordinates(self, bundle):
        if bundle.obj.coordinates:
            c = bundle.obj.coordinates
            return {'longitude': c.x, 'latitude': c.y}
        else:
            return

    def dehydrate(self, bundle):
        if bundle.obj.photo:
            bundle.data['photo_uri'] = bundle.obj.photo.get_location_thumbnail_smart_url()
        return bundle