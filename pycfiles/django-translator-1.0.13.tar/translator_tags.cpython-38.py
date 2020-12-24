# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christianschuermann/Documents/Repositories/django-translator/translator/templatetags/translator_tags.py
# Compiled at: 2020-01-22 10:12:27
# Size of source mod 2**32: 734 bytes
from django import template
from django.template import Template
from translator.util import get_translation_for_key
register = template.Library()

class VariableRenderingNode(template.Node):

    def __init__(self, some_key):
        self.translation_key = template.Variable(some_key)

    def render(self, context):
        translation_for_key = get_translation_for_key(self.translation_key.resolve(context))
        return Template(translation_for_key).render(context)


def render_variable(parser, token):
    tag_name, variable_value = token.split_contents()
    return VariableRenderingNode(variable_value)


register.tag('render_translation', render_variable)