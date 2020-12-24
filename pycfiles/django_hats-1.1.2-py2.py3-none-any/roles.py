# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/templatetags/roles.py
# Compiled at: 2016-07-25 16:50:55
import six
from django import template
from django_hats.roles import RoleFinder
register = template.Library()

@register.filter
def has_role(user, role):
    if isinstance(role, six.string_types):
        role = RoleFinder.by_name(role)
    return role.check_membership(user)