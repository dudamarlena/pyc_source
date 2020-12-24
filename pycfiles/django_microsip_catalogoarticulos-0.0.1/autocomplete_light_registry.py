# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_microsip_catalogoarticulos\django_microsip_catalogoarticulos\autocomplete_light_registry.py
# Compiled at: 2014-10-15 12:19:38
from .models import Tag, Articulo
import autocomplete_light
autocomplete_light.register(Tag, search_fields=('tag', ), autocomplete_js_attributes={'placeholder': 'Tag ..', 'class': 'form-control'})