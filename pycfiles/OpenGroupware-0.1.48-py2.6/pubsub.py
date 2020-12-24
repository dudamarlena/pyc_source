# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/services/pubsub.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *

class PublishSubscribeService(Service):
    __service__ = 'coils.pubsub'
    __auto_dispatch__ = True
    __is_worker__ = False

    def __init__(self):
        self._queues = {'__coils__.event.appointment': [], '__coils__.event.contact': [], '__coils__.event.enterprise': [], '__coils__.event.participant': [], '__coils__.event.process': [], '__coils__.event.project': [], '__coils__.event.resource': [], '__coils__.event.route': [], '__coils__.event.task': [], '__coils__.event.team': []}
        Service.__init__(self)

    def prepare(self):
        Service.prepare(self)

    def do_list(self, parameter, packet):
        self.send(Packet.Reply(packet, self._queues.keys()))

    def do_create(self, parameter, packet):
        if parameter is None:
            self.send(Packet.Reply(packet, '500 No name in request'))
            return
        else:
            if name not in self._queues:
                self._queues.set(name, {'name': parameter, 'creator': Packet.Service(packet.source), 
                   'created': datetime.datetime.now(), 
                   'security': None, 
                   'subscribers': [], 'persist': False})
                self.send(Packet.Reply(packet, ('201 {0}').format(parameter)))
                return
            self.send(Packet.Reply(packet, ('200 {0}').format(parameter)))
            return

    def do_destroy(self, parameter, packet):
        if parameter is None:
            self.send(Packet.Reply(packet, '500 No name in request'))
            return
        else:
            if parameter in self._queues:
                self._queues.remove(parameter)
                self.send(Packet.Reply(packet, ('200 {0}').format(parameter)))
                return
            self.send(Packet.Reply(packet, ('404 {0}').format(parameter)))
            return

    def do_subscribe(self, parameter, packet):
        if parameter is None:
            self.send(Packet.Reply(packet, '500 No name in request'))
            return
        else:
            if parameter in self._queues:
                if packet.source in self._queues[name]['subscribers']:
                    self.send(Packet.Reply(packet, '200 OK'))
                    return
                else:
                    self._queues[name]['subscribers'].append(packet.source)
                    self.send(Packet.Reply(packet, '201 OK'))
                    return
            else:
                self.send(Packet.Reply(packet, ('404 {0} not found').format(name)))
                return
            return

    def do_unsubscribe(self, parameter, packet):
        if parameter is None:
            self.send(Packet.Reply(packet, '500 No name in request'))
        else:
            if parameter in self._queues:
                if packet.source in self._queues[name]['subscribers']:
                    self._queues[name]['subscribers'].remove(packet.source)
                self.send(Packet.Reply(packet, '200 OK'))
                return
            else:
                self.send(Packet.Reply(packet, ('404 {0} not found').format(name)))
                return
        return

    def do_publish(self, parameter, packet):
        return
        if parameter in self._queues:
            subscribers = self._queues[name]['subscribers']
            for subscriber in subscribers:
                self.send(Packet(('{0}/{1}').format(self.__service__, parameter), subscriber, packet.data))

        self.send(Packet.Reply(packet, '200 Published'))