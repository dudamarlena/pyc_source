# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/conf/settings.py
# Compiled at: 2016-10-06 05:45:05
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
MESSAGES_PER_PAGE = getattr(settings, 'AUTOTRANSLATE_MESSAGES_PER_PAGE', 10)
ENABLE_TRANSLATION_SUGGESTIONS = getattr(settings, 'AUTOTRANSLATE_ENABLE_TRANSLATION_SUGGESTIONS', False)
YANDEX_TRANSLATE_KEY = getattr(settings, 'YANDEX_TRANSLATE_KEY', None)
AZURE_CLIENT_ID = getattr(settings, 'AZURE_CLIENT_ID', None)
AZURE_CLIENT_SECRET = getattr(settings, 'AZURE_CLIENT_SECRET', None)
MAIN_LANGUAGE = getattr(settings, 'AUTOTRANSLATE_MAIN_LANGUAGE', None)
MESSAGES_SOURCE_LANGUAGE_CODE = getattr(settings, 'AUTOTRANSLATE_MESSAGES_SOURCE_LANGUAGE_CODE', 'en')
MESSAGES_SOURCE_LANGUAGE_NAME = getattr(settings, 'AUTOTRANSLATE_MESSAGES_SOURCE_LANGUAGE_NAME', 'English')
ACCESS_CONTROL_FUNCTION = getattr(settings, 'AUTOTRANSLATE_ACCESS_CONTROL_FUNCTION', None)
WSGI_AUTO_RELOAD = getattr(settings, 'AUTOTRANSLATE_WSGI_AUTO_RELOAD', False)
UWSGI_AUTO_RELOAD = getattr(settings, 'AUTOTRANSLATE_UWSGI_AUTO_RELOAD', False)
EXCLUDED_APPLICATIONS = getattr(settings, 'AUTOTRANSLATE_EXCLUDED_APPLICATIONS', ())
POFILE_WRAP_WIDTH = getattr(settings, 'AUTOTRANSLATE_POFILE_WRAP_WIDTH', 78)
STORAGE_CLASS = getattr(settings, 'AUTOTRANSLATE_STORAGE_CLASS', 'autotranslate.storage.CacheAutotranslateStorage')
ENABLE_REFLANG = getattr(settings, 'AUTOTRANSLATE_ENABLE_REFLANG', False)
POFILENAMES = getattr(settings, 'AUTOTRANSLATE_POFILENAMES', ('django.po', 'djangojs.po'))
AUTOTRANSLATE_CACHE_NAME = getattr(settings, 'AUTOTRANSLATE_CACHE_NAME', 'autotranslate' if 'autotranslate' in settings.CACHES else 'default')
AUTOTRANSLATE_REQUIRES_AUTH = getattr(settings, 'AUTOTRANSLATE_REQUIRES_AUTH', True)
AUTOTRANSLATE_EXCLUDED_PATHS = getattr(settings, 'AUTOTRANSLATE_EXCLUDED_PATHS', ())
AUTOTRANSLATE_LANGUAGE_GROUPS = getattr(settings, 'AUTOTRANSLATE_LANGUAGE_GROUPS', False)
AUTO_COMPILE = getattr(settings, 'AUTOTRANSLATE_AUTO_COMPILE', True)