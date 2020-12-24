# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/combo_box.py
# Compiled at: 2013-02-13 13:37:18
"""Combobox class."""
import re
from atomac import AXKeyCodeConstants
from utils import Utils
from server_exception import LdtpServerException

class ComboBox(Utils):

    def selectitem(self, window_name, object_name, item_name):
        """
        Select combo box / layered pane item
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_name: Item name to select
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        self._grabfocus(object_handle.AXWindow)
        try:
            object_handle.Press()
        except AttributeError:
            x, y, width, height = self._getobjectsize(object_handle)
            self.generatemouseevent(x + 5, y + 5, 'b1c')
            self.wait(5)
            handle = self._get_sub_menu_handle(object_handle, item_name)
            x, y, width, height = self._getobjectsize(handle)
            self.generatemouseevent(x + 5, y + 5, 'b1d')
            return 1

        self.wait(1)
        menu_list = re.split(';', item_name)
        try:
            menu_handle = self._internal_menu_handler(object_handle, menu_list, True)
            self.wait(1)
            if not menu_handle.AXEnabled:
                raise LdtpServerException('Object %s state disabled' % menu_list[(-1)])
            menu_handle.Press()
        except LdtpServerException:
            object_handle.activate()
            object_handle.sendKey(AXKeyCodeConstants.ESCAPE)
            raise

        return 1

    comboselect = selectitem

    def selectindex(self, window_name, object_name, item_index):
        """
        Select combo box item / layered pane based on index
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_index: Item index to select
        @type object_name: integer

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        self._grabfocus(object_handle.AXWindow)
        try:
            object_handle.Press()
        except AttributeError:
            x, y, width, height = self._getobjectsize(object_handle)
            self.generatemouseevent(x + 5, y + 5, 'b1c')

        self.wait(2)
        if not object_handle.AXChildren:
            raise LdtpServerException('Unable to find menu')
        children = object_handle.AXChildren[0]
        if not children:
            raise LdtpServerException('Unable to find menu')
        children = children.AXChildren
        tmp_children = []
        for child in children:
            role, label = self._ldtpize_accessible(child)
            if label:
                tmp_children.append(child)

        children = tmp_children
        length = len(children)
        try:
            if item_index < 0 or item_index > length:
                raise LdtpServerException('Invalid item index %d' % item_index)
            menu_handle = children[item_index]
            if not menu_handle.AXEnabled:
                raise LdtpServerException('Object %s state disabled' % menu_list[(-1)])
            self._grabfocus(menu_handle)
            x, y, width, height = self._getobjectsize(menu_handle)
            window = object_handle.AXWindow
            window.doubleClickMouse((x + 5, y + 5))
            child = None
        finally:
            if child:
                child.Cancel()

        return 1

    comboselectindex = selectindex

    def getallitem(self, window_name, object_name):
        """
        Get all combo box item

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: list of string on success.
        @rtype: list
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        object_handle.Press()
        self.wait(1)
        child = None
        try:
            if not object_handle.AXChildren:
                raise LdtpServerException('Unable to find menu')
            children = object_handle.AXChildren[0]
            if not children:
                raise LdtpServerException('Unable to find menu')
            children = children.AXChildren
            items = []
            for child in children:
                label = self._get_title(child)
                if label:
                    items.append(label)

        finally:
            if child:
                child.Cancel()

        return items

    def showlist(self, window_name, object_name):
        """
        Show combo box list / menu
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        object_handle.Press()
        return 1

    def hidelist(self, window_name, object_name):
        """
        Hide combo box list / menu
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        object_handle.activate()
        object_handle.sendKey(AXKeyCodeConstants.ESCAPE)
        return 1

    def verifydropdown(self, window_name, object_name):
        """
        Verify drop down list / menu poped up
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled or not object_handle.AXChildren:
                return 0
            children = object_handle.AXChildren[0]
            if children:
                return 1
        except LdtpServerException:
            pass

        return 0

    def verifyshowlist(self, window_name, object_name):
        """
        Verify drop down list / menu poped up
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        return self.verifydropdown(window_name, object_name)

    def verifyhidelist(self, window_name, object_name):
        """
        Verify list / menu is hidden in combo box
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled:
                return 0
            if not object_handle.AXChildren:
                return 1
            children = object_handle.AXChildren[0]
            if not children:
                return 1
            return 1
        except LdtpServerException:
            pass

        return 0

    def verifyselect(self, window_name, object_name, item_name):
        """
        Verify the item selected in combo box
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_name: Item name to select
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled:
                return 0
            role, label = self._ldtpize_accessible(object_handle)
            title = self._get_title(object_handle)
            if re.match(item_name, title, re.M | re.U | re.L) or re.match(item_name, label, re.M | re.U | re.L) or re.match(item_name, '%u%u' % (role, label), re.M | re.U | re.L):
                return 1
        except LdtpServerException:
            pass

        return 0

    def getcombovalue(self, window_name, object_name):
        """
        Get current selected combobox value
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: selected item on success, else LdtpExecutionError on failure.
        @rtype: string
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        return self._get_title(object_handle)