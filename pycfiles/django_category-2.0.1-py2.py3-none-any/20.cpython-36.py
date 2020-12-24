# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-category/category/tests/settings/20.py
# Compiled at: 2019-01-03 06:09:58
# Size of source mod 2**32: 419 bytes
USE_TZ = True
DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql', 
             'NAME':'django', 
             'USER':'postgres', 
             'PASSWORD':'', 
             'HOST':'', 
             'PORT':''}}
INSTALLED_APPS = ('category', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sites')
SITE_ID = 1
SECRET_KEY = 'SECRET_KEY'