# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data/workspace/nst3/env/local/lib/python2.7/site-packages/toffee/templatetags/addcss.py
# Compiled at: 2014-04-15 03:46:19
from django import template
from django.forms import CheckboxInput
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='titlify')
def titlify(field):
    if '__' in field:
        field = field.split('__')[0]
    elif field.lower() == 'id':
        return 'ID'
    return field.replace('_', ' ').title()


@register.filter(name='get_field_type')
def get_field_type(field):
    return field.field.widget.__class__.__name__