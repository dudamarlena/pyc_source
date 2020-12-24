# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protonvpn_gtk/ui/status.py
# Compiled at: 2020-01-04 07:05:35
# Size of source mod 2**32: 649 bytes
from gi.repository import Gtk

class StatusWindow(Gtk.Window):

    def __init__(self, root):
        super().__init__()
        self.app = root
        self.set_title(f"{self.app.name} Status")

    def cb_show(self, w):
        self.resize(300, 200)
        self.wbox = Gtk.Box(spacing=10, orientation=(Gtk.Orientation.VERTICAL))
        self.wbox.set_homogeneous(False)
        self.label = Gtk.Label()
        self.label.set_justify(Gtk.Justification.LEFT)
        self.wbox.pack_start(self.label, True, True, 0)
        self.add(self.wbox)
        status = self.app.proton('status')()
        self.label.set_text(status)
        self.show_all()