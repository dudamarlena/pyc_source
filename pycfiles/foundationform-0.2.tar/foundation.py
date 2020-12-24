# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/testzurbform/foundationform/templatetags/foundation.py
# Compiled at: 2014-02-15 22:43:35
from django.template import Context
from django.template.loader import get_template
from django.template import Library
register = Library()

def get_context_template(element):
    element_type = element.__class__.__name__.lower()
    if element_type == 'boundfield':
        template = get_template('foundationform/_foundation_form_field.html')
        context = Context({'field': element})
    elif hasattr(element, 'management_form'):
        template = get_template('foundationform/foundation_formset.html')
        context = Context({'formset': element})
    else:
        template = get_template('foundationform/foundation_form.html')
        context = Context({'form': element})
    return (
     template, context)


@register.filter
def foundation(element):
    template, context = get_context_template(element)
    return template.render(context)


@register.filter
def foundationinline(element):
    template, context = get_context_template(element)
    context.update({'inline': True})
    return template.render(context)