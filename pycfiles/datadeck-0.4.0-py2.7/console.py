# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datadeck/gui/util/console.py
# Compiled at: 2011-11-23 15:22:22


class ConsoleUtil(object):
    """
    GUI utilities for the Console
    """

    def __init__(self, wxframe):
        self.m_wxframe = wxframe

    def OnUpdateConsole(self, event):
        """
        Update the Console text
        """
        value = event.text
        self.m_wxframe.m_console_tc.AppendText(value)

    def OnProcessPendingEventsConsole(self, event):
        """
        Handle pending events
        """
        self.m_wxframe.m_console_tc.ProcessPendingEvents()

    def OnConsoleClearButtonClick(self, event):
        self.m_wxframe.m_console_tc.Clear()

    def OnConsoleClearButtonClick(self, event):
        self.m_wxframe.m_console_tc.Clear()