# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizas\djmicrosip_polizas\autocomplete_light_registry.py
# Compiled at: 2016-04-13 11:53:07
from .models import ContabilidadCuentaContable
import autocomplete_light
autocomplete_light.register(ContabilidadCuentaContable, search_fields=('cuenta', 'nombre'), autocomplete_js_attributes={'placeholder': 'Cuenta ..'})