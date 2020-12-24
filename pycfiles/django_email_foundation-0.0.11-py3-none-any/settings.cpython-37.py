# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/settings.py
# Compiled at: 2019-03-18 03:08:32
# Size of source mod 2**32: 1681 bytes
import os
from django.conf import settings
DEF_NPM_OR_YARN = getattr(settings, 'DEF_NPM_OR_YARN', 'yarn')
DEF_INSTALL_COMMANDS = {'npm':'install', 
 'yarn':'add'}
DEF_NPM_YARN_INSTALL_COMMAND = DEF_INSTALL_COMMANDS[DEF_NPM_OR_YARN]
DEF_NODE_MODULES_PATH = getattr(settings, 'DEF_NODE_MODULES_PATH', os.getcwd())
DEF_NODE_PACKAGES_REQUIRED = ('gulp@4.0.0', 'panini@1.3.0', 'inky@1.3.6', 'gulp-open@3.0.1',
                              'gulp-debug@4.0.0', 'gulp-load-plugins@1.5.0', 'gulp-sass@2.3.2',
                              'gulp-inline-css@3.3.1', 'gulp-uncss@1.0.6', 'node-sass@4.9.3',
                              'gulp-imagemin@2.4.0', 'siphon-media-query@1.0.0',
                              'lazypipe@1.0.2', 'gulp-htmlmin@1.3.0', 'gulp-replace@0.5.4')
DEF_TEMPLATES_SOURCE_PATH = getattr(settings, 'DEF_TEMPLATES_SOURCE_PATH', None)
DEF_TEMPLATES_TARGET_PATH = getattr(settings, 'DEF_TEMPLATES_TARGET_PATH', None)
DEF_STATIC_TARGET_PATH = getattr(settings, 'DEF_STATIC_TARGET_PATH', None)
DEF_IGNORE_FILES = getattr(settings, 'DEF_IGNORE_FILES', ('subject.html', 'body.txt'))
DEF_RUNSERVER_HOST = getattr(settings, 'DEF_RUNSERVER_HOST', 'http://localhost:8000')