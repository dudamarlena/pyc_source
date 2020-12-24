# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_autocode_tools/app_settings.py
# Compiled at: 2019-09-09 13:42:28
# Size of source mod 2**32: 934 bytes
from __future__ import print_function
from os import path, getcwd

class Settings:

    def __init__(self, settings):
        self.AUTO_CODE_ROOT_APP = getattr(settings, 'AUTO_CODE_ROOT_APP', None)
        self.AUTO_CODE_TEMPLATES_VIEW = getattr(settings, 'AUTO_CODE_TEMPLATES_VIEW', path.join(path.abspath(path.dirname(__file__)), 'templates'))
        self.AUTO_CODE_VIEW_SAVE_PATH = getattr(settings, 'AUTO_CODE_VIEW_SAVE_PATH', path.join(getcwd(), 'auto_code/views'))
        self.AUTO_CODE_ORM_SAVE_PATH = getattr(settings, 'AUTO_CODE_ORM_SAVE_PATH', path.join(getcwd(), 'auto_code/orms'))
        self.AUTO_CODE_SER_SAVE_PATH = getattr(settings, 'AUTO_CODE_SER_SAVE_PATH', path.join(getcwd(), 'auto_code/sers'))