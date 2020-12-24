# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/staticfiles/templatetags/staticfiles.py
# Compiled at: 2018-07-11 18:15:30
from django import template
from django.templatetags.static import StaticNode
from django.contrib.staticfiles.storage import staticfiles_storage
register = template.Library()

class StaticFilesNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        return staticfiles_storage.url(path)


@register.tag('static')
def do_static(parser, token):
    """
    A template tag that returns the URL to a file
    using staticfiles' storage backend

    Usage::

        {% static path [as varname] %}

    Examples::

        {% static "myapp/css/base.css" %}
        {% static variable_with_path %}
        {% static "myapp/css/base.css" as admin_base_css %}
        {% static variable_with_path as varname %}

    """
    return StaticFilesNode.handle_token(parser, token)


def static(path):
    return staticfiles_storage.url(path)