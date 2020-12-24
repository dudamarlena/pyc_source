# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/welcomePanel.py
# Compiled at: 2009-05-29 13:49:10
import wx, wx.lib.fancytext as fancytext
from string import center
import epscComp.config

class WelcomePanel(wx.Panel):
    """
        Default panel in the center position
    """

    def __init__(self, *args, **kwds):
        kwds['style'] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        png = wx.Image(epscComp.config.dirImages + 'scmFront.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.stImage = wx.StaticBitmap(self, -1, png, (10, 10), (png.GetWidth(), png.GetHeight()))
        self.__do_layout()

    def setProperties(self):
        pass

    def __do_layout(self):
        sizer_0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.stImage, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ADJUST_MINSIZE, 0)
        sizer_0.Add(sizer_1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ADJUST_MINSIZE, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_0)

    def refresh(self):
        pass