# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/silica/django_app/templatetags/silica.py
# Compiled at: 2017-05-11 17:20:40
# Size of source mod 2**32: 4789 bytes
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html, mark_safe
from django.forms import DateField, DateTimeField, ModelChoiceField, ModelMultipleChoiceField
from django.db import models
import json
register = template.Library()

@register.filter(name='getattr')
def template_getattr(obj, attr_name):
    return getattr(obj, attr_name)


@register.filter(name='getitem')
def template_getitem(obj, item_name):
    return obj[item_name]


@register.filter(name='title_space')
@stringfilter
def title_space(string):
    return string.replace('_', ' ').title()


@register.filter(name='get_django_field')
def template_get_django_field(obj, field):
    val = getattr(obj, field)
    if field in obj.get_many_to_many_fields():
        return val.all()
    else:
        return val


@register.simple_tag(name='angular_model')
def angular_model(model, angular_model_name, extra_params={}):
    """ Returns javascript that preprocesses obj before attaching it to window
        where angular controller can grab it """
    ret = '<script>\n'
    if model is None:
        ret += 'window.%s = {};\n' % angular_model_name
    else:
        json_ret = model.to_json()
        model_dict = json.loads(json_ret)
        fk_fields = model.get_foreign_key_fields()
        m2m_fields = model.get_many_to_many_fields()
        for field, val in model_dict['fields'].iteritems():
            if field in fk_fields:
                model_dict['fields'][field] = str(val)
            if field in m2m_fields:
                model_dict['fields'][field] = map(str, val)

        ret += 'window.%s = %s;\n' % (angular_model_name, json.dumps(model_dict))
        for field in model.READABLE_ATTRS(type_filter=(models.DateField)):
            ret += 'window.%s.fields.%s = new Date(window.%s.fields.%s);\n' % (
             angular_model_name, field, angular_model_name, field)

    ret += '</script>\n'
    return mark_safe(ret)


@register.simple_tag(name='angular_input_field')
def angular_input_field(form_field, angular_model_name, extra_params={}):
    try:
        form_field_value = form_field.value
        form_field.value = lambda : None
        attrs = {'ng-model':'%s.fields.%s' % (angular_model_name, form_field.name),  'class':'form-control'}
        if form_field.field.required:
            attrs['required'] = 'true'
        attrs.update(extra_params)
        return format_html(form_field.as_widget(attrs=attrs))
    finally:
        form_field.value = form_field_value


def _get_datepicker(form_field, attrs, extra_params):
    attrs = dict(attrs)
    calendar_button = extra_params.pop('silica_calendar_button', True)
    attrs['placeholder'] = 'yyyy-mm-dd'
    attrs['uib-datepicker-popup'] = ''
    attrs['datepicker-options'] = 'dateOptions'
    attrs['is-open'] = '_calendar_widgets[%s]' % id(form_field)
    attrs['ng-click'] = '_calendar_widgets[%s]=true' % id(form_field)
    attrs.update(extra_params)
    ret = form_field.as_widget(attrs=attrs)
    if calendar_button:
        ret = '<div class="input-group">' + ret
        ret += '<span class="input-group-btn"><button type="button" class="btn btn-default" ng-click="_calendar_widgets[%s]=true">\n                  <i class="glyphicon glyphicon-calendar"></i></button></span>' % id(form_field)
        ret += '</div>'
    return ret