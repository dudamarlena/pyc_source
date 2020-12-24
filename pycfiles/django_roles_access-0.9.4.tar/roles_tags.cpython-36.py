# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vicente/Documents/trabajo/desarrollos/roles/django_roles_access/django_roles_access/templatetags/roles_tags.py
# Compiled at: 2019-03-19 09:24:36
# Size of source mod 2**32: 761 bytes
from django import template
from django_roles_access.models import TemplateAccess
register = template.Library()

@register.filter(name='check_role')
def check_role(user, flag):
    """
    **flag** is a unique string used to restrict access by role in template
    content. With **flag** is recover an :class:`roles.models.TemplateAccess`
    object.

    :param flag: :attribute:`roles.models.TemplateAccess.flag`.
    :param user:
    :return:
    """
    try:
        if user.is_superuser:
            return True
        template_flag = TemplateAccess.objects.get(flag__exact=flag)
        for group in user.groups.all():
            if group in template_flag.roles.all():
                return True

        return False
    except:
        return False