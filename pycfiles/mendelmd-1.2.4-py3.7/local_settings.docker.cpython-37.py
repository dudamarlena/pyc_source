# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendelmd/local_settings.docker.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 785 bytes
DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql_psycopg2', 
             'NAME':'postgres', 
             'USER':'postgres', 
             'HOST':'db', 
             'PORT':5432}}
SECRET_KEY = '*efl#$$!@93)8397wwf8hy3873&ad8h7d2w-JKFCGYURaonyGUimaraesCorreayus5mzcx&@'
DEBUG = True
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_URL = '/var/www/static/'
STATICFILES_DIRS = [
 os.path.join(BASE_DIR, 'static')]