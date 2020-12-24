# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/site_basics/middleware.py
# Compiled at: 2013-03-08 20:47:47
from django.conf import settings
from django.core.urlresolvers import is_valid_path
from django.http import HttpResponsePermanentRedirect
from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from django.utils.cache import patch_vary_headers

class UpdatedLocaleMiddleware(LocaleMiddleware):

    def process_response(self, request, response):
        language = translation.get_language()
        if response.status_code == 404 and not translation.get_language_from_path(request.path_info) and self.is_language_prefix_patterns_used():
            urlconf = getattr(request, 'urlconf', None)
            language_path = '/%s%s' % (language, request.path_info)
            if settings.APPEND_SLASH and not language_path.endswith('/'):
                language_path = language_path + '/'
            if is_valid_path(language_path, urlconf):
                language_url = '%s://%s/%s%s' % (
                 request.is_secure() and 'https' or 'http',
                 request.get_host(), language, request.get_full_path())
                return HttpResponsePermanentRedirect(language_url)
        translation.deactivate()
        patch_vary_headers(response, ('Accept-Language', ))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response