# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/admin.py
# Compiled at: 2018-03-10 21:58:03
# Size of source mod 2**32: 973 bytes
from django.contrib import admin
from django_geo_db.models import Location, City, Continent, Country, State, GeoCoordinate, UserLocation, County, GeographicRegion, LocationMap, LocationBounds
from django_geo_db.forms import UserLocationForm, LocationForm, CityForm, GeocoordinateForm

class UserLocationAdmin(admin.ModelAdmin):
    form = UserLocationForm


class LocationAdmin(admin.ModelAdmin):
    form = LocationForm


class CityAdmin(admin.ModelAdmin):
    form = CityForm


class GeocoordinateAdmin(admin.ModelAdmin):
    form = GeocoordinateForm


admin.site.register(City, CityAdmin)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(County)
admin.site.register(GeoCoordinate, GeocoordinateAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(GeographicRegion)
admin.site.register(LocationBounds)
admin.site.register(LocationMap)