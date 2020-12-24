# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/notifier.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 369 bytes
import notify2
from omnilog.strings import Strings

class Notifier(object):
    __doc__ = '\n    Wrapper for the notify2 library.\n    '

    def __init__(self):
        self.appName = Strings.APP_NAME
        notify2.init(self.appName)

    def send_notify(self, title, body):
        n = notify2.Notification(title, body)
        n.show()