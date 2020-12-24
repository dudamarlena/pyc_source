# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feather/test/test_dispatcher.py
# Compiled at: 2011-06-15 17:38:25
import unittest
from feather import Dispatcher, Plugin, Application

class PrintFoo(Plugin):
    listeners = set(['APP_START', 'CALL_FOO'])
    messengers = set(['FOO'])

    def recieve(self, message, payload):
        print 'MMM, FOO'
        self.send('FOO', 'YEEEAHH')


class SendFoo(Plugin):
    listeners = set(['FOO'])
    messengers = set(['CALL_FOO', 'APP_END'])

    def __init__(self):
        self.i = 0

    def recieve(self, message, payload):
        self.i += 1
        print 'SEND FOO %s' % self.i
        if self.i < 100:
            self.send('CALL_FOO')
        else:
            self.send('APP_STOP')


class DispatcherTest(unittest.TestCase):

    def setUp(self):
        self.dis = Dispatcher()
        self.printfoo = PrintFoo()