# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/settings/development.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 306 bytes
from __future__ import absolute_import
from .defaults import *
SECRET_KEY = '0jd7t0(05@5d#-7$#w2#zagfruos0r!&t37%9m)_9^#ymg7dq+'
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}