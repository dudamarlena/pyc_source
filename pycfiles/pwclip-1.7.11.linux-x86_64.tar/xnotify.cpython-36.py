# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/xlib/xnotify.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 1062 bytes
"""x notification function"""
from inspect import stack
try:
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify as xnote
except (AttributeError, ImportError, ValueError) as err:

    def xnotify(msg, **_):
        """xnotify faker function"""
        pass


else:

    def xnotify(msg, name=stack()[1][3], wait=5):
        """
                disply x notification usually in the upper right corner of the display
                """
        try:
            xnote.init(str(name))
            note = xnote.Notification.new(msg)
            note.set_timeout(int(wait * 1000))
            note.show()
        except (NameError, RuntimeError):
            pass