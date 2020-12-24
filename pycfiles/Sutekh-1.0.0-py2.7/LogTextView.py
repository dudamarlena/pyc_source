# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/LogTextView.py
# Compiled at: 2019-12-11 16:37:48
"""Widget for displaying the card text for the given card."""
import logging, gtk

class LogTextBuffer(gtk.TextBuffer):
    """Text buffer for displaying log messages.
       """

    def __init__(self):
        super(LogTextBuffer, self).__init__(None)
        return

    def clear(self):
        """Clear all messages"""
        oStart, oEnd = self.get_bounds()
        self.delete(oStart, oEnd)

    def add_message(self, sMessage):
        """Append a message to the log"""
        oEnd = self.get_end_iter()
        self.insert(oEnd, sMessage)
        self.insert(oEnd, '\n')

    def get_all_text(self):
        """Get everything shown in the buffer"""
        oStart, oEnd = self.get_bounds()
        return self.get_text(oStart, oEnd)


class LogTextView(gtk.TextView):
    """TextView widget which holds the LogTextBuffer."""

    def __init__(self):
        super(LogTextView, self).__init__()
        self._oBuf = LogTextBuffer()
        self.set_buffer(self._oBuf)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_wrap_mode(gtk.WRAP_WORD)
        self._iFilterLevel = logging.NOTSET

    def set_log_messages(self, aMessages):
        """Populate the TextBuffer with the messages, honouring
           the filter level"""
        self._oBuf.clear()
        for tMessage in aMessages:
            if tMessage[0] >= self._iFilterLevel:
                self._oBuf.add_message(tMessage[1])

    def export_buffer(self, oFile):
        """Export all the text from the buffer to the given file object"""
        sData = self._oBuf.get_all_text()
        oFile.write(sData.encode('utf8'))

    def save_to_file(self, sFileName):
        """Handling opening a file and passing it to _export_buffer"""
        if sFileName:
            with open(sFileName, 'wb') as (oFile):
                self.export_buffer(oFile)

    def set_filter_level(self, iNewLevel):
        """Update the filter level."""
        self._iFilterLevel = iNewLevel