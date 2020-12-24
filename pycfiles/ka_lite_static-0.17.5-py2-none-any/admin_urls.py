# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/admin/templatetags/admin_urls.py
# Compiled at: 2018-07-11 18:15:30
from django.core.urlresolvers import reverse
from django import template
from django.contrib.admin.util import quote
register = template.Library()

@register.filter
def admin_urlname(value, arg):
    return 'admin:%s_%s_%s' % (value.app_label, value.module_name, arg)


@register.filter
def admin_urlquote(value):
    return quote(value)