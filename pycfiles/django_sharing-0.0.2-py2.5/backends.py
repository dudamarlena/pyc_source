# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sharing/backends.py
# Compiled at: 2010-09-23 04:50:36
from django.contrib.contenttypes.models import ContentType
from sharing.models import GroupShare, UserShare

class SharingBackend(object):
    """
    Authentication backend providing row level permissions.
    """
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        """
        Required by Django, does nothing.
        """
        return

    def has_perm(self, user_obj, perm, obj=None):
        """
        Checks whether or not the given user or her groups has the given 
        permission for the given object. 
        """
        if obj is None:
            return False
        if not user_obj.is_authenticated():
            return False
        try:
            perm = 'can_%s' % perm.split('.')[(-1)].split('_')[0]
        except IndexError:
            return False

        content_type = ContentType.objects.get_for_model(obj)
        user_shares = UserShare.objects.filter(content_type=content_type, object_id=obj.id, user=user_obj)
        if user_shares.filter(**{perm: True}).exists():
            return True
        group_shares = GroupShare.objects.filter(content_type=content_type, object_id=obj.id, group__in=user_obj.groups.all())
        if group_shares.filter(**{perm: True}).exists():
            return True
        return False