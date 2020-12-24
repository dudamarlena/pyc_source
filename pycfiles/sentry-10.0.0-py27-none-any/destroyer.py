# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/mediators/service_hooks/destroyer.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.mediators import Mediator, Param

class Destroyer(Mediator):
    service_hook = Param('sentry.models.ServiceHook')

    def call(self):
        self._destroy_service_hook()
        return self.service_hook

    def _destroy_service_hook(self):
        self.service_hook.delete()