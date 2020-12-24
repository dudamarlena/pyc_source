# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/cristiandulcey/Documents/trabajo/cato/libros_cristal/libros/lib/python2.7/site-packages/cdmetro/templatetags/filtros_metro.py
# Compiled at: 2016-05-26 00:04:30
from django import template
from django.db.models.loading import get_models, get_model
import humanize
register = template.Library()

@register.simple_tag
def valor_field(id, valor, aplicacion, modelo):
    mymodel = get_model(app_label=aplicacion, model_name=modelo)
    val_aux = mymodel.objects.filter(id=id).values_list(valor, flat=True)
    if str(val_aux[0]) == 'False':
        return '<a class="btn btn-primary red" ><i class="halflings-icon white remove-sign"></i></a>'
    else:
        if str(val_aux[0]) == 'True':
            return '<a class="btn green" ><i class="halflings-icon white ok-sign"></i></a>'
        return val_aux[0]


@register.filter(name='access')
def access(value, arg):
    return value[arg]


@register.filter(name='filtros')
def filtros(value, arg):
    if arg == 'intcomma':
        value = humanize.intcomma(value)
    return value