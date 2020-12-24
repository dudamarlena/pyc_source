# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/subservice.py
# Compiled at: 2012-10-12 07:02:39
import logging, sys, multiprocessing, datetime, time
from bundlemanager import BundleManager
from packet import Packet

class SubService(object):

    def __init__(self, name, target=None, broker=None):
        if target is None:
            self._target = BundleManager.get_service(name)
        else:
            self._target = target
        self._process = None
        self._hello_uuid = None
        self._hello_ack = False
        self._name = name
        self._signals = []
        self._started = datetime.datetime.now()
        self._standby = False
        self._broker = None
        return

    def send(self, packet):
        self._send.send(packet)

    @property
    def main(self):
        return self._target.run

    @property
    def process(self):
        return self._process

    @property
    def hello_uuid(self):
        return self._hello_uuid

    @property
    def acknowledged(self):
        return self._hello_ack

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target

    @property
    def is_alive(self):
        return self._process.is_alive()

    def acknowledge(self, packet):
        if packet.reply_to == self.hello_uuid and str(packet.data) == 'MASTER':
            self._hello_ack = True
            return True
        return False

    def signal(self, signal):
        self._broker.send(Packet('coils.master/__null', ('{0}/{1}').format(self.name, signal), None))
        return

    def subscribe_to_signal(self, signal):
        signal = signal.lower()
        if signal not in self._signals:
            self._signals.append(signal)

    def unsubscribe_from_signal(self, signal):
        signal = signal.lower()
        if signal in self._signals:
            self._signals.remove(signal)

    def is_subscribed_to_signal(self, signal):
        signal = signal.lower()
        return signal in self._signals

    def terminate(self):
        if self._process:
            self._process.terminate()

    def release(self):
        self._standby = False

    def hold(self):
        self._standby = True

    @property
    def held(self):
        return self._standby

    def say_hello(self):
        packet = Packet('coils.master/__hello_ack', ('{0}/__hello').format(self.name), 'MASTER')
        self._hello_uuid = packet.uuid
        self._hello_ack = False
        self._broker.send(packet)

    def start(self, _queue):
        self._process = multiprocessing.Process(target=self.main, args=(), name=self.name)
        self._process.start()