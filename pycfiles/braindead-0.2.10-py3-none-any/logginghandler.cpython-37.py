# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/bcsdk/logginghandler.py
# Compiled at: 2019-12-05 04:55:53
# Size of source mod 2**32: 397 bytes
from bcsdk.bcsdk import Handler

class LoggingHandler(Handler):
    """LoggingHandler"""

    def on_message(self, msg):
        print('Message received: ', msg)
        self.send_message(msg)

    def on_destroy(self):
        print('Destroyed')

    def on_init(self, conf):
        print('Conf received: ', conf)