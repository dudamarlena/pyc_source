# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_diot\django_microsip_diot\autocomplete_light_registry.py
# Compiled at: 2015-11-24 14:59:04
from .models import Ciudad, ContabilidadCuentaContable, Pais, Proveedor
from django.db.models import F
import autocomplete_light
autocomplete_light.register(Proveedor, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Proveedor...', 'class': 'form-control'})
autocomplete_light.register(Ciudad, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Ciudad...', 'class': 'form-control'})
autocomplete_light.register(Pais, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Pais...', 'class': 'form-control'})
autocomplete_light.register(ContabilidadCuentaContable, search_fields=('cuenta', 'nombre'), autocomplete_js_attributes={'placeholder': 'Cuenta ..'})
autocomplete_light.register(ContabilidadCuentaContable, search_fields=('cuenta', 'nombre'), autocomplete_js_attributes={'placeholder': 'Cuenta ..'}, choices=ContabilidadCuentaContable.objects.filter(id=F('cuenta_padre')), name='ContabilidadCuentaContableAutocompleteMayor')