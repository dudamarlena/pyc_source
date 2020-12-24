# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/middleware.py
# Compiled at: 2012-11-19 10:50:40
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from cms.middleware.multilingual import MultilingualURLMiddleware
from cms.utils.i18n import get_default_language

class MultilingualMiddleware(MultilingualURLMiddleware):
    """
    Supplies additional method that redirects / to /en /de etc.
    """

    def process_request(self, request):
        setting = getattr(settings, 'CMS_DEFAULT_LANGUAGE', 'default')
        if setting is 'default':
            language = get_default_language()
        else:
            language = self.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language
        if request.META['PATH_INFO'] == '/' and getattr(settings, 'CMS_SEO_ROOT', True):
            return HttpResponseRedirect('/%s/' % language)