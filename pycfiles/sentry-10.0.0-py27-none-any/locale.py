# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/middleware/locale.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import pytz
from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils.translation import _trans, LANGUAGE_SESSION_KEY
from sentry.models import UserOption
from sentry.utils.safe import safe_execute

class SentryLocaleMiddleware(LocaleMiddleware):

    def process_request(self, request):
        self.__skip_caching = request.path_info.startswith(settings.ANONYMOUS_STATIC_PREFIXES)
        if self.__skip_caching:
            return
        safe_execute(self.load_user_conf, request, _with_transaction=False)
        lang_code = request.GET.get('lang')
        if lang_code:
            try:
                language = _trans.get_supported_language_variant(lang_code)
            except LookupError:
                super(SentryLocaleMiddleware, self).process_request(request)
            else:
                _trans.activate(language)
                request.LANGUAGE_CODE = _trans.get_language()

        else:
            super(SentryLocaleMiddleware, self).process_request(request)

    def load_user_conf(self, request):
        if not request.user.is_authenticated():
            return
        language = UserOption.objects.get_value(user=request.user, key='language')
        if language:
            request.session[LANGUAGE_SESSION_KEY] = language
        timezone = UserOption.objects.get_value(user=request.user, key='timezone')
        if timezone:
            request.timezone = pytz.timezone(timezone)

    def process_response(self, request, response):
        try:
            if self.__skip_caching:
                return response
        except AttributeError:
            pass

        return super(SentryLocaleMiddleware, self).process_response(request, response)