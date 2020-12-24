# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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