# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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