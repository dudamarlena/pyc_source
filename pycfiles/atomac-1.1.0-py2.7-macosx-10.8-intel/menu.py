# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/menu.py
# Compiled at: 2013-02-13 13:37:18
"""Menu class."""
import re, atomac
from utils import Utils
from server_exception import LdtpServerException

class Menu(Utils):

    def _get_menu_handle(self, window_name, object_name, wait_for_window=True):
        menu_list = re.split(';', object_name)
        try:
            menu_handle = Utils._get_menu_handle(self, window_name, menu_list[0], wait_for_window)
        except (atomac._a11y.ErrorCannotComplete, atomac._a11y.ErrorInvalidUIElement):
            self._windows = {}
            menu_handle = Utils._get_menu_handle(self, window_name, menu_list[0], wait_for_window)

        if len(menu_list) <= 1:
            return menu_handle
        return self._internal_menu_handler(menu_handle, menu_list[1:])

    def selectmenuitem(self, window_name, object_name):
        """
        Select (click) a menu item.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        menu_handle = self._get_menu_handle(window_name, object_name)
        if not menu_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        menu_handle.Press()
        return 1

    def doesmenuitemexist(self, window_name, object_name):
        """
        Check a menu item exist.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string
        @param strict_hierarchy: Mandate menu hierarchy if set to True
        @type object_name: boolean

        @return: 1 on success.
        @rtype: integer
        """
        try:
            menu_handle = self._get_menu_handle(window_name, object_name, False)
            return 1
        except LdtpServerException:
            return 0

    def menuitemenabled(self, window_name, object_name):
        """
        Verify a menu item is enabled

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            menu_handle = self._get_menu_handle(window_name, object_name, False)
            if menu_handle.AXEnabled:
                return 1
        except LdtpServerException:
            pass

        return 0

    def listsubmenus(self, window_name, object_name):
        """
        List children of menu item
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: menu item in list on success.
        @rtype: list
        """
        menu_handle = self._get_menu_handle(window_name, object_name)
        role, label = self._ldtpize_accessible(menu_handle)
        menu_clicked = False
        try:
            if not menu_handle.AXChildren:
                menu_clicked = True
                try:
                    menu_handle.Press()
                    self.wait(1)
                except atomac._a11y.ErrorCannotComplete:
                    pass

                if not menu_handle.AXChildren:
                    raise LdtpServerException('Unable to find children under menu %s' % label)
            children = menu_handle.AXChildren[0]
            sub_menus = []
            for current_menu in children.AXChildren:
                role, label = self._ldtpize_accessible(current_menu)
                if not label:
                    continue
                sub_menus.append('%s%s' % (role, label))

        finally:
            if menu_clicked:
                menu_handle.Cancel()

        return sub_menus

    def verifymenucheck(self, window_name, object_name):
        """
        Verify a menu item is checked

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            menu_handle = self._get_menu_handle(window_name, object_name, False)
            try:
                if menu_handle.AXMenuItemMarkChar:
                    return 1
            except atomac._a11y.Error:
                pass

        except LdtpServerException:
            pass

        return 0

    def verifymenuuncheck(self, window_name, object_name):
        """
        Verify a menu item is un-checked

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            menu_handle = self._get_menu_handle(window_name, object_name, False)
            try:
                if not menu_handle.AXMenuItemMarkChar:
                    return 1
            except atomac._a11y.Error:
                return 1

        except LdtpServerException:
            pass

        return 0

    def menucheck(self, window_name, object_name):
        """
        Check (click) a menu item.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        menu_handle = self._get_menu_handle(window_name, object_name)
        if not menu_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        try:
            if menu_handle.AXMenuItemMarkChar:
                return 1
        except atomac._a11y.Error:
            pass

        menu_handle.Press()
        return 1

    def menuuncheck(self, window_name, object_name):
        """
        Uncheck (click) a menu item.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        menu_handle = self._get_menu_handle(window_name, object_name)
        if not menu_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        try:
            if not menu_handle.AXMenuItemMarkChar:
                return 1
        except atomac._a11y.Error:
            return 1

        menu_handle.Press()
        return 1