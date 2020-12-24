# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/photorepl/threads.py
# Compiled at: 2015-07-08 01:08:14
# Size of source mod 2**32: 1085 bytes
import threading
from gi.repository import Gtk, Gdk
from photorepl.views.preview import Preview

class UIThread(threading.Thread):
    __doc__ = "\n    A thread for displaying UI elements and photos. This thread shouldn't\n    maintain any state which must be preserved, and should act as a daemon\n    thread which exits when the main thread (the REPL) is terminated.\n    "

    def __init__(self):
        """
        Initialize the ui thead, making sure it's a daemon thread which will
        exit when the main thread is terminated.
        """
        super(UIThread, self).__init__()
        self.daemon = True

    def run(self):
        """
        Create the preview window and run the Gtk main loop when the UI thead
        is started.
        """
        Gdk.threads_init()
        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()

    def open_window(self, filename=None, rawfile=None):
        """
        Open a new preview window with the given preview file and raw file.
        """
        return Preview(filename=filename, rawfile=rawfile, show=True)