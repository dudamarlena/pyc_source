# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/templatetags/forward_query_param.py
# Compiled at: 2009-01-30 02:41:09
from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
register = template.Library()

class ForwardQueryParamNode(template.Node):
    __module__ = __name__

    def __init__(self, param_name):
        self.param_name = param_name

    def render(self, context):
        request = None
        try:
            request = context['request']
        except:
            request = context['pagevars'].request

        result = '<div><input type="hidden" name="' + self.param_name + '" value="' + escape(request.GET.get(self.param_name, '')) + '" /></div>'
        return mark_safe(result)


def do_forward_query_param(parser, token):
    """
    Turns a parameter in a query string into a hidden input field,
    allowing it to be 'forwarded' as part of the next request in
    a form submission. It requires one argument (the name of the parameter),
    and also requires that the request object be in the context as 
    directly under the ``request`` name or by putting the standard
    ``pagevars`` object in the context.
    """
    try:
        (tag_name, param_name) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, 'forward_query_param tag requires an argument'

    param_name = param_name.strip('"')
    return ForwardQueryParamNode(param_name)


register.tag('forward_query_param', do_forward_query_param)