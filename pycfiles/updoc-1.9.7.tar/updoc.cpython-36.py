# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Updoc/updoc/templatetags/updoc.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 894 bytes
from urllib import parse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django import template
from django.template.defaultfilters import floatformat
register = template.Library()

@register.filter
def si_unit(value, unit=''):
    if value is None:
        return ''
    else:
        sign = ''
        if value < 0:
            sign = '-'
            value = -value
        prefix = ''
        if 1.0 > value > 0.0:
            for prefix in ('', 'm', 'µ', 'n', 'p', 'f', 'a', 'z'):
                if value > 1.0:
                    break
                value *= 1000.0

        else:
            for prefix in ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z'):
                if value < 1000.0:
                    break
                value /= 1000.0

        return '%s%s %s%s' % (sign, floatformat(value, -2), prefix, _(unit))


@register.filter()
def quote_feed(value):
    return mark_safe(parse.quote_plus(value))