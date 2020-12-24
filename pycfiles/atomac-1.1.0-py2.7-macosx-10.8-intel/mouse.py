# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/mouse.py
# Compiled at: 2012-12-07 15:18:39
"""Mouse class."""
from utils import Utils
from server_exception import LdtpServerException

class Mouse(Utils):

    def mouseleftclick(self, window_name, object_name):
        """
        Mouse left click on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        self._grabfocus(object_handle)
        x, y, width, height = self._getobjectsize(object_handle)
        object_handle.clickMouseButtonLeft((x + width / 2, y + height / 2))
        return 1

    def mouserightclick(self, window_name, object_name):
        """
        Mouse right click on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        self._grabfocus(object_handle)
        x, y, width, height = self._getobjectsize(object_handle)
        object_handle.clickMouseButtonRight((x + width / 2, y + height / 2))
        return 1

    def generatemouseevent(self, x, y, eventType='b1c'):
        """
        Generate mouse event on x, y co-ordinates.
        
        @param x: X co-ordinate
        @type x: int
        @param y: Y co-ordinate
        @type y: int
        @param eventType: Mouse click type
        @type eventType: string

        @return: 1 on success.
        @rtype: integer
        """
        if eventType == 'b1c':
            window = self._get_front_most_window()
            window.clickMouseButtonLeft((x, y))
            return 1
        if eventType == 'b3c':
            window = self._get_front_most_window()
            window.clickMouseButtonRight((x, y))
            return 1
        if eventType == 'b1d':
            window = self._get_front_most_window()
            window.doubleClickMouse((x, y))
            return 1
        raise LdtpServerException('Not implemented')

    def mousemove(self, window_name, object_name):
        """
        Mouse move on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')

    def doubleclick(self, window_name, object_name):
        """
        Double click on the object
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        self._grabfocus(object_handle)
        x, y, width, height = self._getobjectsize(object_handle)
        window = self._get_front_most_window()
        window.doubleClickMouse((x + width / 2, y + height / 2))
        return 1

    def simulatemousemove(self, source_x, source_y, dest_x, dest_y, delay=0.0):
        """
        @param source_x: Source X
        @type source_x: integer
        @param source_y: Source Y
        @type source_y: integer
        @param dest_x: Dest X
        @type dest_x: integer
        @param dest_y: Dest Y
        @type dest_y: integer
        @param delay: Sleep time between the mouse move
        @type delay: double

        @return: 1 if simulation was successful, 0 if not.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')