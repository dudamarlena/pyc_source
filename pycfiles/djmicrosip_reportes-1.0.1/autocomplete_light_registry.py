# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reportes\djmicrosip_reportes\autocomplete_light_registry.py
# Compiled at: 2016-06-24 19:12:38
import autocomplete_light
from django_microsip_base.libs.models_base.models import LineaArticulos
autocomplete_light.register(LineaArticulos, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Linea', 'class': 'form-control'}, choices=LineaArticulos.objects.all(), name='LineaArticulosAutocomplete')