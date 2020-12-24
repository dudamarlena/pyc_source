# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Docode\Desktop\Gimbow\DoCode\templatetags\filtros.py
# Compiled at: 2019-11-26 18:05:23
# Size of source mod 2**32: 268 bytes
from django import template
register = template.Library()

@register.filter(name='contenido')
def contenido(registro, campos):
    registros = list()
    for campo in campos:
        registros.append(getattr(registro, campo['nombre']))

    return registros