# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_sms\django_msp_sms\autocomplete_light_registry.py
# Compiled at: 2015-10-19 12:15:01
from .models import *
import autocomplete_light
from django.db.models import Q
autocomplete_light.register(Cliente, name='ClienteManyAutocomplete', search_fields=('nombre', ), choices=Cliente.objects.filter(Q(no_enviar_sms=None) | Q(no_enviar_sms=0)), autocomplete_js_attributes={'placeholder': 'Busca un cliente... '}, widget_js_attributes={'max_values': 20})