# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/LogViewFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Base class for Sutekh Frames"""
import gtk
from .AutoScrolledWindow import AutoScrolledWindow
from .BasicFrame import BasicFrame
from .LogViewMenu import LogViewMenu
from .LogTextView import LogTextView

class LogViewFrame(BasicFrame):
    """The frame holding the log message view.

       The LogHandler is created by the main window, so it's
       there from the start, not tied to this frame.
       """
    _sName = 'Log View Frame'

    def __init__(self, oMainWindow):
        super(LogViewFrame, self).__init__(oMainWindow)
        self.set_name('log frame')
        self._oView = LogTextView()
        self._oMenu = LogViewMenu(self, oMainWindow)
        self.set_title('Log Messages View')
        self.add_parts()
        oMainWindow.gui_log_handler.set_widget(self)

    type = property(fget=lambda self: self._sName, doc='Frame Type')
    view = property(fget=lambda self: self._oView, doc='View')

    def reload(self):
        """Reload frame contents"""
        self._oView.set_log_messages(self._oMainWindow.gui_log_handler.aQueue)

    def do_queued_reload(self):
        """Do a deferred reload if one was set earlier"""
        self._bNeedReload = False
        self.reload()

    def add_parts(self):
        """Add the menu and text view to the frame"""
        oMbox = gtk.VBox(False, 2)
        oMbox.pack_start(self._oTitle, False, False)
        oMbox.pack_start(self._oMenu, False, False)
        oMbox.pack_end(AutoScrolledWindow(self._oView), expand=True)
        self.add(oMbox)
        self.show_all()
        self.set_drag_handler(self._oMenu)
        self.set_drop_handler(self._oMenu)

    def cleanup(self, bQuit=False):
        """Cleanup reference held in the log handler"""
        self._oMainWindow.gui_log_handler.unset_widget()
        super(LogViewFrame, self).cleanup(bQuit)

    def get_menu_name(self):
        """Get the menu key"""
        return self._sName

    def set_filter_level(self, iNewLevel):
        """Set the filter level and reload the messages"""
        self._oView.set_filter_level(iNewLevel)
        self.reload()