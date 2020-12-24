# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/decorators.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 1045 bytes
""" Manifest Decorators
"""
from functools import wraps
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from manifest import defaults

def secure_required(view_func):
    """
    Decorator that redirects to a secure version (https) of the url.

    If ``MANIFEST_USE_HTTPS`` setting is ``True``, any view this decorator
    applied and accessed through an insecure (http) protocol, will return
    a permanent redirect to the secure (https) version of itself.

    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not settings.DEBUG:
            if not request.is_secure():
                if defaults.MANIFEST_USE_HTTPS:
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(secure_url)
        return view_func(request, *args, **kwargs)

    return _wrapped_view