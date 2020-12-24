# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/services/srv_notify.py
# Compiled at: 2019-03-26 17:49:49
# Size of source mod 2**32: 817 bytes
"""
# File: srv_notify.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: notifications service
"""
import sys, gi
try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    NOTIFY_INSTALLED = True
except:
    NOTIFY_INSTALLED = False

from basico.core.mod_srv import Service

class Notification(Service):

    def initialize(self):
        if NOTIFY_INSTALLED:
            Notify.init('Basico')

    def show(self, module, message):
        if NOTIFY_INSTALLED:
            icon = 'basico-component'
            notification = Notify.Notification.new('Basico - %s' % module, '<b>%s</b>' % message, icon)
            notification.show()
        else:
            return