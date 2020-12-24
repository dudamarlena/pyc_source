# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_mail\djmicrosip_mail\autocomplete_light_registry.py
# Compiled at: 2019-12-02 13:48:11
from .models import *
import autocomplete_light
from django.db.models import Q
autocomplete_light.register(Cliente, name='ClienteManyAutocomplete', search_fields=('nombre', ), choices=Cliente.objects.all(), autocomplete_js_attributes={'placeholder': 'Busca un cliente... '}, widget_js_attributes={'max_values': 20})