# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/templatetags/wizard_builder.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 878 bytes
from widget_tweaks.templatetags.widget_tweaks import append_attr
from django import template
from django.forms.widgets import ChoiceWidget
register = template.Library()

@register.filter(is_safe=True)
def add_aria_tags_to_field(field):
    attrs = []
    if field.help_text or field.label:
        attrs.append('aria-describedby:help-' + field.id_for_label)
    if field.field.required:
        attrs.append('aria-required:true')
    if field.errors:
        attrs.append('aria-invalid:true')
        attrs.append('aria-describedby:error-' + field.id_for_label)
    for attr in attrs:
        append_attr(field, attr)

    return field


@register.filter(name='is_multiple_choice')
def is_multiple_choice(field):
    return issubclass(field.field.widget.__class__, ChoiceWidget)