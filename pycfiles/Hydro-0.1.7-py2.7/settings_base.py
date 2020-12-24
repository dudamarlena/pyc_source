# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/conf/settings_base.py
# Compiled at: 2015-08-06 10:05:35
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
APPLICATION_NAME = 'HYDRO'
SECRET_KEY = '8lu*6g0lg)9w!ba+a$edk)xx)x%rxgb$i1&amp;022shmi1jcgihb*'
SECOND = 1
MINUTE = SECOND * 60
SECONDS_IN_DAY = SECOND * 86400
MYSQL_CACHE_DB = 'cache'
MYSQL_STATS_DB = 'stats'
MYSQL_CACHE_TABLE = 'hydro_cache_table'
CACHE_IN_MEMORY_KEY_EXPIRE = 600
CACHE_DB_KEY_EXPIRE = 86400
USE_STATS_DB = False
DATABASES = {'stats': {'ENGINE': 'django.db.backends.mysql', 
             'NAME': MYSQL_STATS_DB, 
             'USER': 'root', 
             'PASSWORD': 'xxxx', 
             'HOST': '127.0.0.1', 
             'OPTIONS': {'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;', 
                         'compress': True}}, 
   'cache': {'ENGINE': 'django.db.backends.mysql', 
             'NAME': MYSQL_CACHE_DB, 
             'USER': 'root', 
             'PASSWORD': 'xxxx', 
             'HOST': '127.0.0.1', 
             'OPTIONS': {'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;', 
                         'compress': True}}, 
   'default': {'ENGINE': 'django.db.backends.mysql', 
               'NAME': 'cache', 
               'USER': 'root', 
               'PASSWORD': 'xxxx', 
               'HOST': '127.0.0.1', 
               'OPTIONS': {'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;', 
                           'compress': True}}}