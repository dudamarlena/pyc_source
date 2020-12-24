# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_faexist\djmicrosip_faexist\autocomplete_light_registry.py
# Compiled at: 2015-01-15 14:54:02
import autocomplete_light
from django_microsip_base.libs.models_base.models import LineaArticulos
autocomplete_light.register(LineaArticulos, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Linea ..', 'class': 'form-control'}, choices=LineaArticulos.objects.all(), name='LineaArticulosAutocomplete')