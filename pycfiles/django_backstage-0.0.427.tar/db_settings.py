# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/settings/db_settings.py
# Compiled at: 2014-07-03 13:45:32
DBENGINE = 'django.db.backends.sqlite3'
DBHOST = '127.0.0.1'
DBPORT = ''
DBUSER = ''
DBPASS = ''
DBNAME = 'db/django_backstage.sq3'
DATABASES = {}
DATABASES['default'] = {'NAME': DBNAME, 
   'ENGINE': DBENGINE, 
   'HOST': DBHOST, 
   'PORT': DBPORT, 
   'USER': DBUSER, 
   'PASSWORD': DBPASS}
DEFAULT_DB_ALIAS = 'default'
DEFAULT_DB = DATABASES['default']