# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/plugins/notify.py
# Compiled at: 2011-07-09 22:56:18
import pynotify
pynotify.init('Basics')
from feather import Plugin

class Notify(Plugin):
    listeners = set(['songloaded'])
    messengers = set()

    def songloaded(self, payload):
        msg = 'Playing: %s' % payload
        notification = pynotify.Notification('Pyrana', msg)
        notification.show()