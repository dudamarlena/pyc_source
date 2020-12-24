# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/com/dtmilano/android/robotframework/viewclientwrapper.py
# Compiled at: 2019-10-11 02:14:01
__doc__ = '\nCopyright (C) 2012-2018  Diego Torres Milano\nCreated on Nov 10, 2015\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n\n@author: Diego Torres Milano\n'
__version__ = '15.8.1'
__author__ = 'diego'
import sys
from com.dtmilano.android.viewclient import ViewClient
DEBUG = False
ROBOT_LIBRARY_DOC_FORMAT = 'reST'

class ViewClientWrapper:

    def __init__(self, serialno):
        device, serialno = ViewClient.connectToDeviceOrExit(serialno=serialno)
        self.vc = ViewClient(device, serialno)
        self.device = device
        if DEBUG:
            print >> sys.stderr, 'ViewClientWrapper: connected to', device, serialno

    def dump(self):
        """Dumps window hierarchy."""
        return self.vc.dump()

    def touch(self, x, y):
        """Touches a point.

        :param x: x
        :param y: y
        :return:
        """
        return self.vc.touch(x, y)

    @staticmethod
    def long_touch_view(view):
        """Long-touches the view."""
        return view.longTouch()

    @staticmethod
    def touch_view(view):
        """Touches the View"""
        return view.touch()

    @staticmethod
    def get_view_position_and_size(view):
        """ Gets the View position and size
        :param view: the View
        :return: the position and size
        """
        return view.getPositionAndSize()

    def find_view_with_text(self, text):
        return self.vc.findViewWithText(text)

    def find_view_by_id(self, id):
        return self.vc.findViewById(id)

    def start_activity(self, component):
        """Starts Activity."""
        return self.vc.device.startActivity(component)

    def get_top_activity_name(self):
        return self.device.getTopActivityName()

    def force_stop_package(self, package):
        self.device.shell('am force-stop %s' % package)

    def get_windows(self):
        return self.device.getWindows()

    def is_keyboard_show(self):
        return self.device.isKeyboardShown()