# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-licyilu1/django-cbr/cbr/templatetags/cbr.py
# Compiled at: 2017-08-28 23:32:16
# Size of source mod 2**32: 447 bytes
from django import template
from cbr.models import CBRCurrencyRate
register = template.Library()

@register.inclusion_tag('cbr/informer.html', takes_context=True)
def currency_informer(context):
    usd = CBRCurrencyRate.objects.filter(currency__char_code='USD').last()
    eur = CBRCurrencyRate.objects.filter(currency__char_code='EUR').last()
    return {'request': context['request'], 
     'usd': usd, 
     'eur': eur}