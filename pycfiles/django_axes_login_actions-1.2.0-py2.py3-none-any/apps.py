# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/titschendorf.de/axes_login_actions/apps.py
# Compiled at: 2017-03-25 09:54:41
from django.apps import AppConfig

class AxesLoginActionsConfig(AppConfig):
    name = 'axes_login_actions'

    def ready(self):
        import axes_login_actions.signals