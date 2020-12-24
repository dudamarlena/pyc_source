# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/social/backends.py
# Compiled at: 2011-08-22 06:58:14
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from social.constants import SOCIAL_GROUPS
from social.models import SocialObjectPermission, SocialObjectFieldPermission, resolve_is_member_method

class SocialObjectPermissionBackend(object):
    """
    Authentication backend providing a social permissions system, 
    i.e. which users (friends included) can access another's content.
    """
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        """
        We don't care about authentication here, so return None.
        """
        return

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user has access to object based on social permissions.
        """
        if obj is None:
            return False
        else:
            content_type = ContentType.objects.get_for_model(obj)
            try:
                perm = perm.split('.')[(-1)].split('_')[0]
            except IndexError:
                return False
            else:
                target_user = obj.target_user
                perms = SocialObjectPermission.objects.filter(content_type=content_type, user=target_user).filter(**{'can_%s' % perm: True})
                perms = perms.order_by('social_group')
                for perm in perms:
                    return perm.is_member(target_user=target_user, requesting_user=user_obj)

            try:
                default_social_group = settings.DEFAULT_SOCIAL_PERMISSION_GROUP
                return resolve_is_member_method(SOCIAL_GROUPS[default_social_group][1])(target_user=target_user, requesting_user=user_obj)
            except AttributeError:
                raise ImproperlyConfigured('settings should provide a DEFAULT_SOCIAL_PERMISSION_GROUP.')

            return


class SocialObjectFieldPermissionBackend(object):
    """
    Authentication backend providing a social permissions system, 
    i.e. which users (friends included) can access another's content.
    """
    supports_field_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        """
        We don't care about authentication here, so return None.
        """
        return

    def has_field_perm(self, user_obj, perm, obj=None, field=None):
        """
        Check if user has access to object based on social permissions.
        """
        if field is None or obj is None:
            return False
        else:
            content_type = ContentType.objects.get_for_model(obj)
            try:
                perm = perm.split('.')[(-1)].split('_')[0]
            except IndexError:
                return False
            else:
                target_user = obj.target_user
                perms = SocialObjectFieldPermission.objects.filter(content_type=content_type, field_name=field.name, user=target_user).filter(**{'can_%s' % perm: True})
                perms = perms.order_by('social_group')
                for perm in perms:
                    return perm.is_member(target_user=target_user, requesting_user=user_obj)

            try:
                default_social_group = settings.DEFAULT_SOCIAL_PERMISSION_GROUP
                return resolve_is_member_method(SOCIAL_GROUPS[default_social_group][1])(target_user=target_user, requesting_user=user_obj)
            except AttributeError:
                raise ImproperlyConfigured('settings should provide a DEFAULT_SOCIAL_PERMISSION_GROUP.')

            return