# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/authorization.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
from tastypie.exceptions import TastypieError, Unauthorized
from tastypie.compat import get_module_name

class Authorization(object):
    """
    A base class that provides no permissions checking.
    """

    def __get__(self, instance, owner):
        """
        Makes ``Authorization`` a descriptor of ``ResourceOptions`` and creates
        a reference to the ``ResourceOptions`` object that may be used by
        methods of ``Authorization``.
        """
        self.resource_meta = instance
        return self

    def apply_limits(self, request, object_list):
        """
        Deprecated.

        FIXME: REMOVE BEFORE 1.0
        """
        raise TastypieError(b'Authorization classes no longer support `apply_limits`. Please update to using `read_list`.')

    def read_list(self, object_list, bundle):
        """
        Returns a list of all the objects a user is allowed to read.

        Should return an empty list if none are allowed.

        Returns the entire list by default.
        """
        return object_list

    def read_detail(self, object_list, bundle):
        """
        Returns either ``True`` if the user is allowed to read the object in
        question or throw ``Unauthorized`` if they are not.

        Returns ``True`` by default.
        """
        return True

    def create_list(self, object_list, bundle):
        """
        Unimplemented, as Tastypie never creates entire new lists, but
        present for consistency & possible extension.
        """
        raise NotImplementedError(b'Tastypie has no way to determine if all objects should be allowed to be created.')

    def create_detail(self, object_list, bundle):
        """
        Returns either ``True`` if the user is allowed to create the object in
        question or throw ``Unauthorized`` if they are not.

        Returns ``True`` by default.
        """
        return True

    def update_list(self, object_list, bundle):
        """
        Returns a list of all the objects a user is allowed to update.

        Should return an empty list if none are allowed.

        Returns the entire list by default.
        """
        return object_list

    def update_detail(self, object_list, bundle):
        """
        Returns either ``True`` if the user is allowed to update the object in
        question or throw ``Unauthorized`` if they are not.

        Returns ``True`` by default.
        """
        return True

    def delete_list(self, object_list, bundle):
        """
        Returns a list of all the objects a user is allowed to delete.

        Should return an empty list if none are allowed.

        Returns the entire list by default.
        """
        return object_list

    def delete_detail(self, object_list, bundle):
        """
        Returns either ``True`` if the user is allowed to delete the object in
        question or throw ``Unauthorized`` if they are not.

        Returns ``True`` by default.
        """
        return True


class ReadOnlyAuthorization(Authorization):
    """
    Default Authentication class for ``Resource`` objects.

    Only allows ``GET`` requests.
    """

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        return []

    def create_detail(self, object_list, bundle):
        raise Unauthorized(b'You are not allowed to access that resource.')

    def update_list(self, object_list, bundle):
        return []

    def update_detail(self, object_list, bundle):
        raise Unauthorized(b'You are not allowed to access that resource.')

    def delete_list(self, object_list, bundle):
        return []

    def delete_detail(self, object_list, bundle):
        raise Unauthorized(b'You are not allowed to access that resource.')


class DjangoAuthorization(Authorization):
    """
    Uses permission checking from ``django.contrib.auth`` to map
    ``POST / PUT / DELETE / PATCH`` to their equivalent Django auth
    permissions.

    Both the list & detail variants simply check the model they're based
    on, as that's all the more granular Django's permission setup gets.
    """

    def base_checks(self, request, model_klass):
        if not model_klass or not getattr(model_klass, b'_meta', None):
            return False
        if not hasattr(request, b'user'):
            return False
        else:
            return model_klass

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        if klass is False:
            return []
        return object_list

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        if klass is False:
            raise Unauthorized(b'You are not allowed to access that resource.')
        return True

    def create_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        if klass is False:
            return []
        permission = b'%s.add_%s' % (
         klass._meta.app_label,
         get_module_name(klass._meta))
        if not bundle.request.user.has_perm(permission):
            return []
        return object_list

    def create_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        if klass is False:
            raise Unauthorized(b'You are not allowed to access that resource.')
        permission = b'%s.add_%s' % (
         klass._meta.app_label,
         get_module_name(klass._meta))
        if not bundle.request.user.has_perm(permission):
            raise Unauthorized(b'You are not allowed to access that resource.')
        return True

    def update_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        if klass is False:
            return []
        permission = b'%s.change_%s' % (
         klass._meta.app_label,
         get_module_name(klass._meta))
        if not bundle.request.user.has_perm(permission):
            return []
        return object_list

    def update_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        if klass is False:
            raise Unauthorized(b'You are not allowed to access that resource.')
        permission = b'%s.change_%s' % (
         klass._meta.app_label,
         get_module_name(klass._meta))
        if not bundle.request.user.has_perm(permission):
            raise Unauthorized(b'You are not allowed to access that resource.')
        return True

    def delete_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        if klass is False:
            return []
        permission = b'%s.delete_%s' % (
         klass._meta.app_label,
         get_module_name(klass._meta))
        if not bundle.request.user.has_perm(permission):
            return []
        return object_list

    def delete_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        if klass is False:
            raise Unauthorized(b'You are not allowed to access that resource.')
        permission = b'%s.delete_%s' % (
         klass._meta.app_label,
         get_module_name(klass._meta))
        if not bundle.request.user.has_perm(permission):
            raise Unauthorized(b'You are not allowed to access that resource.')
        return True