# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ralph/Development/django-internationalflavor/tests/settings.py
# Compiled at: 2020-05-04 05:43:24
# Size of source mod 2**32: 348 bytes
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':':memory:'}}
INSTALLED_APPS = [
 'internationalflavor']
import django
if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
SECRET_KEY = 'spam-spam-spam-spam'
MIDDLEWARE_CLASSES = []