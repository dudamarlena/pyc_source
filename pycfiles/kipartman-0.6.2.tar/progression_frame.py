# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/progression_frame.py
# Compiled at: 2017-10-01 05:26:02
from dialogs.dialog_progression import DialogProgression
import wx

class ProgressionFrame(DialogProgression):

    def __init__(self, parent, title):
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(ProgressionFrame, self).__init__(parent)
        self.SetTitle(title)
        self.canceled = False
        self.result = None
        return

    def SetProgression(self, caption, current_item, max_item):
        self.static_progression.Label = '%s (%d / %d)' % (caption, current_item, max_item)
        self.gauge_progression.SetRange(max_item)
        self.gauge_progression.SetValue(current_item)

    def Canceled(self):
        return self.canceled

    def onCancelButtonClick(self, event):
        self.canceled = True