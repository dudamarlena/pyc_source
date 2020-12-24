# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/templatetags/sentry_react.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django import template
from sentry.utils import json
from sentry.web.client_config import get_client_config
register = template.Library()

@register.simple_tag(takes_context=True)
def get_react_config(context):
    context = get_client_config(context.get('request', None))
    return json.dumps_htmlsafe(context)