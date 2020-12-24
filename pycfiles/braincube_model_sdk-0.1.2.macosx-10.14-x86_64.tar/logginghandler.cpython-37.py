# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/bcsdk/logginghandler.py
# Compiled at: 2019-12-05 04:55:53
# Size of source mod 2**32: 397 bytes
from bcsdk.bcsdk import Handler

class LoggingHandler(Handler):
    __doc__ = 'This handler logs to console everythiong that it received and sends back anything it receives'

    def on_message(self, msg):
        print('Message received: ', msg)
        self.send_message(msg)

    def on_destroy(self):
        print('Destroyed')

    def on_init(self, conf):
        print('Conf received: ', conf)