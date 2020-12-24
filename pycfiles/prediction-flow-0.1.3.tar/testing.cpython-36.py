# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/omri/code/prediction/prediction/settings/testing.py
# Compiled at: 2017-12-26 08:32:26
# Size of source mod 2**32: 175 bytes
from .base import *
DEBUG = True
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':os.path.join(BASE_DIR, 'db.sqlite3')}}