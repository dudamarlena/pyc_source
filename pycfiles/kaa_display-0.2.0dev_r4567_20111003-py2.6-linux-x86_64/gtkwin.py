# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/display/gtkwin.py
# Compiled at: 2008-01-18 10:37:26
import kaa
from x11 import X11Display

class GTKWindow(object):
    """
    GTK based Window.
    """

    def __init__(self, window):
        self._window = window
        self.signals = kaa.Signals('key_press_event', 'focus_in_event', 'focus_out_event', 'expose_event', 'map_event', 'unmap_event', 'resize_event', 'configure_event')
        self._display = X11Display(self._window.get_display().get_name())

    def get_size(self):
        return self._window.get_size()

    def show(self, raised=False):
        self._window.show()

    def hide(self):
        self._window.hide()

    def get_id(self):
        return self._window.xid

    def get_visible(self):
        return self._window.is_visible()

    def get_display(self):
        return self._display

    def raise_window(self):
        pass

    def lower_window(self):
        pass

    def set_visible(self, visible=True):
        if visible:
            self.show()
        else:
            self.hide()

    def handle_events(self, events):
        pass

    def move(self, pos, force=False):
        pass

    def resize(self, size, force=False):
        pass

    def set_geometry(self, pos, size, force=False):
        pass

    def get_geometry(self):
        pass

    def get_pos(self):
        pass

    def set_cursor_visible(self, visible):
        pass

    def set_cursor_hide_timeout(self, timeout):
        pass

    def set_fullscreen(self, fs=True):
        pass

    def get_fullscreen(self):
        pass

    def focus(self):
        pass


class GladeWindow(GTKWindow):
    """
    Glade based Window.
    """

    def __init__(self, gladefile, name):
        import gtk.glade
        self._glade = gtk.glade.XML(gladefile, name)
        GTKWindow.__init__(self, self._glade.get_widget(name).window)

    def signal_autoconnect(self, obj):
        """
        Autoconnect signals to the given object.
        """
        return self._glade.signal_autoconnect(obj)

    def get_widget(self, name):
        """
        Get widget based on name.
        """
        return self._glade.get_widget(name)