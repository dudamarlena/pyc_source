# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/middlewares.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 977 bytes
""" Manifest Middlewares
"""
from django.conf import settings
import django.middleware.locale as DjangoLocaleMiddleware
from django.utils import translation
from manifest import defaults

class LocaleMiddleware(DjangoLocaleMiddleware):
    __doc__ = "\n    Set the language by looking at the language setting in the profile.\n\n    It doesn't override the cookie that is set by Django so a user can still\n    switch languages depending if the cookie is set.\n\n    "

    def process_request(self, request):
        lang_cookie = request.session.get(settings.LANGUAGE_COOKIE_NAME)
        if not lang_cookie:
            if request.user.is_authenticated:
                try:
                    lang = getattr(request.user, defaults.MANIFEST_LOCALE_FIELD)
                    translation.activate(lang)
                    request.LANGUAGE_CODE = translation.get_language()
                except AttributeError:
                    pass