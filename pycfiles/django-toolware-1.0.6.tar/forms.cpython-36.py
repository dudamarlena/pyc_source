# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/templatetags/forms.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 1940 bytes
import copy, operator
from django import template
from django import forms
from django.utils.datastructures import SortedDict
register = template.Library()

class FieldSetNode(template.Node):
    __doc__ = ' Returns a subset of given form '

    def __init__(self, opcode, fields, orig_form, new_form):
        self.opcode = opcode
        self.fields = fields
        self.orig_form = orig_form
        self.new_form = new_form

    def render(self, context):
        oform = template.Variable(self.orig_form).resolve(context)
        nform = copy.copy(oform)
        if 'fields' in self.opcode:
            nform.fields = SortedDict([(key, oform.fields[key]) for key in oform.fields if key in self.fields])
        if 'exclude' in self.opcode:
            nform.fields = SortedDict([(key, oform.fields[key]) for key in oform.fields if key not in self.fields])
        context[self.new_form] = nform
        return ''


@register.tag
def trim_form(parser, token):
    """
        Returns a form that only contains a subset of the original fields (opcode: incude/exclude fields)
        Exampel:
            <fieldset>
                <legend>Business Info</legend>
                <ul>
                {% trim_form orig_form fields biz_name,biz_city,biz_email,biz_phone as new_form %}
                {{ new_form.as_ul }}
                </ul>
            </fieldset>
            OR:
            <fieldset>
                <legend>Business Info</legend>
                <ul>
                {% trim_form orig_form exclude biz_country,biz_url as new_form %}
                {{ new_form.as_ul }}
                </ul>
            </fieldset>
    """
    try:
        trim_form, orig_form, opcode, fields, as_, new_form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('Invalid arguments for %r' % token.split_contents()[0])

    return FieldSetNode(opcode, fields.split(','), orig_form, new_form)