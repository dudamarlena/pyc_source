# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/wx/wxVTKRenderWindowInteractor.py
# Compiled at: 2018-11-28 17:07:58
"""

A VTK RenderWindowInteractor widget for wxPython.

Find wxPython info at http://wxPython.org

Created by Prabhu Ramachandran, April 2002
Based on wxVTKRenderWindow.py

Fixes and updates by Charl P. Botha 2003-2008

Updated to new wx namespace and some cleaning up by Andrea Gavana,
December 2006
"""
import math, os, sys, wx, vtk
baseClass = wx.Window
if wx.Platform == '__WXGTK__':
    import wx.glcanvas
    baseClass = wx.glcanvas.GLCanvas
_useCapture = wx.Platform == '__WXMSW__'

class EventTimer(wx.Timer):
    """Simple wx.Timer class.
    """

    def __init__(self, iren):
        """Default class constructor.
        @param iren: current render window
        """
        wx.Timer.__init__(self)
        self.iren = iren

    def Notify(self):
        """ The timer has expired.
        """
        self.iren.TimerEvent()


class wxVTKRenderWindowInteractor(baseClass):
    """
    A wxRenderWindow for wxPython.
    Use GetRenderWindow() to get the vtkRenderWindow.
    Create with the keyword stereo=1 in order to
    generate a stereo-capable window.
    """
    USE_STEREO = False

    def __init__(self, parent, ID, *args, **kw):
        """Default class constructor.
        @param parent: parent window
        @param ID: window id
        @param **kw: wxPython keywords (position, size, style) plus the
        'stereo' keyword
        """
        self.__RenderWhenDisabled = 0
        try:
            stereo = bool(kw['stereo'])
            del kw['stereo']
        except KeyError:
            stereo = False

        try:
            position = kw['position']
            del kw['position']
        except KeyError:
            position = wx.DefaultPosition

        try:
            size = kw['size']
            del kw['size']
        except KeyError:
            try:
                size = parent.GetSize()
            except AttributeError:
                size = wx.DefaultSize

        style = wx.WANTS_CHARS | wx.NO_FULL_REPAINT_ON_RESIZE
        try:
            style = style | kw['style']
            del kw['style']
        except KeyError:
            pass

        if wx.Platform != '__WXMSW__':
            l = []
            p = parent
            while p:
                l.append(p)
                p = p.GetParent()

            l.reverse()
            for p in l:
                p.Show(1)

        if baseClass.__name__ == 'GLCanvas':
            attribList = [
             wx.glcanvas.WX_GL_RGBA,
             wx.glcanvas.WX_GL_MIN_RED, 1,
             wx.glcanvas.WX_GL_MIN_GREEN, 1,
             wx.glcanvas.WX_GL_MIN_BLUE, 1,
             wx.glcanvas.WX_GL_DEPTH_SIZE, 16,
             wx.glcanvas.WX_GL_DOUBLEBUFFER]
            if stereo:
                attribList.append(wx.glcanvas.WX_GL_STEREO)
            try:
                baseClass.__init__(self, parent, ID, pos=position, size=size, style=style, attribList=attribList)
            except wx.PyAssertionError:
                baseClass.__init__(self, parent, ID, pos=position, size=size, style=style)
                if stereo:
                    stereo = 0

        else:
            baseClass.__init__(self, parent, ID, pos=position, size=size, style=style)
        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._Iren.SetRenderWindow(vtk.vtkRenderWindow())
        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)
        self._Iren.GetRenderWindow().AddObserver('CursorChangedEvent', self.CursorChangedEvent)
        try:
            self._Iren.GetRenderWindow().SetSize(size.width, size.height)
        except AttributeError:
            self._Iren.GetRenderWindow().SetSize(size[0], size[1])

        if stereo:
            self._Iren.GetRenderWindow().StereoCapableWindowOn()
            self._Iren.GetRenderWindow().SetStereoTypeToCrystalEyes()
        self.__handle = None
        self.BindEvents()
        self.__has_painted = False
        self._own_mouse = False
        self._mouse_capture_button = 0
        self._cursor_map = {0: wx.CURSOR_ARROW, 1: wx.CURSOR_ARROW, 
           2: wx.CURSOR_SIZENESW, 
           3: wx.CURSOR_SIZENWSE, 
           4: wx.CURSOR_SIZENESW, 
           5: wx.CURSOR_SIZENWSE, 
           6: wx.CURSOR_SIZENS, 
           7: wx.CURSOR_SIZEWE, 
           8: wx.CURSOR_SIZING, 
           9: wx.CURSOR_HAND, 
           10: wx.CURSOR_CROSS}
        return

    def BindEvents(self):
        """Binds all the necessary events for navigation, sizing,
        drawing.
        """
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnButtonDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnButtonDown)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnButtonDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnButtonUp)
        self.Bind(wx.EVT_LEFT_UP, self.OnButtonUp)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnButtonUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        if _useCapture and hasattr(wx, 'EVT_MOUSE_CAPTURE_LOST'):
            self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnMouseCaptureLost)

    def __getattr__(self, attr):
        """Makes the object behave like a
        vtkGenericRenderWindowInteractor.
        """
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        if hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        raise AttributeError(self.__class__.__name__ + ' has no attribute named ' + attr)

    def CreateTimer(self, obj, evt):
        """ Creates a timer.
        """
        self._timer = EventTimer(self)
        self._timer.Start(10, True)

    def DestroyTimer(self, obj, evt):
        """The timer is a one shot timer so will expire automatically.
        """
        return 1

    def _CursorChangedEvent(self, obj, evt):
        """Change the wx cursor if the renderwindow's cursor was
        changed.
        """
        cur = self._cursor_map[obj.GetCurrentCursor()]
        c = wx.StockCursor(cur)
        self.SetCursor(c)

    def CursorChangedEvent(self, obj, evt):
        """Called when the CursorChangedEvent fires on the render
        window."""
        wx.CallAfter(self._CursorChangedEvent, obj, evt)

    def HideCursor(self):
        """Hides the cursor."""
        c = wx.StockCursor(wx.CURSOR_BLANK)
        self.SetCursor(c)

    def ShowCursor(self):
        """Shows the cursor."""
        rw = self._Iren.GetRenderWindow()
        cur = self._cursor_map[rw.GetCurrentCursor()]
        c = wx.StockCursor(cur)
        self.SetCursor(c)

    def GetDisplayId(self):
        """Function to get X11 Display ID from WX and return it in a format
        that can be used by VTK Python.

        We query the X11 Display with a new call that was added in wxPython
        2.6.0.1.  The call returns a SWIG object which we can query for the
        address and subsequently turn into an old-style SWIG-mangled string
        representation to pass to VTK.
        """
        d = None
        try:
            d = wx.GetXDisplay()
        except AttributeError:
            pass

        if d:
            d = hex(d)
            if not d.startswith('0x'):
                d = '0x' + d
            d = '_%s_%s\x00' % (d[2:], 'p_void')
        return d

    def OnMouseCaptureLost(self, event):
        """This is signalled when we lose mouse capture due to an
        external event, such as when a dialog box is shown.  See the
        wx documentation.
        """
        if _useCapture and self._own_mouse:
            self._own_mouse = False

    def OnPaint(self, event):
        """Handles the wx.EVT_PAINT event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        dc = wx.PaintDC(self)
        self._Iren.GetRenderWindow().SetSize(self.GetSize())
        if not self.__handle:
            d = self.GetDisplayId()
            if d and self.__has_painted:
                self._Iren.GetRenderWindow().SetDisplayId(d)
            self.__handle = self.GetHandle()
            self._Iren.GetRenderWindow().SetWindowInfo(str(self.__handle))
            self.__has_painted = True
        self.Render()

    def OnSize(self, event):
        """Handles the wx.EVT_SIZE event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        try:
            width, height = event.GetSize()
        except:
            width = event.GetSize().width
            height = event.GetSize().height

        self._Iren.SetSize(width, height)
        self._Iren.ConfigureEvent()
        self.Render()

    def OnMotion(self, event):
        """Handles the wx.EVT_MOTION event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), event.ControlDown(), event.ShiftDown(), chr(0), 0, None)
        self._Iren.MouseMoveEvent()
        return

    def OnEnter(self, event):
        """Handles the wx.EVT_ENTER_WINDOW event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), event.ControlDown(), event.ShiftDown(), chr(0), 0, None)
        self._Iren.EnterEvent()
        return

    def OnLeave(self, event):
        """Handles the wx.EVT_LEAVE_WINDOW event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), event.ControlDown(), event.ShiftDown(), chr(0), 0, None)
        self._Iren.LeaveEvent()
        return

    def OnButtonDown(self, event):
        """Handles the wx.EVT_LEFT/RIGHT/MIDDLE_DOWN events for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        ctrl, shift = event.ControlDown(), event.ShiftDown()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), ctrl, shift, chr(0), 0, None)
        button = 0
        if event.RightDown():
            self._Iren.RightButtonPressEvent()
            button = 'Right'
        elif event.LeftDown():
            self._Iren.LeftButtonPressEvent()
            button = 'Left'
        elif event.MiddleDown():
            self._Iren.MiddleButtonPressEvent()
            button = 'Middle'
        if _useCapture and not self._own_mouse:
            self._own_mouse = True
            self._mouse_capture_button = button
            self.CaptureMouse()
        return

    def OnButtonUp(self, event):
        """Handles the wx.EVT_LEFT/RIGHT/MIDDLE_UP events for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        button = 0
        if event.RightUp():
            button = 'Right'
        elif event.LeftUp():
            button = 'Left'
        elif event.MiddleUp():
            button = 'Middle'
        if _useCapture and self._own_mouse and button == self._mouse_capture_button:
            self.ReleaseMouse()
            self._own_mouse = False
        ctrl, shift = event.ControlDown(), event.ShiftDown()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), ctrl, shift, chr(0), 0, None)
        if button == 'Right':
            self._Iren.RightButtonReleaseEvent()
        elif button == 'Left':
            self._Iren.LeftButtonReleaseEvent()
        elif button == 'Middle':
            self._Iren.MiddleButtonReleaseEvent()
        return

    def OnMouseWheel(self, event):
        """Handles the wx.EVT_MOUSEWHEEL event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        ctrl, shift = event.ControlDown(), event.ShiftDown()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), ctrl, shift, chr(0), 0, None)
        if event.GetWheelRotation() > 0:
            self._Iren.MouseWheelForwardEvent()
        else:
            self._Iren.MouseWheelBackwardEvent()
        return

    def OnKeyDown(self, event):
        """Handles the wx.EVT_KEY_DOWN event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        ctrl, shift = event.ControlDown(), event.ShiftDown()
        keycode, keysym = event.GetKeyCode(), None
        key = chr(0)
        if keycode < 256:
            key = chr(keycode)
        x, y = self._Iren.GetEventPosition()
        self._Iren.SetEventInformation(x, y, ctrl, shift, key, 0, keysym)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()
        return

    def OnKeyUp(self, event):
        """Handles the wx.EVT_KEY_UP event for
        wxVTKRenderWindowInteractor.
        """
        event.Skip()
        ctrl, shift = event.ControlDown(), event.ShiftDown()
        keycode, keysym = event.GetKeyCode(), None
        key = chr(0)
        if keycode < 256:
            key = chr(keycode)
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(), ctrl, shift, key, 0, keysym)
        self._Iren.KeyReleaseEvent()
        return

    def GetRenderWindow(self):
        """Returns the render window (vtkRenderWindow).
        """
        return self._Iren.GetRenderWindow()

    def Render(self):
        """Actually renders the VTK scene on screen.
        """
        RenderAllowed = 1
        if not self.__RenderWhenDisabled:
            topParent = wx.GetTopLevelParent(self)
            if topParent:
                RenderAllowed = topParent.IsEnabled()
        if RenderAllowed:
            if self.__handle and self.__handle == self.GetHandle():
                self._Iren.GetRenderWindow().Render()
            elif self.GetHandle() and self.__has_painted:
                self._Iren.GetRenderWindow().SetNextWindowInfo(str(self.GetHandle()))
                d = self.GetDisplayId()
                if d:
                    self._Iren.GetRenderWindow().SetDisplayId(d)
                self._Iren.GetRenderWindow().WindowRemap()
                self.__handle = self.GetHandle()
                self._Iren.GetRenderWindow().Render()

    def SetRenderWhenDisabled(self, newValue):
        """Change value of __RenderWhenDisabled ivar.

        If __RenderWhenDisabled is false (the default), this widget will not
        call Render() on the RenderWindow if the top level frame (i.e. the
        containing frame) has been disabled.

        This prevents recursive rendering during wx.SafeYield() calls.
        wx.SafeYield() can be called during the ProgressMethod() callback of
        a VTK object to have progress bars and other GUI elements updated -
        it does this by disabling all windows (disallowing user-input to
        prevent re-entrancy of code) and then handling all outstanding
        GUI events.

        However, this often triggers an OnPaint() method for wxVTKRWIs,
        resulting in a Render(), resulting in Update() being called whilst
        still in progress.
        """
        self.__RenderWhenDisabled = bool(newValue)


def wxVTKRenderWindowInteractorConeExample():
    """Like it says, just a simple example
    """
    app = wx.App(False)
    frame = wx.Frame(None, -1, 'wxVTKRenderWindowInteractor', size=(400, 400))
    widget = wxVTKRenderWindowInteractor(frame, -1)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(widget, 1, wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Layout()
    widget.Enable(1)
    widget.AddObserver('ExitEvent', lambda o, e, f=frame: f.Close())
    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)
    cone = vtk.vtkConeSource()
    cone.SetResolution(8)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    ren.AddActor(coneActor)
    frame.Show()
    app.MainLoop()
    return


if __name__ == '__main__':
    wxVTKRenderWindowInteractorConeExample()