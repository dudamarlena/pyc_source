# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/native_select.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a simple drop-down select."""
from muntjac.ui.abstract_select import AbstractSelect
from muntjac.data.container import IContainer

class NativeSelect(AbstractSelect):
    """This is a simple drop-down select without, for instance, support
    for multiselect, new items, lazyloading, and other advanced features.
    Sometimes "native" select without all the bells-and-whistles of the
    ComboBox is a better choice.
    """
    CLIENT_WIDGET = None

    def __init__(self, *args):
        self._columns = 0
        args = args
        nargs = len(args)
        if nargs == 0:
            super(NativeSelect, self).__init__()
        elif nargs == 1:
            caption, = args
            super(NativeSelect, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], IContainer):
                caption, dataSource = args
                super(NativeSelect, self).__init__(caption, dataSource)
            else:
                caption, options = args
                super(NativeSelect, self).__init__(caption, options)
        else:
            raise ValueError, 'too many arguments'

    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns
        is set 0, the actual number of displayed columns is determined
        implicitly by the adapter.

        @param columns:
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0
        if self._columns != columns:
            self._columns = columns
            self.requestRepaint()

    def getColumns(self):
        return self._columns

    def paintContent(self, target):
        target.addAttribute('type', 'native')
        if self._columns != 0:
            target.addAttribute('cols', self._columns)
        super(NativeSelect, self).paintContent(target)

    def setMultiSelect(self, multiSelect):
        if multiSelect == True:
            raise NotImplementedError, 'Multiselect not supported'

    def setNewItemsAllowed(self, allowNewOptions):
        if allowNewOptions == True:
            raise NotImplementedError, 'newItemsAllowed not supported'