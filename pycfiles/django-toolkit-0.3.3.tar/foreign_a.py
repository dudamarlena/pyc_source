# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/templatetags/foreign_a.py
# Compiled at: 2014-02-18 18:41:38
import re
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django.template.defaultfilters import truncatechars
register = template.Library()

def base_site_url():
    default_http_protocol = getattr(settings, 'DEFAULT_HTTP_PROTOCOL', 'http')
    current_site = Site.objects.get_current()
    return '%s://%s' % (default_http_protocol, current_site.domain)


@register.filter
def foreign_a(value, include_base=False, text=None):
    if hasattr(value, 'get_absolute_url'):
        if include_base:
            base_url = base_site_url()
        else:
            base_url = ''
        data_tip = ''
        prepend = ''
        if hasattr(value, 'get_data_tip'):
            data_tip = ' data-tip="%s"' % value.get_data_tip()
        if hasattr(value, 'get_append_markup'):
            prepend = value.get_append_markup()
        if text is None:
            text = '%s' % value
        return mark_safe('<a href="%s%s"%s>%s</a>%s' % (base_url, value.get_absolute_url(), data_tip, text, prepend))
    else:
        return mark_safe(value)


def context_processor():
    default_http_protocol = getattr(settings, 'DEFAULT_HTTP_PROTOCOL', 'http')
    current_site = Site.objects.get_current()
    base_url = '%s://%s' % (default_http_protocol, current_site.domain)
    return {'default_http_protocol': default_http_protocol, 
       'current_site': current_site, 
       'base_url': base_url}