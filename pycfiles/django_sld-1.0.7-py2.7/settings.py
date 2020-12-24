# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djsld/tests/settings.py
# Compiled at: 2012-10-05 09:39:32
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.contrib.gis.db.backends.postgis', 
               'NAME': 'djsld_test', 
               'USER': 'djsld', 
               'PASSWORD': 'djsld', 
               'HOST': 'localhost', 
               'PORT': '5432'}}
POSTGIS_TEMPLATE = 'djsld_test'
INSTALLED_APPS = ('django.contrib.gis', 'djsld', 'djsld-test')