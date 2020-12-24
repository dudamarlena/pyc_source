# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/dev_reactor/django-reactor/reactor/templatetags.py
# Compiled at: 2019-10-10 12:05:59
# Size of source mod 2**32: 3091 bytes
""" Reactor Navigation Template Tags
"""
import re
from django import forms, template
from django.template.loader import get_template
from django.urls import NoReverseMatch, reverse
register = template.Library()

@register.simple_tag(takes_context=True)
def active_nav(context, paths_or_urlnames, css_class='active'):
    try:
        pattern = '^' + reverse(paths_or_urlnames) + '$'
    except NoReverseMatch:
        pattern = paths_or_urlnames

    if re.fullmatch(pattern, context['request'].path):
        return css_class
    return ''


@register.filter
def bootstrap_form(element, layout=None):
    label_class = 'sr-only' if layout == 'inline' else ''
    markup_classes = {'label':label_class,  'value':'',  'single_value':''}
    return render_form(element, markup_classes)


@register.filter
def is_checkbox_input(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox_input(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_date_input(field):
    return isinstance(field.field.widget, forms.widgets.SelectDateWidget)


@register.filter
def is_radio_input(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file_input(field):
    return isinstance(field.field.widget, forms.FileInput)


def add_input_classes(field):
    field_classes = field.field.widget.attrs.get('class', '')
    if not is_checkbox_input(field):
        if not is_multiple_checkbox_input(field):
            if not is_radio_input(field):
                if not is_file_input(field):
                    field_classes += ' form-control'
    if is_file_input(field):
        field_classes += ' custom-file-input'
    if is_checkbox_input(field) or is_radio_input(field) or is_multiple_checkbox_input(field):
        field_classes += ' form-check-input'
    if field.errors:
        field_classes += ' is-invalid'
    field.field.widget.attrs['class'] = field_classes


def render_form(element, markup_classes):
    element_type = element.__class__.__name__.lower()
    if element_type == 'boundfield':
        add_input_classes(element)
        field_template = get_template('reactor/forms/field.html')
        context = dict({'field':element,  'classes':markup_classes})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            field_template = get_template('reactor/forms/formset.html')
            context = dict({'formset':element,  'classes':markup_classes})
        else:
            for field in element.visible_fields():
                add_input_classes(field)

            field_template = get_template('reactor/forms/default.html')
            context = dict({'form':element,  'classes':markup_classes})
    return field_template.render(context)