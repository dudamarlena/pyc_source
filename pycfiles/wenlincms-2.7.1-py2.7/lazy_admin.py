# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/boot/lazy_admin.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib.admin.sites import AdminSite
from wenlincms.utils.importing import import_dotted_path

class LazyAdminSite(AdminSite):
    """
    Defers calls to register/unregister until autodiscover is called
    to avoid load issues with injectable model fields defined by
    ``settings.EXTRA_MODEL_FIELDS``.
    """

    def __init__(self, *args, **kwargs):
        self._deferred = []
        super(LazyAdminSite, self).__init__(*args, **kwargs)

    def register(self, *args, **kwargs):
        for name, deferred_args, deferred_kwargs in self._deferred:
            if name == b'unregister' and deferred_args[0] == args[0]:
                self._deferred.append((b'register', args, kwargs))
                break
        else:
            super(LazyAdminSite, self).register(*args, **kwargs)

    def unregister(self, *args, **kwargs):
        self._deferred.append((b'unregister', args, kwargs))

    def lazy_registration(self):
        for name, deferred_args, deferred_kwargs in self._deferred:
            getattr(AdminSite, name)(self, *deferred_args, **deferred_kwargs)

    @property
    def urls(self):
        from django.conf import settings
        urls = patterns(b'', (b'', super(LazyAdminSite, self).urls))
        fb_name = getattr(settings, b'PACKAGE_NAME_FILEBROWSER', b'')
        if fb_name in settings.INSTALLED_APPS:
            try:
                fb_urls = import_dotted_path(b'%s.sites.site' % fb_name).urls
            except ImportError:
                fb_urls = b'%s.urls' % fb_name

            urls = patterns(b'', (b'^media-library/', include(fb_urls))) + urls
        for admin in self._registry.values():
            user_change_password = getattr(admin, b'user_change_password', None)
            if user_change_password:
                urls = patterns(b'', url(b'^auth/user/(\\d+)/password/$', self.admin_view(user_change_password), name=b'user_change_password')) + urls
                break

        return urls