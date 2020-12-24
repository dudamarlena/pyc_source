# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjama/gui/hildon/pyjamaGui.py
# Compiled at: 2012-01-06 12:40:54
"""
Created on Oct 14, 2011

@author: maemo

"""
import gtk, hildon, logging, os.path, logging, time, datetime, pango, urllib
from pyjama.gui.gtk.widget import *
from pyjama.gui.hildon.widget import *
from pyjama.gui.gtk.utils import fill_widget_with_logo, LOGO_PIXBUF
from pyjama.gui.hildon.utils import show_about_dialog, call_handled_method, not_yet_implemented, PyjamaStackableWindow, ASYNC_EXCEPTION_HANDLER_INSTANCE, AsyncTask, StopSignalException, show_banner_information, show_note_information
from pyjama.core import facade
from pyjama.common import version
version.getInstance().submitRevision('$Revision: 139 $')
from pyjama.gui.hildon.portrait import FremantleRotation
gtk.gdk.threads_init()

def show_new_window(window):
    program = hildon.Program.get_instance()
    program.add_window(window)
    window.show_all()


def show_album_list_view(facade):
    window = AlbumListView(facade)
    show_new_window(window)


def show_feed_list_view(facade):
    window = LastPictureView(facade)
    show_new_window(window)


class pyjamaGui(object):
    """
    This is the GUI of gnatirac
    """
    _last_folder = None

    def __init__(self):
        """
        Create a new application GUI
        """
        self.program = hildon.Program.get_instance()
        self.facade = facade.pyjama()
        ASYNC_EXCEPTION_HANDLER_INSTANCE.start_async_exception_handler()
        self.init_main_view()

    def init_main_view(self):
        """
        create a new window for the main view of the application
        """
        window = SplashScreenView(self.facade)
        window.connect('destroy', self.quit_application, None)
        show_new_window(window)
        FremantleRotation('Pyjama', main_window=window)
        if self.facade.connected:
            show_album_list_view(self.facade)
        return

    def quit_application(self, widget, data):
        ASYNC_EXCEPTION_HANDLER_INSTANCE.stop_async_exception_handler()
        gtk.main_quit()

    def run(self):
        gtk.main()


class SplashScreenView(PyjamaStackableWindow):
    """
    This is the first view of the application e.g. the main view.  
    """

    def __init__(self, facade):
        self.facade = facade
        PyjamaStackableWindow.__init__(self)

    def init_center_view(self, centerview):
        fill_widget_with_logo(centerview)

    def init_menu(self, menu):
        pass