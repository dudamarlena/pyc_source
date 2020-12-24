# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/simo/PycharmProjects/mezzanine_page_auth/mezzanine_page_auth/middleware.py
# Compiled at: 2014-02-07 03:34:44
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from mezzanine.pages.models import Page
from .models import PageAuthGroup

class PageAuthMiddleware(object):

    def process_request(self, request):
        if not hasattr(request, b'user'):
            raise ImproperlyConfigured(b"The PageAuthMiddleware middleware requires the authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' before the PageAuthMiddleware class.")
        slug = request.path
        if slug != b'/':
            slug = slug.strip(b'/')
        request.unauthorized_pages = PageAuthGroup.unauthorized_pages(request.user)
        try:
            page = Page.objects.get(slug=slug)
            if page.pk in request.unauthorized_pages:
                return HttpResponseForbidden()
        except Page.DoesNotExist:
            pass