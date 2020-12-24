# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\WX\pidWX.py
# Compiled at: 2008-04-09 17:20:41
"""WXCanvas

This class implements a Sping plug-in drawing Canvas object that draws using wxPython, the
wxWindows Python language bindings into a GUI window.
"""
import wx
from pidWxDc import SpingWxDc
__version__ = '1.0'
__date__ = 'February 6, 2000'
__author__ = 'Paul & Kevin Jacobs'

class _WXCanvasDefaultStatusBar(wx.StatusBar):
    """
    This status bar displays clear and quit buttons, as well as the
    location of the mouse and whether the left button is down.
    """

    def __init__(self, canvas):
        wx.StatusBar.__init__(self, canvas.window, -1)
        self.closed = False
        self.Parent.Bind(wx.EVT_CLOSE, self.OnClose)
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetFieldsCount(3)
        self.quitButton = wx.Button(self, -1, 'Quit')
        self.clearButton = wx.Button(self, -1, 'Clear')
        self.click = wx.CheckBox(self, -1, 'Click')
        self.text = wx.StaticText(self, -1, '')
        self.Reposition()
        self.quitButton.Bind(wx.EVT_BUTTON, canvas._OnQuit)
        self.clearButton.Bind(wx.EVT_BUTTON, canvas._OnClear)

    def SetStatusText(self, s):
        self.text.SetLabel(s)

    def OnOver(self, x, y):
        self.SetStatusText(`x` + ',' + `y`)
        self.Refresh()

    def OnClick(self, x, y):
        self.SetStatusText(`x` + ',' + `y`)
        self.click.SetValue(True)
        self.Refresh()

    def OnLeaveWindow(self):
        self.click.SetValue(False)
        self.SetStatusText('')
        self.Refresh()

    def OnClose(self, evt):
        self.closed = True
        evt.Skip()

    def OnClickUp(self, x, y):
        self.click.SetValue(False)

    def OnSize(self, evt):
        self.Reposition()
        self.sizeChanged = True

    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()

    def Reposition(self):
        if self.closed:
            return
        field = self.GetFieldRect(0)
        self.quitButton.SetPosition(wx.Point(field.x, field.y))
        self.quitButton.SetSize(wx.Size(field.width / 2, field.height))
        self.clearButton.SetPosition(wx.Point(field.x + field.width / 2, field.y))
        self.clearButton.SetSize(wx.Size(field.width / 2, field.height))
        field = self.GetFieldRect(1)
        self.click.SetPosition(wx.Point(field.x, field.y))
        self.click.SetSize(wx.Size(field.width, field.height))
        field = self.GetFieldRect(2)
        self.text.SetPosition(wx.Point(field.x + 2, field.y + 2))
        self.sizeChanged = False


class WXCanvas(SpingWxDc):

    def __init__(self, size=(300, 300), name='spingWX', status_bar=None, interactive=True, show_status=True):
        """
        Works like all other Sping.pid canvases, except with extra interactive
        controls:

        interactive enables the interactive parts of the Sping.pid API
        show_status controls if the default status bar is shown
        """
        window = wx.Frame(None, -1, 'WXCanvas', wx.DefaultPosition, wx.Size(size[0], size[1]))
        window.Show(True)
        window.Raise()
        self.window = window
        CSize = window.GetClientSizeTuple()
        if show_status:
            status_area = 20
        else:
            status_area = 0
        window.SetSize(wx.Size(size[0] + (size[0] - CSize[0]), size[1] + (size[1] - CSize[1] + status_area)))
        bmp = wx.EmptyBitmap(size[0], size[1])
        MemDc = wx.MemoryDC()
        MemDc.SelectObject(bmp)
        MemDc.Clear()
        self.MemDc = MemDc
        SpingWxDc.__init__(self, MemDc, size, name)
        self.window = window
        self.size = size
        self.sb = status_bar if status_bar else _WXCanvasDefaultStatusBar(self)
        self.window.SetStatusBar(self.sb)
        self.sb.Show(show_status)

        def ignoreClick(canvas, x, y):
            canvas.sb.OnClick(x, y)

        self.onClick = ignoreClick

        def ignoreOver(canvas, x, y):
            canvas.sb.OnOver(x, y)

        self.onOver = ignoreOver

        def ignoreKey(canvas, key, modifiers):
            pass

        self.onKey = ignoreKey

        def ignoreClickUp(canvas, x, y):
            canvas.sb.OnClickUp(x, y)

        self.onClickUp = ignoreClickUp
        self.interactive = interactive
        wx.EVT_PAINT(window, self._OnPaint)
        wx.EVT_LEFT_DOWN(window, self._OnClick)
        wx.EVT_LEFT_UP(window, self._OnClickUp)
        wx.EVT_MOTION(window, self._OnOver)
        wx.EVT_CHAR(window, self._OnKey)
        wx.EVT_LEAVE_WINDOW(window, self._OnLeaveWindow)

        def leaveWindow(canvas):
            canvas.sb.OnLeaveWindow()

        self.onLeaveWindow = leaveWindow
        return

    def _OnClick(self, event):
        if self.interactive == False:
            return
        if event.GetY() <= self.size[1]:
            self.onClick(self, event.GetX(), event.GetY())
        return

    def _OnClickUp(self, event):
        if self.interactive == False:
            return
        self.onClickUp(self, event.GetX(), event.GetY())
        return

    def _OnOver(self, event):
        if self.interactive == False:
            return
        if event.GetY() <= self.size[1]:
            self.onOver(self, event.GetX(), event.GetY())
        return

    def _OnLeaveWindow(self, event):
        if self.interactive == False:
            return
        self.onLeaveWindow(self)
        return

    def _OnKey(self, event):
        code = event.KeyCode
        key = None
        if code >= 0 and code < 256:
            key = chr(event.KeyCode)
        modifier = []
        if event.ControlDown():
            modifier.append('modControl')
        if event.ShiftDown():
            modifier.append('modshift')
        self.onKey(self, key, tuple(modifier))
        return

    def _OnPaint(self, event):
        dc = wx.PaintDC(self.window)
        dc.Blit(0, 0, self.size[0], self.size[1], self.MemDc, 0, 0, wx.COPY)
        del dc

    def _OnQuit(self, event):
        """Closes the canvas.  Call to return control your application"""
        self.window.Close()

    def _OnClear(self, event):
        """Clears the canvas by emptying the memory buffer, and redrawing"""
        self.MemDc.Clear()
        dc = wx.ClientDC(self.window)
        dc.Blit(0, 0, self.size[0], self.size[1], self.MemDc, 0, 0, wx.COPY)

    def isInteractive(self):
        """Returns 1 if onClick and onOver events are possible, 0 otherwise."""
        return self.interactive

    def canUpdate(self):
        """Returns 1 if the drawing can be meaningfully updated over time (e.g.,
        screen graphics), 0 otherwise (e.g., drawing to a file)."""
        return True

    def clear(self):
        self.Clear()
        dc = wx.ClientDC(self.window)
        dc.Blit(0, 0, self.size[0], self.size[1], self.MemDc, 0, 0, wx.COPY)

    def flush(self):
        """Copies the contents of the memory buffer to the screen and enters the
        application main loop"""
        dc = wx.ClientDC(self.window)
        dc.Blit(0, 0, self.size[0], self.size[1], self.MemDc, 0, 0, wx.COPY)
        del dc

    def setInfoLine(self, s):
        """For interactive Canvases, displays the given string in the 'info
        line' somewhere where the user can probably see it."""
        if self.sb != None:
            self.sb.SetStatusText(s)
        return


if __name__ == '__main__':
    app = wx.App(redirect=False)
    canvas = WXCanvas()
    app.MainLoop()