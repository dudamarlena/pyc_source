# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/table.py
# Compiled at: 2013-02-13 13:37:18
"""Mouse class."""
import re, fnmatch
from utils import Utils
from server_exception import LdtpServerException

class Table(Utils):

    def getrowcount(self, window_name, object_name):
        """
        Get count of rows in table object.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: Number of rows.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        return len(object_handle.AXRows)

    def selectrow(self, window_name, object_name, row_text):
        """
        Select row

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to select
        @type row_text: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        for cell in object_handle.AXRows:
            if re.match(row_text, cell.AXChildren[0].AXValue):
                if not cell.AXSelected:
                    object_handle.activate()
                    cell.AXSelected = True
                return 1

        raise LdtpServerException('Unable to select row: %s' % row_text)

    def selectrowpartialmatch(self, window_name, object_name, row_text):
        """
        Select row partial match

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to select
        @type row_text: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        for cell in object_handle.AXRows:
            if re.search(row_text, cell.AXChildren[0].AXValue):
                if not cell.AXSelected:
                    object_handle.activate()
                    cell.AXSelected = True
                return 1

        raise LdtpServerException('Unable to select row: %s' % row_text)

    def selectrowindex(self, window_name, object_name, row_index):
        """
        Select row index

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to select
        @type row_index: integer

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        count = len(object_handle.AXRows)
        if row_index < 0 or row_index > count:
            raise LdtpServerException('Row index out of range: %d' % row_index)
        cell = object_handle.AXRows[row_index]
        if not cell.AXSelected:
            object_handle.activate()
            cell.AXSelected = True
        return 1

    def selectlastrow(self, window_name, object_name):
        """
        Select last row

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
        cell = object_handle.AXRows[(-1)]
        if not cell.AXSelected:
            object_handle.activate()
            cell.AXSelected = True
        return 1

    def setcellvalue(self, window_name, object_name, row_index, column=0, data=None):
        """
        Set cell value

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer
        @param data: data, default value None
                None, used for toggle button
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')

    def getcellvalue(self, window_name, object_name, row_index, column=0):
        """
        Get cell value

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer

        @return: cell value on success.
        @rtype: string
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        count = len(object_handle.AXRows)
        if row_index < 0 or row_index > count:
            raise LdtpServerException('Row index out of range: %d' % row_index)
        cell = object_handle.AXRows[row_index]
        count = len(cell.AXChildren)
        if column < 0 or column > count:
            raise LdtpServerException('Column index out of range: %d' % column)
        obj = cell.AXChildren[column]
        if not re.search('AXColumn', obj.AXRole):
            obj = cell.AXChildren[column]
        return obj.AXValue

    def getcellsize(self, window_name, object_name, row_index, column=0):
        """
        Get cell size

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer

        @return: cell coordinates on success.
        @rtype: list
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        count = len(object_handle.AXRows)
        if row_index < 0 or row_index > count:
            raise LdtpServerException('Row index out of range: %d' % row_index)
        cell = object_handle.AXRows[row_index]
        count = len(cell.AXChildren)
        if column < 0 or column > count:
            raise LdtpServerException('Column index out of range: %d' % column)
        obj = cell.AXChildren[column]
        if not re.search('AXColumn', obj.AXRole):
            obj = cell.AXChildren[column]
        return self._getobjectsize(obj)

    def rightclick(self, window_name, object_name, row_text):
        """
        Right click on table cell

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to right click
        @type row_text: string

        @return: 1 on success.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')

    def checkrow(self, window_name, object_name, row_index, column=0):
        """
        Check row

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer

        @return: cell value on success.
        @rtype: string
        """
        raise LdtpServerException('Not implemented')

    def expandtablecell(self, window_name, object_name, row_index, column=0):
        """
        Expand or contract table cell

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer

        @return: cell value on success.
        @rtype: string
        """
        raise LdtpServerException('Not implemented')

    def uncheckrow(self, window_name, object_name, row_index, column=0):
        """
        Check row

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer

        @return: 1 on success.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')

    def gettablerowindex(self, window_name, object_name, row_text):
        """
        Get table row index matching given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to select
        @type row_text: string

        @return: row index matching the text on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException('Object %s state disabled' % object_name)
        index = 0
        for cell in object_handle.AXRows:
            if re.match(row_text, cell.AXChildren[0].AXValue):
                return index
            index += 1

        raise LdtpServerException('Unable to find row: %s' % row_text)

    def singleclickrow(self, window_name, object_name, row_text):
        """
        Single click row matching given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to select
        @type row_text: string

        @return: row index matching the text on success.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')

    def doubleclickrow(self, window_name, object_name, row_text):
        """
        Double click row matching given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to select
        @type row_text: string

        @return: row index matching the text on success.
        @rtype: integer
        """
        raise LdtpServerException('Not implemented')

    def verifytablecell(self, window_name, object_name, row_index, column_index, row_text):
        """
        Verify table cell value with given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column_index: Column index to get, default value 0
        @type column_index: integer
        @param row_text: Row text to match
        @type string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            value = getcellvalue(window_name, object_name, row_index, column_index)
            if re.match(row_text, value):
                return 1
        except LdtpServerException:
            pass

        return 0

    def doesrowexist(self, window_name, object_name, row_text, partial_match=False):
        """
        Verify table cell value with given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to match
        @type string
        @param partial_match: Find partial match strings
        @type boolean

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled:
                return 0
            for cell in object_handle.AXRows:
                if not partial_match and re.match(row_text, cell.AXChildren[0].AXValue):
                    return 1
                if partial_match and re.search(row_text, cell.AXChildren[0].AXValue):
                    return 1

        except LdtpServerException:
            pass

        return 0

    def verifypartialtablecell(self, window_name, object_name, row_index, column_index, row_text):
        """
        Verify partial table cell value

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column_index: Column index to get, default value 0
        @type column_index: integer
        @param row_text: Row text to match
        @type string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            value = getcellvalue(window_name, object_name, row_index, column_index)
            if re.searchmatch(row_text, value):
                return 1
        except LdtpServerException:
            pass

        return 0