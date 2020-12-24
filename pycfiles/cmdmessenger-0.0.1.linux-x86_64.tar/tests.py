# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cmdmessenger/tests.py
# Compiled at: 2015-01-27 21:20:54
import serial
from . import messenger
cmds = [{'name': 'kCommError'}, {'name': 'kComment'}, {'name': 'kAcknowledge'}, {'name': 'kAreYouReady'}, {'name': 'kError'}, {'name': 'kAskIfReady'}, {'name': 'kYouAreReady'}, {'name': 'kValuePing'}, {'name': 'kValuePong'}, {'name': 'kMultiValuePing'}, {'name': 'kMultiValuePong'}, {'name': 'kRequestReset'}, {'name': 'kRequestResetAcknowledge'}, {'name': 'kRequestSeries'}, {'name': 'kReceiveSeries'}, {'name': 'kDoneReceiveSeries'}, {'name': 'kPrepareSendSeries'}, {'name': 'kSendSeries'}, {'name': 'kAckSendSeries'}]

def setup(port='/dev/ttyUSB0'):
    s = serial.Serial(port, 115200)
    return messenger.Messenger(s, cmds)


def run(m):
    pass


def test():
    m = setup()
    run(m)