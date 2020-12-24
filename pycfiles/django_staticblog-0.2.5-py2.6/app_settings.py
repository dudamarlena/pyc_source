# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/staticblog-bak/app_settings.py
# Compiled at: 2012-10-05 07:52:59
from django.conf import settings
import os
STATICBLOG_ROOT = os.path.abspath(os.path.dirname(__name__))
STATICBLOG_POST_DIRECTORY = getattr(settings, 'STATICBLOG_POST_DIRECTORY', STATICBLOG_ROOT + '/posts/')
STATICBLOG_COMPILE_DIRECTORY = getattr(settings, 'STATICBLOG_COMPILE_DIRECTORY', settings.MEDIA_ROOT + 'posts/')
STATICBLOG_STORAGE = getattr(settings, 'STATICBLOG_STORAGE', settings.DEFAULT_FILE_STORAGE)