# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/babeldjango/middleware.py
# Compiled at: 2007-08-20 06:52:43
from babel import Locale, UnknownLocaleError
from django.conf import settings
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

__all__ = [
 'get_current_locale', 'LocaleMiddleware']
_thread_locals = local()

def get_current_locale():
    """Get current locale data outside views.

    See http://babel.edgewall.org/wiki/ApiDocs/babel.core for Locale
    objects documentation
    """
    return getattr(_thread_locals, 'locale', None)


class LocaleMiddleware(object):
    """Simple Django middleware that makes available a Babel `Locale` object
    via the `request.locale` attribute.
    """
    __module__ = __name__

    def process_request(self, request):
        try:
            code = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
            locale = Locale.parse(code, sep='-')
        except (ValueError, UnknownLocaleError):
            pass
        else:
            _thread_locals.locale = request.locale = locale