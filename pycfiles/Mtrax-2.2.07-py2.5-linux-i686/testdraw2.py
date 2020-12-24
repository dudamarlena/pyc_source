# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/testdraw2.py
# Compiled at: 2008-01-31 15:27:32
import matplotlib
matplotlib.use('WXAgg')
import wx
from wx import xrc
import wx.glcanvas as wxvideo, pkg_resources, numpy as nx, movies, imagesk
RSRC_FILE = pkg_resources.resource_filename(__name__, 'test.xrc')

class TestDrawApp(wx.App):

    def OnInit(self):
        rsrc = xrc.XmlResource(RSRC_FILE)
        self.frame = rsrc.LoadFrame(None, 'FRAME')
        self.frame.Show()
        self.img_panel = xrc.XRCCTRL(self.frame, 'PANEL')
        box = wx.BoxSizer(wx.VERTICAL)
        self.img_panel.SetSizer(box)
        self.img_wind = wxvideo.GLCanvas(self.img_panel, -1)
        box.Add(self.img_wind, 1, wx.EXPAND)
        self.img_panel.SetAutoLayout(True)
        self.img_panel.Layout()
        wx.EVT_LEFT_DOWN(self.img_wind, self.MouseClick)
        return True

    def MouseClick(self, evt):
        print 'mouse clicked'


def main():
    app = TestDrawApp(0)
    app.MainLoop()


if __name__ == '__main__':
    main()