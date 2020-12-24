# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/elbaschid/Worx/Tangent.One/django-url-tracker/tests/config.py
# Compiled at: 2012-09-07 02:40:30
import os
from django.conf import settings, global_settings
if not settings.configured:
    location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
    settings.configure(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 
                   'NAME': ':memory:'}}, INSTALLED_APPS=[
     'django.contrib.auth',
     'django.contrib.admin',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.sites',
     'django.contrib.flatpages',
     'url_tracker'], TEMPLATE_CONTEXT_PROCESSORS=('django.contrib.auth.context_processors.auth',
                                                  'django.core.context_processors.request',
                                                  'django.core.context_processors.debug',
                                                  'django.core.context_processors.i18n',
                                                  'django.core.context_processors.media',
                                                  'django.core.context_processors.static',
                                                  'django.contrib.messages.context_processors.messages'), TEMPLATE_DIRS=(
     location('templates'),), MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES + ('url_tracker.middleware.URLChangePermanentRedirectMiddleware', ), AUTHENTICATION_BACKENDS=('django.contrib.auth.backends.ModelBackend', ), ROOT_URLCONF='tests.urls', DEBUG=False, SITE_ID=1, APPEND_SLASH=True)