# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/backends.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

class ModelBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return

        return

    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if user_obj.is_anonymous() or obj is not None:
            return set()
        else:
            if not hasattr(user_obj, b'_group_perm_cache'):
                if user_obj.is_superuser:
                    perms = Permission.objects.all()
                else:
                    user_groups_field = get_user_model()._meta.get_field(b'groups')
                    user_groups_query = b'group__%s' % user_groups_field.related_query_name()
                    perms = Permission.objects.filter(**{user_groups_query: user_obj})
                perms = perms.values_list(b'content_type__app_label', b'codename').order_by()
                user_obj._group_perm_cache = set([ b'%s.%s' % (ct, name) for ct, name in perms ])
            return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous() or obj is not None:
            return set()
        else:
            if not hasattr(user_obj, b'_perm_cache'):
                user_obj._perm_cache = set([ b'%s.%s' % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related() ])
                user_obj._perm_cache.update(self.get_group_permissions(user_obj))
            return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        if not user_obj.is_active:
            return False
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index(b'.')] == app_label:
                return True

        return False

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return

        return


class RemoteUserBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """
    create_unknown_user = True

    def authenticate(self, remote_user):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not remote_user:
            return
        else:
            user = None
            username = self.clean_username(remote_user)
            UserModel = get_user_model()
            if self.create_unknown_user:
                user, created = UserModel.objects.get_or_create(**{UserModel.USERNAME_FIELD: username})
                if created:
                    user = self.configure_user(user)
            else:
                try:
                    user = UserModel.objects.get_by_natural_key(username)
                except UserModel.DoesNotExist:
                    pass

            return user

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.

        By default, returns the username unchanged.
        """
        return username

    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        return user