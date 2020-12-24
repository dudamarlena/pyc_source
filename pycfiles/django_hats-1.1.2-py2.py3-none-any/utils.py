# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/utils.py
# Compiled at: 2017-11-19 12:06:11
import re
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django_hats.bootstrap import Bootstrapper

def check_membership(user, roles, any=False):
    """Returns membership of all/any of the specified roles for a given `User`.
    """
    try:
        roles = iter(roles)
    except TypeError:
        roles = [
         roles]

    slugs = [ '%s%s' % (Bootstrapper.prefix, role.get_slug()) for role in roles ]
    queryset = user.groups.filter(name__in=slugs)
    if any is False:
        return queryset.count() == len(slugs)
    return queryset.exists()


def migrate_role(old_group, new_role):
    users = old_group.user_set.all()
    new_role.assign(*users)
    old_group.user_set.remove(*users)


def cleanup_roles():
    roles = Bootstrapper.get_roles()
    stale_roles = Group.objects.filter(name__istartswith=Bootstrapper.prefix).exclude(id__in=[ role.get_group().id for role in roles ]).delete()
    return stale_roles


def synchronize_roles(roles):
    ContentType.objects.get_or_create(app_label='roles', model='role')
    for role in roles:
        role.synchronize()


def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', name)
    return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower()