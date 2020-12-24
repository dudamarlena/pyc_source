# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/form_renderers/monkey.py
# Compiled at: 2017-05-03 06:55:45
from __future__ import unicode_literals
import inspect, logging
from django.forms import BaseForm
from django.forms.widgets import Widget
HAS_CHOICE_INPUT = True
try:
    from django.forms.widgets import ChoiceInput
except ImportError:
    HAS_CHOICE_INPUT = False

try:
    from django.forms.boundfield import BoundField
except ImportError:
    from django.forms.forms import BoundField

from django.utils.html import format_html
from django.utils.module_loading import import_module
from django.conf import settings
from form_renderers import SETTINGS, as_div
logger = logging.getLogger(b'logger')

def decorate_a(meth):

    def decorator(context, *args, **kwargs):
        di = meth(context, *args, **kwargs)
        if context.is_required:
            di[b'required'] = b'required'
        if b'class' not in di:
            di[b'class'] = b''
        di[b'class'] = di[b'class'] + b' ' + context.__class__.__name__ + b' '
        return di

    return decorator


logger.info(b'Patching Widget.build_attrs')
Widget.build_attrs = decorate_a(Widget.build_attrs)

def decorate_b(meth):

    def decorator(context, *args, **kwargs):
        result = meth(context, *args, **kwargs)
        result += b' Form-item Field %s ' % context.field.__class__.__name__
        if context.field.widget.is_required:
            result += b' Field--required '
        return result

    return decorator


if SETTINGS[b'enable-bem-classes']:
    logger.info(b'Patching BoundField.css_classes')
    BoundField.css_classes = decorate_b(BoundField.css_classes)

def decorate_c(meth):

    def decorator(context, contents=None, attrs=None, label_suffix=None):
        if attrs is None:
            attrs = {b'class': b''}
        if b'class' in attrs:
            attrs[b'class'] += b' '
        else:
            attrs[b'class'] = b''
        attrs[b'class'] += b'Field-label'
        return meth(context, contents, attrs, label_suffix)

    return decorator


if SETTINGS[b'enable-bem-classes']:
    logger.info(b'Patching BoundField.label_tag')
    BoundField.label_tag = decorate_c(BoundField.label_tag)

def my_render(self, name=None, value=None, attrs=None, choices=()):
    if hasattr(self, b'id_for_label'):
        if self.id_for_label:
            label_for = format_html(b' for="{}"', self.id_for_label)
        else:
            label_for = b''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        return format_html(b'<label{}>{} <span class="{}-label">{}</span></label>', label_for, self.tag(attrs), attrs[b'class'], self.choice_label)
    else:
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if b'id' in self.attrs:
            label_for = format_html(b' for="{0}_{1}"', self.attrs[b'id'], self.index)
        else:
            label_for = b''
        return format_html(b'<label{0}>{1} <span class="{2}-label">{3}</span></label>', label_for, self.tag(), attrs[b'class'], self.choice_label)


if HAS_CHOICE_INPUT:
    logger.info(b'Patching ChoiceInput.render')
    ChoiceInput.render = my_render
logger.info(b'Adding BaseForm.as_div')
BaseForm.as_div = as_div
if SETTINGS[b'replace-as-p']:
    BaseForm.as_p = as_div
if SETTINGS[b'replace-as-table']:
    BaseForm.as_table = as_div
for app_name in reversed(settings.INSTALLED_APPS):
    try:
        module = import_module(app_name + b'.form_renderers')
    except ImportError:
        continue

    for name, func in inspect.getmembers(module, inspect.isfunction):
        logger.info(b'Adding BaseForm.%s' % name)
        setattr(BaseForm, name, func)