# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/django-mips/mips/dbsettings_default.py
# Compiled at: 2015-11-13 09:30:49
"""Database settings file"""
DBNAME = ''
USER = ''
PASSWORD = ''
HOST = 'xxx.xxx.xxx.xxx'
SECRET_KEY = 'set-secret-key-here'
ALLOWED_HOSTS = []
import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(PROJECT_DIR, 'mips.db')}}