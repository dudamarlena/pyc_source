# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case9_9_1.py
# Compiled at: 2018-12-17 11:51:20
from case import Case
from autobahn.websocket.protocol import WebSocketProtocol
import binascii
from zope.interface import implements
from twisted.internet import reactor, interfaces

class FrameProducer:
    implements(interfaces.IPushProducer)

    def __init__(self, proto, payload):
        self.proto = proto
        self.payload = payload
        self.paused = False
        self.stopped = False

    def pauseProducing(self):
        self.paused = True

    def resumeProducing(self):
        if self.stopped:
            return
        self.paused = False
        while not self.paused:
            self.proto.sendMessageFrame(self.payload)

    def stopProducing(self):
        self.stopped = True


class Case9_9_1(Case):
    PAYLOAD = '*' * 1024 * 4
    DESCRIPTION = 'Send a text message consisting of an infinite sequence of frames with payload 4k. Do this for X seconds.'
    EXPECTATION = '...'

    def onOpen(self):
        self.expected[Case.OK] = [
         ('timeout', 'A'), ('timeout', 'B')]
        self.expectedClose = {'closedByMe': True, 'closeCode': [self.p.CLOSE_STATUS_CODE_NORMAL], 'requireClean': True}
        self.p.createWirelog = False
        self.producer = FrameProducer(self.p, self.PAYLOAD)
        self.p.registerProducer(self.producer, True)
        self.p.beginMessage(opcode=WebSocketProtocol.MESSAGE_TYPE_TEXT)
        self.producer.resumeProducing()
        self.p.continueLater(3, self.part2, 'A')

    def part2(self):
        self.received.append(('timeout', 'A'))
        self.producer.stopProducing()
        self.p.endMessage()
        self.p.continueLater(5, self.part3, 'B')

    def part3(self):
        self.received.append(('timeout', 'B'))
        self.p.createWirelog = True
        self.p.sendClose(WebSocketProtocol.CLOSE_STATUS_CODE_NORMAL, 'You have survived;)')

    def onConnectionLost(self, failedByMe):
        self.producer.stopProducing()
        Case.onConnectionLost(self, failedByMe)