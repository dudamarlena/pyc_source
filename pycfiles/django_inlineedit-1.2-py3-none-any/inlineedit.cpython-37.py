# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\pedro\OneDrive\dev\github\django-inlineedit\inlineedit\templatetags\inlineedit.py
# Compiled at: 2020-05-09 01:54:13
# Size of source mod 2**32: 2700 bytes
from uuid import uuid4
from django.template.library import Library
from django.template.exceptions import TemplateSyntaxError
from django.urls import reverse
from django.forms.widgets import HiddenInput
from django import forms
from ..apps import InlineeditConfig
from ..adaptors import _get_adaptor_class_
register = Library()

@register.simple_tag()
def inlineedit_access(user, model, field):
    return check_access(user, model, field)


@register.inclusion_tag('inlineedit/default_bevahiour.html', takes_context=False)
def inlineedit_script():
    return {'inlineedit_endpoint': reverse(':'.join([InlineeditConfig.name, 'inlineedit']))}


@register.inclusion_tag('inlineedit/extendable.html', takes_context=True)
def inlineedit(context, field_info, adaptor='basic', *args, **kwargs):
    try:
        splits = tuple(field_info.split('.'))
        field_name = splits[(-1)]
    except ValueError:
        raise TemplateSyntaxError('inlineedit invalid argument "{}": must be of the form "model.field"'.format(field_info))

    user = context['request'].user
    object_model = context[splits[0]]
    for s in splits[1:-1]:
        object_model = getattr(object_model, s)

    model_name = object_model._meta.label
    field = object_model._meta.get_field(field_name)
    adaptor_class = _get_adaptor_class_(adaptor)
    adaptor_obj = adaptor_class(object_model, field, user, *args, **kwargs)
    uuid = uuid4().hex
    context.request.session[uuid] = '{}.{}.{}.{}'.format(model_name, field_name, object_model.pk, adaptor)

    class _InlineeditForm(forms.Form):
        uuid = forms.fields.CharField(max_length=32, widget=(HiddenInput()))
        field = adaptor_obj.form_field()

    form = _InlineeditForm({'field':adaptor_obj.db_value(), 
     'uuid':uuid},
      auto_id=(field_info.replace('.', '__') + '__%s'))
    template_name = kwargs['template'] if 'template' in kwargs else 'inlineedit/default.html'
    value = adaptor_obj.display_value()
    empty_msg = '' if value else adaptor_obj.empty_message()
    perm = adaptor_obj.has_edit_perm(user)
    return {'uuid':uuid, 
     'form':form, 
     'value':value, 
     'empty_message':empty_msg, 
     'adaptor':adaptor, 
     'has_edit_perm':perm, 
     'template_name':template_name}