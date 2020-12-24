# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\autocomplete_light_registry.py
# Compiled at: 2019-09-17 20:13:05
import autocomplete_light
from django_microsip_base.libs.models_base.models import Cliente, Articulo
autocomplete_light.register(Articulo, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Articulo ..', 'class': 'form-control'}, choices=Articulo.objects.filter(seguimiento='N', estatus='A', es_almacenable='S'), name='ArticuloNormalAutocomplete')
autocomplete_light.register(Articulo, search_fields=('nombre', ), autocomplete_js_attributes={'placeholder': 'Articulo de series..', 'class': 'form-control'}, choices=Articulo.objects.filter(seguimiento='S', estatus='A', es_almacenable='S'), name='ArticuloSerieAutocomplete')