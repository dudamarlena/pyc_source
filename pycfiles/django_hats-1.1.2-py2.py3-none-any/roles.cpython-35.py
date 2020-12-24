# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/roles.py
# Compiled at: 2017-07-02 03:10:32
# Size of source mod 2**32: 4194 bytes
import six
from django.contrib.auth.models import Group, Permission
from django_hats.bootstrap import Bootstrapper
from django_hats.utils import snake_case

class RoleMetaClass(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(RoleMetaClass, cls).__new__(cls, name, bases, attrs)
        if bases and Role in bases:
            super_new._meta = type('Meta', (), {})
            super_new._meta.permissions = ()
            if hasattr(super_new, 'Meta'):
                for attr in [attr for attr in dir(super_new.Meta) if not callable(attr) and not attr.startswith('__')]:
                    setattr(super_new._meta, attr, getattr(super_new.Meta, attr))

            Bootstrapper.register(super_new)
        return super_new


class Role(six.with_metaclass(RoleMetaClass)):
    group = None

    @classmethod
    def add_permissions(cls, *args):
        return cls.get_group().permissions.add(*args)

    @classmethod
    def remove_permissions(cls, *args):
        return cls.get_group().permissions.remove(*args)

    @classmethod
    def check_membership(cls, user):
        return user.groups.filter(id=cls.get_group().id).exists()

    @classmethod
    def get_users(cls):
        group = cls.get_group()
        return group.user_set.all()

    @classmethod
    def get_group(cls):
        if cls.group is None:
            cls.group, _ = Group.objects.get_or_create(name='%s%s' % (Bootstrapper.prefix, cls.get_slug()))
        return cls.group

    @classmethod
    def get_permissions(cls):
        permissions = cls.get_group().permissions.all()
        return permissions

    @classmethod
    def assign(cls, *users):
        group = cls.get_group()
        group.user_set.add(*users)

    @classmethod
    def remove(cls, *users):
        group = cls.get_group()
        group.user_set.remove(*users)

    @classmethod
    def get_slug(cls):
        return (getattr(cls._meta, 'name', None) or snake_case(cls.__name__)).lower()

    @classmethod
    def synchronize(cls):
        cls.add_permissions(*Permission.objects.filter(codename__in=cls._meta.permissions))
        perms_to_remove = []
        for perm in cls.get_permissions():
            if perm.codename not in cls._meta.permissions:
                perms_to_remove.append(perm)

        cls.remove_permissions(*perms_to_remove)


class RoleFinder(object):

    @staticmethod
    def by_name(name):
        """Returns single `Role` where snake case name matches the given string `name`.
        """
        return Bootstrapper._available_roles.get(name, None)

    @staticmethod
    def by_group(group):
        """Returns single `Role` which `group` corresponds with.
        """
        return RoleFinder.by_name(group.name.replace(Bootstrapper.prefix, ''))

    @staticmethod
    def by_user(user):
        """Returns list of `Roles` which belong to a given `User`.
        """
        roles = []
        for group in user.groups.filter(name__istartswith=Bootstrapper.prefix):
            role = RoleFinder.by_group(group)
            if role is not None:
                roles.append(role)

        return roles