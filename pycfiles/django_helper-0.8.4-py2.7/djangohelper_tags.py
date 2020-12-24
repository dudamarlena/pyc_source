# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djangohelper/templatetags/djangohelper_tags.py
# Compiled at: 2012-10-31 05:15:39
from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def getvars(request, excludes):
    getvars = request.GET.copy()
    excludes = excludes.split(',')
    for p in excludes:
        if p in getvars:
            del getvars[p]
        if len(getvars.keys()) > 0:
            return '&%s' % getvars.urlencode()
        return ''


@register.simple_tag(takes_context=True)
def get_setting(context, key, default_val='', as_key=None):
    """ 
    get val form settings and set to context
      {% load djangohelper_tags %}
      {% get_setting "key" default_val "as_key" %}
      {{ as_key }}
      if as_key is None, this tag will return val
    """
    if ('%s' % default_val).startswith('$.'):
        default_val = getattr(settings, default_val[2:])
    val = getattr(settings, key, default_val)
    if not as_key:
        return val
    context[as_key] = val
    return ''