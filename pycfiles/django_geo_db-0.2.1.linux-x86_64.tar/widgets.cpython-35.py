# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/widgets.py
# Compiled at: 2018-02-13 09:27:30
# Size of source mod 2**32: 573 bytes
from django import forms
from django.conf import settings
from django.template.loader import render_to_string

class GeocoordinateWidget(forms.TextInput):
    template_name = 'django_geo_db/geocoordinate.html'
    css = {'all': ('styles.css', )}

    def render(self, name, value, attrs=None):
        context = {'name': name, 
         'value': value, 
         'GM_SETTINGS': settings.GM_SETTINGS, 
         'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
        return render_to_string(self.template_name, context)