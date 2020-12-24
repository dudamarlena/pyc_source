# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/apps.py
# Compiled at: 2015-04-02 05:00:35
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
        import ninecms.signals