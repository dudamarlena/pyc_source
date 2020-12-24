# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/templatetags/djtools_form_tags.py
# Compiled at: 2017-01-21 12:36:57
import copy
from collections import OrderedDict
from django import forms
from django import template
from django.template.loader import render_to_string
register = template.Library()

@register.filter
def quick_form(form, template='djtools/quick_form.html'):
    return render_to_string(template, {'form': form})


class FieldSetNode(template.Node):

    def __init__(self, fields, variable_name, form):
        self.fields = fields
        self.variable_name = variable_name
        self.form = form

    def render(self, context):
        form = template.Variable(self.form).resolve(context)
        new_form = copy.copy(form)
        new_form.fields = OrderedDict([ (key, value) for key, value in form.fields.items() if key in self.fields
                                      ])
        context[self.variable_name] = new_form
        return ''


@register.tag
def get_fieldset(parser, token):
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)