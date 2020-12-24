# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fast_gfk/tests/settings/111.py
# Compiled at: 2017-07-17 11:51:22
import os, glob
BASE_DIR = os.path.join(glob.glob(os.environ['VIRTUAL_ENV'] + '/lib/*/site-packages')[0], 'fast_gfk')
DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
INSTALLED_APPS = ('fast_gfk.tests', 'django.contrib.contenttypes', 'test_without_migrations')
SECRET_KEY = 'SECRET_KEY'
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'DIRS': [], 'OPTIONS': {}}]