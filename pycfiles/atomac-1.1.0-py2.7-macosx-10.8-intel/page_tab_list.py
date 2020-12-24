# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/page_tab_list.py
# Compiled at: 2012-10-05 17:37:25
"""PageTabList class."""
import re, fnmatch
from utils import Utils
from server_exception import LdtpServerException

class PageTabList(Utils):

    def _get_tab_children(self, window_name, object_name):
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle:
            raise LdtpServerException('Unable to find object %s' % object_name)
        return object_handle.AXChildren

    def _get_tab_handle(self, window_name, object_name, tab_name):
        children = self._get_tab_children(window_name, object_name)
        tab_handle = None
        for current_tab in children:
            role, label = self._ldtpize_accessible(current_tab)
            tmp_tab_name = fnmatch.translate(tab_name)
            if re.match(tmp_tab_name, label) or re.match(tmp_tab_name, '%s%s' % (role, label)):
                tab_handle = current_tab
                break

        if not tab_handle:
            raise LdtpServerException('Unable to find tab %s' % tab_name)
        if not tab_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        return tab_handle

    def selecttab(self, window_name, object_name, tab_name):
        """
        Select tab based on name.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_name: tab to select
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        tab_handle = self._get_tab_handle(window_name, object_name, tab_name)
        tab_handle.Press()
        return 1

    def selecttabindex(self, window_name, object_name, tab_index):
        """
        Select tab based on index.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_index: tab to select
        @type data: integer

        @return: 1 on success.
        @rtype: integer
        """
        children = self._get_tab_children(window_name, object_name)
        length = len(children)
        if tab_index < 0 or tab_index > length:
            raise LdtpServerException('Invalid tab index %s' % tab_index)
        tab_handle = children[tab_index]
        if not tab_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        tab_handle.Press()
        return 1

    def verifytabname(self, window_name, object_name, tab_name):
        """
        Verify tab name.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_name: tab to select
        @type data: string

        @return: 1 on success 0 on failure
        @rtype: integer
        """
        try:
            tab_handle = self._get_tab_handle(window_name, object_name, tab_name)
            if tab_handle.AXValue:
                return 1
        except LdtpServerException:
            pass

        return 0

    def gettabcount(self, window_name, object_name):
        """
        Get tab count.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: tab count on success.
        @rtype: integer
        """
        children = self._get_tab_children(window_name, object_name)
        return len(children)

    def gettabname(self, window_name, object_name, tab_index):
        """
        Get tab name
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_index: Index of tab (zero based index)
        @type object_name: int

        @return: text on success.
        @rtype: string
        """
        children = self._get_tab_children(window_name, object_name)
        length = len(children)
        if tab_index < 0 or tab_index > length:
            raise LdtpServerException('Invalid tab index %s' % tab_index)
        tab_handle = children[tab_index]
        if not tab_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        return tab_handle.AXTitle