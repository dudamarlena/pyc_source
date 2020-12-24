# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/Datos/devel/hg-repos/scru/scru/utils.py
# Compiled at: 2011-06-17 01:12:31
from gi.repository import Notify, GLib
Notify.init('Scru notify')

def show_notification(title, message, image=None):
    """Show a notification message"""
    n = Notify.Notification.new(title, message, image)
    n.set_hint('transient', GLib.Variant.new_boolean(True))
    n.set_urgency(Notify.Urgency.NORMAL)
    n.set_timeout(5000)
    try:
        if not n.show():
            print 'Failed to send notification'
    except glib.GError:
        pass