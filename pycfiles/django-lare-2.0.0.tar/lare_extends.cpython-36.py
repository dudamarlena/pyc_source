# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonasbraun/Coding/iekadou/django-lare/django_lare/templatetags/lare_extends.py
# Compiled at: 2016-06-18 05:54:39
# Size of source mod 2**32: 2511 bytes
from django.conf import settings
from django.template.base import TemplateSyntaxError, FilterExpression
from django.template import Library
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode
register = Library()

class LareExtendsNode(ExtendsNode):

    def __init__(self, nodelist, parent_name, lare_namespace, lare_template, template_dirs=None):
        super(LareExtendsNode, self).__init__(nodelist, parent_name, template_dirs=template_dirs)
        self.lare_namespace = lare_namespace
        self.lare_template = lare_template

    def __repr__(self):
        return '<LareExtendsNode: extends %s>' % self.parent_name.token

    def get_parent(self, context):
        lare_context = dict((k, v) for d in context.dicts for k, v in d.items())
        lare = lare_context.get('lare', False)
        if lare:
            if lare.is_enabled():
                if lare.matches(self.lare_namespace.resolve(context)):
                    self.parent_name = self.lare_template
        return super(LareExtendsNode, self).get_parent(context)


@register.tag()
def lare_extends(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        if len(bits) != 3:
            if len(bits) != 2:
                raise TemplateSyntaxError("'%s' takes 1 - 3 arguments" % bits[0])
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(LareExtendsNode) or nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError("'lare_extends' and 'extends' cannot appear more than once in the same template!")
    if len(bits) > 2:
        try:
            lare_template = parser.compile_filter(bits[3]) if len(bits) == 4 else FilterExpression("'{0}'".format(settings.DEFAULT_LARE_TEMPLATE), parser)
        except AttributeError:
            raise TemplateSyntaxError('No lare template set, even no default!')

        return LareExtendsNode(nodelist, parser.compile_filter(bits[1]), parser.compile_filter(bits[2]), lare_template)
    else:
        return ExtendsNode(nodelist, parser.compile_filter(bits[1]))