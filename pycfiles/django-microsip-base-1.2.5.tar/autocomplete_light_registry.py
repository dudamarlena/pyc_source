# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\django_microsip_base\apps\main\autocomplete_light_registry.py
# Compiled at: 2020-02-13 19:27:53
from django_microsip_base.libs.models_base.models import Cliente, Articulo, Clasificadores, ClasificadoresValores, ElementosClasificadores, GrupoLineas, LineaArticulos
import autocomplete_light
autocomplete_light.register(Cliente, search_fields=('nombre', 'contacto1'), autocomplete_js_attributes={'placeholder': 'Cliente ..', 'class': 'form-control'})
autocomplete_light.register(Articulo, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Articulo ..', 'class': 'form-control'})
autocomplete_light.register(Clasificadores, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Clasificador ..', 'class': 'form-control'})
autocomplete_light.register(ClasificadoresValores, search_fields=('valor', ), autocomplete_js_attributes={'placeholder': 'Valor clasificadores ..', 'class': 'form-control'})