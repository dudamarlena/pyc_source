# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/templatetags/user_admin_url.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 628 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

templatetags/admin_url.py - Very simple template tag allow linking to the
                            right auth user model urls.

{% url 'changelist'|user_admin_url %}
"""
from django import template
from django.contrib.auth import get_user_model

def user_admin_url(action):
    user = get_user_model()
    return 'admin:%s_%s_%s' % (
     user._meta.app_label, user._meta.model_name.lower(),
     action)


register = template.Library()
register.filter(user_admin_url)