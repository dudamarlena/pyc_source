# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/site/context_processors.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.contrib.auth.context_processors import PermLookupDict, PermWrapper
from django.utils import six
from reviewboard.site.models import LocalSite

class AllPermsLookupDict(PermLookupDict):

    def __init__(self, user, app_label, perms_wrapper):
        super(AllPermsLookupDict, self).__init__(user, app_label)
        self.perms_wrapper = perms_wrapper

    def __repr__(self):
        return six.text_type(self.user.get_all_permissions(self.perms_wrapper.get_local_site()))

    def __getitem__(self, perm_name):
        return self.user.has_perm(b'%s.%s' % (self.app_label, perm_name), self.perms_wrapper.get_local_site())

    def __nonzero__(self):
        return super(AllPermsLookupDict, self).__nonzero__()

    def __bool__(self):
        return super(AllPermsLookupDict, self).__bool__()


class AllPermsWrapper(PermWrapper):

    def __init__(self, user, local_site_name):
        super(AllPermsWrapper, self).__init__(user)
        self.local_site_name = local_site_name
        self.local_site = None
        return

    def __getitem__(self, app_label):
        return AllPermsLookupDict(self.user, app_label, self)

    def get_local_site(self):
        if self.local_site_name is None:
            return
        else:
            if not self.local_site:
                self.local_site = LocalSite.objects.get(name=self.local_site_name)
            return self.local_site


def localsite(request):
    """Returns context variables useful to Local Sites.

    This provides the name of the Local Site (``local_site_name``), and
    a permissions variable used for accessing user permissions (``perm``).

    ``perm`` overrides the permissions provided by the Django auth framework.
    These permissions cover Local Sites along with the standard global
    permissions.
    """
    local_site_name = getattr(request, b'_local_site_name', None)
    return {b'local_site_name': local_site_name, 
       b'perms': AllPermsWrapper(request.user, local_site_name)}