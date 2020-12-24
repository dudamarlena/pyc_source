# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/julio.rama/git/vault-opensource/vault/templatetags/dashboard_tags.py
# Compiled at: 2020-03-17 15:36:47
# Size of source mod 2**32: 594 bytes
from django import template
from django.apps import apps
from django.conf import settings
register = template.Library()

@register.simple_tag(takes_context=True)
def info_endpoints(context, **kwargs):
    """Templatetag to render a list of info endpoints"""
    endpoints = []
    request = context.get('request')
    project_name = request.session.get('project_name')
    for conf in apps.get_app_configs():
        if hasattr(conf, 'vault_app'):
            endpoints.append("'/p/{}/{}/api/info'".format(project_name, conf.name))

    return ','.join(endpoints)