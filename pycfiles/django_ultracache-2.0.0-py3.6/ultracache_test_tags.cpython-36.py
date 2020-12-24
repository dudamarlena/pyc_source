# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/templatetags/ultracache_test_tags.py
# Compiled at: 2018-09-10 07:18:29
# Size of source mod 2**32: 1411 bytes
"""Template tag used in unit tests"""
import re
from django import template
from django.conf import settings
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse, resolve, get_script_prefix
register = template.Library()

@register.tag
def render_view(parser, token):
    """{% render_view view_name %}"""
    tokens = token.split_contents()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError('render_view view_name %}')
    return RenderViewNode(tokens[1])


class RenderViewNode(template.Node):

    def __init__(self, view_name):
        self.view_name = template.Variable(view_name)

    def render(self, context):
        view_name = self.view_name.resolve(context)
        url = reverse(view_name)
        url = re.sub('^%s' % get_script_prefix().rstrip('/'), '', url)
        view, args, kwargs = resolve(url)
        request = context['request']
        result = view(request, *args, **kwargs)
        if isinstance(result, TemplateResponse):
            result.render()
            html = result.rendered_content
        else:
            if isinstance(result, HttpResponse):
                html = result.content
        return html