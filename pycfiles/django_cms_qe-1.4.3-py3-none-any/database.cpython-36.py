# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/database.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 408 bytes
"""
Database settings, used PostgreSQL without auth by default.
"""
DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql_psycopg2', 
             'NAME':'cms_qe', 
             'USER':'', 
             'PASSWORD':'', 
             'HOST':'', 
             'OPTIONS':{'application_name': 'cms_qe'}}}