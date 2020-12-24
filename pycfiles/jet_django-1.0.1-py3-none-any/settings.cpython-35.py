# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_django/jet_django/settings.py
# Compiled at: 2020-01-19 06:51:36
# Size of source mod 2**32: 1745 bytes
from django.conf import settings
from django.db import connection
JET_BACKEND_API_BASE_URL = getattr(settings, 'JET_BACKEND_API_BASE_URL', 'https://api.jetadmin.io/api')
JET_BACKEND_WEB_BASE_URL = getattr(settings, 'JET_BACKEND_WEB_BASE_URL', 'https://app.jetadmin.io')
JET_READ_ONLY = getattr(settings, 'JET_READ_ONLY', False)
JET_REGISTER_TOKEN_ON_START = getattr(settings, 'JET_REGISTER_TOKEN_ON_START', True)
JET_CORS_HEADERS = getattr(settings, 'JET_CORS_HEADERS', 'corsheaders' not in settings.INSTALLED_APPS)
JET_MEDIA_FILE_STORAGE = getattr(settings, 'JET_MEDIA_FILE_STORAGE', settings.DEFAULT_FILE_STORAGE)
JET_PROJECT = getattr(settings, 'JET_PROJECT', None)
JET_TOKEN = getattr(settings, 'JET_TOKEN', None)
JET_DJANGO_DATABASE = getattr(settings, 'JET_DJANGO_DATABASE', 'default')
JET_DATABASE_EXTRA = getattr(settings, 'JET_DATABASE_EXTRA', None)
JET_DATABASE_ONLY = getattr(settings, 'JET_DATABASE_ONLY', None)
JET_DATABASE_EXCEPT = getattr(settings, 'JET_DATABASE_EXCEPT', None)
JET_DATABASE_SCHEMA = getattr(settings, 'JET_DATABASE_SCHEMA', None)
database_settings = settings.DATABASES.get(JET_DJANGO_DATABASE, {})
database_engine = None
mysql_read_default_file = database_settings.get('OPTIONS', {}).get('read_default_file')
if JET_DATABASE_EXTRA is None and mysql_read_default_file:
    JET_DATABASE_EXTRA = '?read_default_file={}'.format(mysql_read_default_file)
if connection.vendor == 'postgresql':
    database_engine = 'postgresql'
else:
    if connection.vendor == 'mysql':
        database_engine = 'mysql'
    else:
        if connection.vendor == 'oracle':
            database_engine = 'oracle'
        else:
            if connection.vendor in ('mssql', 'microsoft'):
                database_engine = 'mssql+pyodbc'
            elif connection.vendor == 'sqlite':
                database_engine = 'sqlite'