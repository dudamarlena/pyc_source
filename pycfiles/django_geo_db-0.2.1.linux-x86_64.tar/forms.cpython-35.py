# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/forms.py
# Compiled at: 2018-02-11 12:08:49
# Size of source mod 2**32: 1346 bytes
from django import forms
from dal.autocomplete import ModelSelect2
from django_geo_db.models import UserLocation, City, Location, GeoCoordinate
from django_geo_db.widgets import GeocoordinateWidget

class GeocoordinateForm(forms.ModelForm):

    class Meta:
        model = GeoCoordinate
        fields = [
         'generated_name',
         'lat',
         'lon']
        widgets = {'generated_name': GeocoordinateWidget}


class UserLocationForm(forms.ModelForm):

    class Meta:
        model = UserLocation
        widgets = {'location': ModelSelect2(url='location-autocomplete')}
        fields = '__all__'


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        widgets = {'zipcode': ModelSelect2(url='zipcode-autocomplete'), 
         'city': ModelSelect2(url='city-autocomplete'), 
         'county': ModelSelect2(url='county-autocomplete'), 
         'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete')}
        fields = '__all__'


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        widgets = {'zipcode': ModelSelect2(url='zipcode-autocomplete'), 
         'county': ModelSelect2(url='county-autocomplete')}
        fields = '__all__'