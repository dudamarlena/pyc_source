# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/tests/settings.py
# Compiled at: 2016-04-11 01:51:28
"""
These settings are used by the ``manage.py`` command.

With normal tests we want to use the fastest possible way which is an
in-memory sqlite database but if you want to create migrations you
need a persistant database.

"""
from .test_settings import *
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'db.sqlite'}}