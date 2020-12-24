# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/frontend/window_webcam.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 2532 bytes
import logging
logger = logging.getLogger('Window Webcam')
from gi.repository import Gtk, GObject, Gdk, GdkX11
from kazam.backend.prefs import *

class WebcamWindow(GObject.GObject):

    def __init__(self, width, height, position):
        super(WebcamWindow, self).__init__()
        logger.debug('Initializing Webcam window.')
        self.xid = None
        self.window = Gtk.Window()
        self.window.set_default_size(width, height)
        self.webcam_area = Gtk.DrawingArea()
        self.window.add(self.webcam_area)
        self.window.set_decorated(False)
        self.window.set_property('skip-taskbar-hint', True)
        self.window.set_keep_above(True)
        self.window.show_all()
        screen = HW.screens[prefs.current_screen]
        self.window.set_size_request(width, height)
        if position == CAM_PREVIEW_TL:
            self.window.set_gravity(Gdk.Gravity.NORTH_WEST)
            self.window.move(screen['x'], screen['y'])
        else:
            if position == CAM_PREVIEW_TR:
                self.window.set_gravity(Gdk.Gravity.NORTH_EAST)
                self.window.move(screen['x'] + screen['width'] - width, screen['y'])
            else:
                if position == CAM_PREVIEW_BR:
                    self.window.set_gravity(Gdk.Gravity.SOUTH_EAST)
                    self.window.move(screen['x'] + screen['width'] - width, screen['y'] + screen['height'] - height)
                else:
                    if position == CAM_PREVIEW_BL:
                        self.window.set_gravity(Gdk.Gravity.SOUTH_WEST)
                        self.window.move(screen['x'], screen['y'] + screen['height'] - height)
                    else:
                        self.xid = self.webcam_area.get_property('window').get_xid()