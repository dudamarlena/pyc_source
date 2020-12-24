# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/templatetags/mycms_tags.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 2915 bytes
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template
import re
register = template.Library()
from . import registry
script_str_re_obj = re.compile('(?P<name>src|type)="(?P<value>.*)"|((?P<name2>priority)=(?P<value2>(\\d*)))', re.DOTALL)

@register.inclusion_tag('mycms/templatetags/file_upload.html')
def file_upload():
    return {'none': None}


@register.inclusion_tag('mycms/templatetags/article_editor.html')
def article_editor():
    return {'none': None}


class NullNode(template.Node):

    def __init__(self):
        pass

    def render(self, context):
        return ''


@register.simple_tag(takes_context=True)
def Script(context, *args, **kwargs):
    isLoggedIn = kwargs.get('isLoggedIn', False)
    src = kwargs.get('src', None)
    if kwargs.get('src', None) is not None:
        if isLoggedIn:
            view_object = context['view_object']
            if not view_object.request.user.is_authenticated():
                return ''
        registry.register(src=(kwargs.get('src', '/dummy/path')), type=(kwargs.get('type', 'text/javascript')),
          priority=(kwargs.get('priority', 9999)))
    else:
        print('skipped {}'.format(token_str))
        return ''


class ScriptCollectorNode(template.Node):

    def __init__(self):
        pass

    def __repr__(self):
        return '<ScriptCollectorNode>'

    def render(self, context):
        return registry.html()


@register.tag
def ScriptCollector(parser, token_str):
    return ScriptCollectorNode()


class NullNode(template.Node):

    def __init__(self):
        pass

    def render(self, context):
        return ''


@register.tag
def Link(parser, token_str):
    """
    Adds a <link> for our css at the header of the page.   
    """

    def parse_tokens(tokens):
        tokens = token_str.split_contents()
        tokens = tokens[1:]