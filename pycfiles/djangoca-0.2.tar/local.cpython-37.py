# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/base_django/configuracion/local.py
# Compiled at: 2019-07-31 13:53:25
# Size of source mod 2**32: 455 bytes
from .base import *
DEBUG = True
ALLOWED_HOSTS = [
 '*']
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':os.path.join(BASE_DIR, 'db.sqlite3')}}
STATICFILES_DIRS = (
 BASE_DIR, 'static')