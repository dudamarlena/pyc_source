# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/text_area.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a text field that supports multi-line editing."""
from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty

class TextArea(AbstractTextField):
    """A text field that supports multi line editing."""
    CLIENT_WIDGET = None
    _DEFAULT_ROWS = 5

    def __init__(self, *args):
        """Constructs a TextArea with an optional caption, data source,
        and/or value.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption for the field
            - (dataSource)
              1. the data source for the field
            - (caption, dataSource)
              1. the caption for the field
              2. the data source for the field
            - (caption, value)
              1. the caption for the field
              2. the value for the field
        """
        self._rows = self._DEFAULT_ROWS
        self._wordwrap = True
        nargs = len(args)
        if nargs == 0:
            super(TextArea, self).__init__()
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                TextArea.__init__(self)
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                TextArea.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                TextArea.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                TextArea.__init__(self, caption)
                self.setValue(value)
        else:
            raise ValueError, 'too many arguments'

    def setRows(self, rows):
        """Sets the number of rows in the text area.

        @param rows: the number of rows for this text area.
        """
        if rows < 0:
            rows = 0
        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()

    def getRows(self):
        """Gets the number of rows in the text area.

        @return: number of explicitly set rows.
        """
        return self._rows

    def setWordwrap(self, wordwrap):
        """Sets the text area's word-wrap mode on or off.

        @param wordwrap:
                   the boolean value specifying if the text area should be
                   in word-wrap mode.
        """
        if self._wordwrap != wordwrap:
            self._wordwrap = wordwrap
            self.requestRepaint()

    def isWordwrap(self):
        """Tests if the text area is in word-wrap mode.

        @return: C{True} if the component is in word-wrap mode,
                 C{False} if not.
        """
        return self._wordwrap

    def paintContent(self, target):
        super(TextArea, self).paintContent(target)
        target.addAttribute('rows', self.getRows())
        if not self.isWordwrap():
            target.addAttribute('wordwrap', False)