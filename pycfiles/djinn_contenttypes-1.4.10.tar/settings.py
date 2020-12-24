# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/settings.py
# Compiled at: 2015-11-17 03:57:50
from django.conf import settings
DEFAULT_DATETIME_INPUT_FORMAT = getattr(settings, 'DEFAULT_DATETIME_INPUT_FORMAT', '%d/%m/%Y %H:%M')
DEFAULT_DATE_INPUT_FORMAT = getattr(settings, 'DEFAULT_DATE_INPUT_FORMAT', '%d/%m/%Y')