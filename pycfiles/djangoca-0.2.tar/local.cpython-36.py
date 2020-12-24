# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\base_django\configuracion\local.py
# Compiled at: 2019-07-11 01:16:32
# Size of source mod 2**32: 452 bytes
from .base import *
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':os.path.join(BASE_DIR, 'db.sqlite3')}}
STATICFILES_DIRS = (
 BASE_DIR, 'static')