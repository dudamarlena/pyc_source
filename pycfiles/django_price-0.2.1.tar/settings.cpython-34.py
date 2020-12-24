# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ddanier/work/django/django_price/tests/settings.py
# Compiled at: 2015-09-08 23:10:15
# Size of source mod 2**32: 390 bytes
import warnings
warnings.simplefilter('always')
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': 'db.sqlite'}}
USE_I18N = True
USE_L10N = True
INSTALLED_APPS = [
 'django.contrib.contenttypes',
 'django_deferred_polymorph',
 'django_price',
 'tests']
MIDDLEWARE_CLASSES = ()
STATIC_URL = '/static/'
SECRET_KEY = '0'