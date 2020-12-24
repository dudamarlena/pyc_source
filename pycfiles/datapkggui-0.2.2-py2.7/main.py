# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datapkggui/main.py
# Compiled at: 2011-10-24 15:04:23
__author__ = 'dgraziotin'
import sys, wx, wx.xrc, gui.maingui, pkg_resources

class Datapkg(wx.App):

    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        xml = wx.xrc.XmlResource(pkg_resources.resource_filename('datapkggui.res', 'datapkggui.xrc'))
        self.MainGUI = gui.maingui.MainGUI(xml)
        return True


class SysOutListener:

    def write(self, string):
        sys.__stdout__.write(string)
        evt = gui.maingui.WX_STDOUT(text=string)
        wx.PostEvent(wx.GetApp().MainGUI.m_console_text, evt)

    def flush(self):
        sys.__stdout__.flush()


def run():
    sysout_listener = SysOutListener()
    app = Datapkg(0)
    app.SetAppName('Datapkg')
    sys.stdout = sysout_listener
    app.MainLoop()


if __name__ == '__main__':
    run()