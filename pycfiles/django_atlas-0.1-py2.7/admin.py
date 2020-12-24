# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/admin.py
# Compiled at: 2015-04-21 15:30:03
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import LineString
from atlas.models import Location, City, Country, Region
from atlas.utils import get_city

class LocationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LocationAdminForm, self).__init__(*args, **kwargs)
        self.fields['country'].required = False

    def clean(self, *args, **kwargs):
        cd = super(LocationAdminForm, self).clean(*args, **kwargs)
        if not cd.get('country', None) or cd['country'] != cd['city'].country:
            cd['country'] = cd['city'].country
        return cd

    def check_consistency(self, cleaned_data):
        if cleaned_data['city'].country != cleaned_data['country']:
            return (False, "The location's city and country do not match.")
        if cleaned_data['coordinates']:
            line = LineString(cleaned_data['coordinates'], cleaned_data['city'].coordinates, srid=4326)
            line.transform(53031)
            if line.length > 500000:
                return (False, "The location's coordinates are more than 500km away from its city.")
        return (
         True, '')


class SearchByNameAdmin(admin.ModelAdmin):
    search_fields = [
     'name']


class LocationAdmin(SearchByNameAdmin):
    form = LocationAdminForm


admin.site.register(Location, LocationAdmin)
admin.site.register(City, SearchByNameAdmin)
admin.site.register(Country, SearchByNameAdmin)
admin.site.register(Region, SearchByNameAdmin)