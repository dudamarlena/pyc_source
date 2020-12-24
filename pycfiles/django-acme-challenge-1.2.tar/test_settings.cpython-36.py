# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ec2-user/environment/django-acme-challenge/acme_challenge/tests/test_settings.py
# Compiled at: 2018-04-02 16:11:40
# Size of source mod 2**32: 316 bytes
SECRET_KEY = 'secret!'
ROOT_URLCONF = 'acme_challenge.urls'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
INSTALLED_APPS = ('acme_challenge', )
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'APP_DIRS':True}]