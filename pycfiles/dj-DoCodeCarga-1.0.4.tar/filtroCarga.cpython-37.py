# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Docode\Desktop\Gimbow\DoCodeCarga\templatetags\filtroCarga.py
# Compiled at: 2020-01-07 15:39:06
# Size of source mod 2**32: 207 bytes
from django import template
register = template.Library()

@register.filter(name='filtro')
def filtro(registro):
    registros = list()
    return registros