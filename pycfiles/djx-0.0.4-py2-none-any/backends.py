# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/auth/backends.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
UserModel = get_user_model()

class ModelBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, b'is_active', None)
        return is_active or is_active is None

    def _get_user_permissions(self, user_obj):
        return user_obj.user_permissions.all()

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field(b'groups')
        user_groups_query = b'group__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Returns the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        else:
            perm_cache_name = b'_%s_perm_cache' % from_name
            if not hasattr(user_obj, perm_cache_name):
                if user_obj.is_superuser:
                    perms = Permission.objects.all()
                else:
                    perms = getattr(self, b'_get_%s_permissions' % from_name)(user_obj)
                perms = perms.values_list(b'content_type__app_label', b'codename').order_by()
                setattr(user_obj, perm_cache_name, set(b'%s.%s' % (ct, name) for ct, name in perms))
            return getattr(user_obj, perm_cache_name)

    def get_user_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings the user `user_obj` has from their
        `user_permissions`.
        """
        return self._get_permissions(user_obj, obj, b'user')

    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return self._get_permissions(user_obj, obj, b'group')

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        else:
            if not hasattr(user_obj, b'_perm_cache'):
                user_obj._perm_cache = self.get_user_permissions(user_obj)
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
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return

        if self.user_can_authenticate(user):
            return user
        else:
            return


class AllowAllUsersModelBackend(ModelBackend):

    def user_can_authenticate(self, user):
        return True


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

    def authenticate(self, request, remote_user):
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
            if self.create_unknown_user:
                user, created = UserModel._default_manager.get_or_create(**{UserModel.USERNAME_FIELD: username})
                if created:
                    user = self.configure_user(user)
            else:
                try:
                    user = UserModel._default_manager.get_by_natural_key(username)
                except UserModel.DoesNotExist:
                    pass

                if self.user_can_authenticate(user):
                    return user
            return

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


class AllowAllUsersRemoteUserBackend(RemoteUserBackend):

    def user_can_authenticate(self, user):
        return True