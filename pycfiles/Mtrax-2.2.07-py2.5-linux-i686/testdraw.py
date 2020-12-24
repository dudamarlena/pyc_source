# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/testdraw.py
# Compiled at: 2008-02-04 19:11:54
import wx
from wx import xrc
import motmot.wxvideo.wxvideo as wxvideo, pkg_resources, numpy as nx, movies, imagesk
RSRC_FILE = pkg_resources.resource_filename(__name__, 'test.xrc')

class TestDrawApp(wx.App):

    def OnInit(self):
        rsrc = xrc.XmlResource(RSRC_FILE)
        self.frame = rsrc.LoadFrame(None, 'FRAME')
        self.frame.Show()
        self.img_panel = xrc.XRCCTRL(self.frame, 'PANEL')
        box = wx.BoxSizer(wx.VERTICAL)
        self.img_panel.SetSizer(box)
        self.img_wind = wxvideo.DynamicImageCanvas(self.img_panel, -1)
        self.img_wind.set_resize(True)
        box.Add(self.img_wind, 1, wx.EXPAND)
        self.img_panel.SetAutoLayout(True)
        self.img_panel.Layout()
        wx.EVT_LEFT_DOWN(self.img_wind, self.MouseClick)
        self.filename = '/home/kristin/FLIES/data/walking_arena/movie20071009_155327.sbfmf'
        self.movie = movies.Movie(self.filename, True)
        (imd, stamp) = self.movie.get_frame(1)
        print 'imd = ' + str(imd)
        print 'minv = ' + str(nx.min(imd))
        im8 = imagesk.double2mono8(imd)
        print 'im8 = ' + str(im8)
        print 'minv = ' + str(nx.min(im8))
        print 'im8.shape = ' + str(im8.shape)
        point = [
         [
          500, 500]]
        line = [[250, 250, 750, 750]]
        pointcolors = [(1, 0, 0)]
        linecolors = [(1, 1, 0)]
        self.img_wind.update_image_and_drawings('camera', im8, format='MONO8', linesegs=line, points=point, point_colors=pointcolors, lineseg_colors=linecolors)
        return True

    def MouseClick(self, evt):
        print 'mouse clicked'


def main():
    app = TestDrawApp(0)
    app.MainLoop()


if __name__ == '__main__':
    main()