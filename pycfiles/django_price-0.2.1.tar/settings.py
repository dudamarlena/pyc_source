# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ddanier/work/django/django_price/tests/settings.py
# Compiled at: 2015-09-08 23:10:15
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