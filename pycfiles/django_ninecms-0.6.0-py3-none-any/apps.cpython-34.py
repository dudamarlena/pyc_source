# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/django-ninecms/ninecms/apps.py
# Compiled at: 2016-04-06 07:45:54
# Size of source mod 2**32: 426 bytes
""" Application name of Nine CMS for Admin """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.apps import AppConfig

class NineCMSConfig(AppConfig):
    name = 'ninecms'
    verbose_name = 'Nine CMS'

    def ready(self):
        import ninecms.signals, ninecms.checks