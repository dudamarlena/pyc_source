# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/middleware/doc.py
# Compiled at: 2018-07-11 18:15:30
from django.conf import settings
from django import http

class XViewMiddleware(object):
    """
    Adds an X-View header to internal HEAD requests -- used by the documentation system.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        If the request method is HEAD and either the IP is internal or the
        user is a logged-in staff member, quickly return with an x-header
        indicating the view function.  This is used by the documentation module
        to lookup the view function for an arbitrary page.
        """
        assert hasattr(request, 'user'), "The XView middleware requires authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'."
        if request.method == 'HEAD' and (request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS or request.user.is_active and request.user.is_staff):
            response = http.HttpResponse()
            response['X-View'] = '%s.%s' % (view_func.__module__, view_func.__name__)
            return response