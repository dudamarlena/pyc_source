# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cclarke/Dropbox/Development/django-foundation-formtags/foundation_formtags/templatetags/foundation_formtags.py
# Compiled at: 2017-10-04 02:04:46
import types
from django import template
from django.conf import settings
from django.template.loader import get_template
from django.forms import CheckboxInput
register = template.Library()
FOUNDATION_FORMTAGS_USE_OPTIONAL = getattr(settings, 'FOUNDATION_FORMTAGS_USE_OPTIONAL', False)

@register.filter
def as_foundation(form):
    template = get_template('foundation_formtags/form.html')
    c = {'form': form, 'use_optional': FOUNDATION_FORMTAGS_USE_OPTIONAL}
    return template.render(c)


@register.inclusion_tag('foundation_formtags/foundation_form_field.html')
def render_field(field):
    """
    Use this need tag to get more control over the layout of your forms
    {% raw %}{% render_field form.my_field %} {% endraw %}
    """
    return {'field': field}


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


def silence_without_field(fn):

    def wrapped(field, attr):
        if not field:
            return ''
        return fn(field, attr)

    return wrapped


def _process_field_attributes(field, attr, process):
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter('append_attr')
@silence_without_field
def append_attr(field, attr):

    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter('add_class')
@silence_without_field
def add_class(field, css_class):
    return append_attr(field, 'class:' + css_class)


@register.filter('add_error_class')
@silence_without_field
def add_error_class(field, css_class):
    if hasattr(field, 'errors') and field.errors:
        return add_class(field, css_class)
    return field