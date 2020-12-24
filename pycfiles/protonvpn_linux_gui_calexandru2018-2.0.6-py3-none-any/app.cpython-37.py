# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protonvpn_gtk/ui/app.py
# Compiled at: 2020-01-04 14:09:39
# Size of source mod 2**32: 500 bytes
from gi.repository import Gtk
from .status import StatusWindow
from .indicator import Indicator
from protonvpn_gtk.utils.core import ProtonVPN

class MyApp(Gtk.Application):

    @staticmethod
    def proton(method: str):
        return lambda _=None: getattr(ProtonVPN(), method)()

    def __init__(self, app_name):
        super().__init__()
        self.name = app_name
        self.main_win = StatusWindow(self)
        self.indicator = Indicator(self)

    def run(self):
        Gtk.main()