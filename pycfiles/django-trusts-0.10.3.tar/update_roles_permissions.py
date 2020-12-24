# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/management/commands/update_roles_permissions.py
# Compiled at: 2016-04-16 22:35:57
from __future__ import unicode_literals
import getpass, unicodedata
from django.conf import settings
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, router
from django.db.models import Q
from django.utils.encoding import DEFAULT_LOCALE_ENCODING
from django.utils import six

def _process_roles(Permission, model_roles, content_klass, roles, using):
    for rolename, perm_names in roles:
        if rolename not in model_roles:
            model_roles[rolename] = set()
        from django.contrib.contenttypes.models import ContentType
        ctype = ContentType.objects.db_manager(using).get_for_model(content_klass)
        model_roles[rolename].update([ Permission.objects.get(content_type=ctype, codename=perm_name) for perm_name in perm_names
                                     ])


def update_roles_permissions(Role, Permission, RolePermission, app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, **kwargs):
    if not router.allow_migrate_model(using, Role):
        return
    try:
        Role = app_config.get_model(b'trusts', b'Role')
    except LookupError:
        return

    model_roles = {}
    for klass in app_config.get_models():
        if hasattr(klass._meta, b'roles'):
            _process_roles(Permission, model_roles, klass, klass._meta.roles, using)
        elif hasattr(klass._meta, b'content_roles'):
            if hasattr(klass, b'get_content_model'):
                content_klass = klass.get_content_model()
                _process_roles(Permission, model_roles, content_klass, klass._meta.content_roles, using)

    db_roles = {}
    for r in Role.objects.using(using).all():
        db_roles[r.name] = set(r.permissions.all())

    model_rolenames = set(model_roles.keys())
    db_rolenames = set(db_roles.keys())
    added_rolenames = model_rolenames - db_rolenames
    deleted_rolenames = db_rolenames - model_rolenames
    existing_rolenames = model_rolenames.intersection(db_rolenames)
    bulk_add_rolepermissions = []
    q_del_rolepermissions = []
    deleted_role_ids = []
    for rolename in added_rolenames:
        r = Role(name=rolename)
        r.save()
        for p in model_roles[rolename]:
            bulk_add_rolepermissions.append(RolePermission(managed=True, permission=p, role=r))

    for rolename in existing_rolenames:
        r = Role.objects.get(name=rolename)
        db_permissions = db_roles[rolename]
        model_permissions = model_roles[rolename]
        added_permissions = set(model_permissions) - set(db_permissions)
        for p in added_permissions:
            bulk_add_rolepermissions.append(RolePermission(managed=True, permission=p, role=r))

        deleted_permissions = set(db_permissions) - set(model_permissions)
        if len(deleted_permissions):
            q_del_rolepermissions.append((r, Q(managed=True, role=r, permission__in=deleted_permissions)))

    for rolename in deleted_rolenames:
        r = Role.objects.get(name=rolename)
        q_del_rolepermissions.append((r, Q(managed=True, role=r)))
        deleted_role_ids.append(r.pk)

    RolePermission.objects.using(using).bulk_create(bulk_add_rolepermissions)
    if verbosity >= 2:
        for rolepermission in bulk_add_rolepermissions:
            print b'Adding role(%s).rolepermission "%s"' % (rolepermission.role.name, rolepermission)

    for r, q in q_del_rolepermissions:
        qs = RolePermission.objects.filter(q)
        if verbosity >= 2:
            if qs.count() > 0:
                for rolepermission in qs.all():
                    print b'Removing role(%s).rolepermission "%s"' % (rolepermission.role.name, rolepermission)

        qs.delete()

    qs = Role.objects.filter(pk__in=deleted_role_ids, permissions__isnull=True)
    if verbosity >= 2:
        if qs.count() > 0:
            for role in qs.all():
                print b'Removing role "%s"' % role.name

    qs.delete()


class Command(BaseCommand):
    help = b"Create Role objects linking to permission defined in models's meta class."

    def handle(self, **options):
        self.verbosity = int(options.get(b'verbosity', 1))
        if b'apps' in options:
            apps = options[b'apps']
            Permission = apps.get_model(b'auth', b'Permission')
            Role = apps.get_model(b'trusts', b'role')
            RolePermission = apps.get_model(b'trusts', b'rolepermission')
            app_config = options[b'apps']
        else:
            from trusts.models import Role, RolePermission
            from django.contrib.auth.models import Permission
            from django.apps import apps as app_config
        update_roles_permissions(Role, Permission, RolePermission, app_config, **options)