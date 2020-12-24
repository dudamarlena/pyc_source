# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_settings.py
# Compiled at: 2018-06-21 03:34:43
# Size of source mod 2**32: 341 bytes
SECRET_KEY = 'faaaake-key'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':':memory:', 
             'USER':'', 
             'PASSWORD':'', 
             'HOST':'', 
             'PORT':''}}
INSTALLED_APPS = [
 'tests',
 'marple']
MARPLE_ROOT = 'tests/sass'
MARPLE_EXCLUDE = [
 'ignoreme']