# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsilva/Proyectos/django-cfdi/cfdi/templatetags/cfdi_tags.py
# Compiled at: 2020-04-03 14:20:13
# Size of source mod 2**32: 1381 bytes
from django import template
from django.conf import settings
import pytz, time
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def escape(string):
    from cfdi.classes import escape as escapeCfdi
    return escapeCfdi(string)


@register.simple_tag
def set_field(field, value):
    """
        Agrega el campo al XML según el valor de dicho
        campo en la clase CFDI.
    """
    from cfdi.classes import escape as escapeCfdi
    if value == '' or value is None:
        return ''
    else:
        return mark_safe('%s="%s" ' % (field, escapeCfdi(value)))


@register.filter
def iso_date(fecha, timezone):
    """
    Recibe la fecha y la cambia a la zona horaria establecida.
    """
    if settings.USE_TZ:
        timezoneLocal = pytz.timezone(timezone)
        return fecha.astimezone(timezoneLocal).strftime('%Y-%m-%dT%H:%M:%S')
    else:
        iso_tuple = (
         fecha.year, fecha.month, fecha.day,
         fecha.hour, fecha.minute, fecha.second,
         0, 0, 0)
        return time.strftime('%Y-%m-%dT%H:%M:%S', iso_tuple)


@register.filter
def cur(value):
    from django.contrib.humanize.templatetags.humanize import intcomma
    from cfdi.functions import to_precision_decimales
    if value == '':
        return ''
    else:
        return intcomma('%s' % to_precision_decimales(value, 2))