# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/services/clock.py
# Compiled at: 2012-10-12 07:02:39
import time
from coils.foundation import *
from coils.core import *

class ClockService(Service):
    __service__ = 'coils.clock'
    __auto_dispatch__ = True
    __is_worker__ = True

    def __init__(self):
        Service.__init__(self)

    def prepare(self):
        self._subscribers = []
        self._alarms = {}
        self._ctx = AnonymousContext()
        self._ticktock = time.time()
        Service.prepare(self)

    @property
    def ticktock(self):
        if time.time() - self._ticktock > 59:
            self._ticktock = time.time()
            return True
        return False

    @property
    def subscribers(self):
        return self._subscribers

    @property
    def stamp(self):
        x = self._ctx.get_utctime()
        return ('{0} {1}').format(x.strftime('%Y %m %d %H %M %w %a %b'), int(time.mktime(x.timetuple())))

    def do_subscribe(self, parameter, packet):
        if packet.source not in self.subscribers:
            self.subscribers.append(packet.source)
        self.send(Packet.Reply(packet, self.stamp))

    def do_unsubscribe(self, parameter, packet):
        if packet.source in self.subscribers:
            self.subscribers.remove(packet.source)
        self.send(Packet.Reply(packet, self.stamp))

    def do_setalarm(self, parameter, packet):
        try:
            source = packet.data.get('alarmTarget', None)
            if source is None:
                source = packet.source
            t = float(parameter)
            if t not in self._alarms:
                self._alarms[t] = []
            self._alarms[t].append(source)
        except Exception, e:
            self.log.exception(e)
            self.send(Packet.Reply(packet, {'status': 500, 'test': 'Error'}))
        else:
            self.send(Packet.Reply(packet, {'status': 201, 'test': 'OK'}))

        return

    def work(self):
        if self.ticktock:
            try:
                t = time.time()
                x = self.stamp
                for target in self.subscribers:
                    self.send(Packet('coils.clock/__null', target, x))

                for alarm in self._alarms.keys():
                    if alarm < t:
                        self.log.debug(('firing alarms for {0}').format(alarm))
                        for target in self._alarms[alarm]:
                            self.log.debug(('Sending alarm packet for {0} to {1}').format(alarm, target))
                            self.send(Packet('coils.clock/__null', target, None))

                    self.log.debug(('expiring alarms for {0}').format(alarm))
                    del self._alarms[alarm]

            except Exception, e:
                self.log.exception(e)

        return