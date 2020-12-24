# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/apps.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 189 bytes
from django.apps import AppConfig

class DjreservationConfig(AppConfig):
    name = 'djreservation'

    def ready(self):
        import djreservation.signals
        AppConfig.ready(self)