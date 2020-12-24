# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/templatetags/rapid_filters.py
# Compiled at: 2015-08-31 20:53:03
__author__ = 'marcos.medeiros'
from django import template
from django.utils.safestring import mark_safe
from django.template import loader, Context
from rapid import filters
register = template.Library()
_base = 'rapid/filters/'

@register.inclusion_tag(_base + 'model_filters.html', takes_context=True)
def model_filters(context, model):
    ff = filters.FilterSet.from_request(model, context.request)
    return {'filters': mark_safe(ff.render_filters(context.request)), 
       'has_filters': ff.has_filters(), 
       'selectors': mark_safe(ff.render_selectors(context.request))}


@register.inclusion_tag(_base + 'register.html', takes_context=True)
def register_filters(context):
    return {}


@register.simple_tag(takes_context=True)
def filter_icon(context, field):
    if filters.FilterSet.can_filter(field):
        c = Context({'f': field})
        t = loader.get_template(_base + 'icon.html')
        return mark_safe(t.render(c))
    return ''