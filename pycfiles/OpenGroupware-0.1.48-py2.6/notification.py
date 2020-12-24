# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/notification.py
# Compiled at: 2012-10-12 07:02:39
from time import time
from coils.foundation import *
from coils.core import *

class NotificationService(Service):
    __service__ = 'coils.schedular.notification'
    __auto_dispatch__ = True
    __is_worker__ = False

    def __init__(self):
        Service.__init__(self)

    def prepare(self):
        self._iter = 0
        Service.prepare(self)
        packet = Packet('coils.schedular.notification/ticktock', 'coils.clock/subscribe', None)
        self.send(packet)
        self._time = time() + 100
        self._ctx = AdministrativeContext()
        return

    def iteration(self):
        self._iter = self._iter + 1
        return self._iter

    def do_list_notifications(self, route, packet):
        self.send(Packet.Reply(packet, '500 Not implemented'))

    def do_ticktock(self, parameter, packet):
        pass