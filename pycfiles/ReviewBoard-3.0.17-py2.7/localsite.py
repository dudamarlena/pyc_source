# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/site/templatetags/localsite.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import template
from django.core.urlresolvers import NoReverseMatch, ViewDoesNotExist
from django.template.defaulttags import url as django_url
register = template.Library()

class LocalSiteURLNode(template.Node):

    def __init__(self, url_node):
        self.url_node = url_node
        self.args = list(url_node.args)
        self.kwargs = url_node.kwargs.copy()

    def render(self, context):
        local_site_name = context.get(b'local_site_name', None)
        if local_site_name:
            local_site_var = template.Variable(b'local_site_name')
            if self.args:
                self.url_node.args = [
                 local_site_var] + self.args
            else:
                self.url_node.kwargs[b'local_site_name'] = local_site_var
            try:
                return self.url_node.render(context)
            except (NoReverseMatch, ViewDoesNotExist):
                pass

        self.url_node.args = list(self.args)
        self.url_node.kwargs = self.kwargs.copy()
        return self.url_node.render(context)


@register.tag
def url(parser, token):
    return LocalSiteURLNode(django_url(parser, token))