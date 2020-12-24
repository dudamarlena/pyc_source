# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/slava/myprojects/cbr/django_weather_darksky/templatetags/django_weather_darksky.py
# Compiled at: 2017-03-21 22:29:51
# Size of source mod 2**32: 718 bytes
from django import template
from django_weather_darksky.models import WeatherForecast
from django_weather_darksky.helpers import format_temperature as format_temp
register = template.Library()

@register.inclusion_tag('django_weather_darksky/informer.html', takes_context=True)
def weather_current(context, location):
    """
    Current weather informer
    """
    data = WeatherForecast.objects.filter(location__slug=location, forecast_type='currently').last()
    return {'data': data}


@register.filter
def format_temperature(value, units='C'):
    """
    Filter format temperature
    """
    try:
        res = format_temp(value, units)
    except ValueError:
        res = ''

    return res