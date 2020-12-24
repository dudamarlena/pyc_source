# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\workspace\django-template-project\source\conf\settings\dev.py
# Compiled at: 2011-06-19 18:35:58
import os
from project.utils.settings import get_setting, import_settings
from project.utils.install import install_settings, install_app
install_settings('conf.settings.main')
install_app('web', 'conf.apps.web')
install_app('django.contrib.admin', 'conf.apps.admin')
import_settings(globals())
DEBUG = TEMPLATE_DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(get_setting('PROJECT_ROOT'), 'source', 'db', 'dev.sqlite')}}