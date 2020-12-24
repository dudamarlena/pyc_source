# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/GtkGLExtVTKRenderWindowInteractor.py
# Compiled at: 2012-04-18 08:40:01
__doc__ = '\nThis code is based on GtkVTKRenderWindowInteractor written by Prabhu\nRamachandran that ships with VTK.\n\nThe extensions here allow the use of gtkglext rather than gtkgl and\npygtk-2 rather than pygtk-0.  It requires pygtk-2.0.0 or later.\n\nJohn Hunter jdhunter@ace.bsd.uchicago.edu\n'
import sys, gtk
from gtk import gdk
import gtk.gtkgl, vtk
from shared import shared

class GtkGLExtVTKRenderWindowInteractor(gtk.gtkgl.DrawingArea):
    """
    CLASS: GtkGLExtVTKRenderWindowInteractor
    DESCR: Embeds a vtkRenderWindow into a pyGTK widget and uses
    vtkGenericRenderWindowInteractor for the event handling.  This
    class embeds the RenderWindow correctly.  A __getattr__ hook is
    provided that makes the class behave like a
    vtkGenericRenderWindowInteractor."""

    def __init__(self, *args):
        gtk.gtkgl.DrawingArea.__init__(self)
        self.set_double_buffered(False)
        self._RenderWindow = vtk.vtkRenderWindow()
        self.__Created = 0
        self._ActiveButton = 0
        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._Iren.SetRenderWindow(self._RenderWindow)
        self._Iren.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)
        self.ConnectSignals()
        self.set_flags(gtk.CAN_FOCUS)

    def set_size_request(self, w, h):
        gtk.gtkgl.DrawingArea.set_size_request(self, w, h)
        self._RenderWindow.SetSize(w, h)
        self._Iren.SetSize(w, h)
        self._Iren.ConfigureEvent()

    def ConnectSignals(self):
        self.connect('realize', self.OnRealize)
        self.connect('expose_event', self.OnExpose)
        self.connect('configure_event', self.OnConfigure)
        self.connect('button_press_event', self.OnButtonDown)
        self.connect('button_release_event', self.OnButtonUp)
        self.connect('motion_notify_event', self.OnMouseMove)
        self.connect('enter_notify_event', self.OnEnter)
        self.connect('leave_notify_event', self.OnLeave)
        self.connect('key_press_event', self.OnKeyPress)
        self.connect('delete_event', self.OnDestroy)
        self.add_events(gdk.EXPOSURE_MASK | gdk.BUTTON_PRESS_MASK | gdk.BUTTON_RELEASE_MASK | gdk.KEY_PRESS_MASK | gdk.POINTER_MOTION_MASK | gdk.POINTER_MOTION_HINT_MASK | gdk.ENTER_NOTIFY_MASK | gdk.LEAVE_NOTIFY_MASK)

    def __getattr__(self, attr):
        """Makes the object behave like a
        vtkGenericRenderWindowInteractor"""
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        if hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        raise AttributeError, self.__class__.__name__ + ' has no attribute named ' + attr

    def CreateTimer(self, obj, event):
        gtk.timeout_add(10, self._Iren.TimerEvent)

    def DestroyTimer(self, obj, event):
        """The timer is a one shot timer so will expire automatically."""
        return 1

    def GetRenderWindow(self):
        return self._RenderWindow

    def Render(self):
        if self.__Created:
            self._RenderWindow.Render()

    def OnRealize(self, *args):
        if self.__Created == 0:
            self.realize()
            if sys.platform == 'win32':
                win_id = str(self.widget.window.handle)
            else:
                win_id = str(self.widget.window.xid)
            self._RenderWindow.SetWindowInfo(win_id)
            self.__Created = 1
        return True

    def OnConfigure(self, widget, event):
        self.widget = widget
        self._Iren.SetSize(event.width, event.height)
        self._Iren.ConfigureEvent()
        self.Render()
        return True

    def OnExpose(self, *args):
        self.Render()
        return True

    def OnDestroy(self, event=None):
        self.hide()
        del self._RenderWindow
        self.destroy()
        return True

    def _GetCtrlShift(self, event):
        ctrl, shift = (0, 0)
        if event.state & gdk.CONTROL_MASK == gdk.CONTROL_MASK:
            ctrl = 1
        if event.state & gdk.SHIFT_MASK == gdk.SHIFT_MASK:
            shift = 1
        return (ctrl, shift)

    def OnButtonDown(self, wid, event):
        if shared.debug:
            print 'GtkGLExtVTKRenderWindowInteractor.OnButtonDown()'
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, chr(0), 0, None)
        button = event.button
        if button == 3:
            self._Iren.RightButtonPressEvent()
            return True
        else:
            if button == 1:
                self._Iren.LeftButtonPressEvent()
                return True
            else:
                if button == 2:
                    self._Iren.MiddleButtonPressEvent()
                    return True
                return False

            return

    def OnButtonUp(self, wid, event):
        """Mouse button released."""
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, chr(0), 0, None)
        button = event.button
        if button == 3:
            self._Iren.RightButtonReleaseEvent()
            return True
        else:
            if button == 1:
                self._Iren.LeftButtonReleaseEvent()
                return True
            if button == 2:
                self._Iren.MiddleButtonReleaseEvent()
                return True
            return False

    def OnMouseMove(self, wid, event):
        """Mouse has moved."""
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, chr(0), 0, None)
        self._Iren.MouseMoveEvent()
        return True

    def OnEnter(self, wid, event):
        """Entering the vtkRenderWindow."""
        self.grab_focus()
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, chr(0), 0, None)
        self._Iren.EnterEvent()
        return True

    def OnLeave(self, wid, event):
        """Leaving the vtkRenderWindow."""
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, chr(0), 0, None)
        self._Iren.LeaveEvent()
        return True

    def OnKeyPress(self, wid, event):
        """Key pressed."""
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        keycode, keysym = event.keyval, event.string
        key = chr(0)
        if keycode < 256:
            key = chr(keycode)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, key, 0, keysym)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()
        return True

    def OnKeyRelease(self, wid, event):
        """Key released."""
        m = self.get_pointer()
        ctrl, shift = self._GetCtrlShift(event)
        keycode, keysym = event.keyval, event.string
        key = chr(0)
        if keycode < 256:
            key = chr(keycode)
        self._Iren.SetEventInformationFlipY(m[0], m[1], ctrl, shift, key, 0, keysym)
        self._Iren.KeyReleaseEvent()
        return True

    def Initialize(self):
        if self.__Created:
            self._Iren.Initialize()

    def SetPicker(self, picker):
        self._Iren.SetPicker(picker)

    def GetPicker(self, picker):
        return self._Iren.GetPicker()


def main():
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title('A GtkVTKRenderWindow Demo!')
    window.connect('destroy', gtk.main_quit)
    window.connect('delete_event', gtk.main_quit)
    window.set_border_width(10)
    vbox = gtk.VBox(spacing=3)
    window.add(vbox)
    vbox.show()
    gvtk = GtkGLExtVTKRenderWindowInteractor()
    gvtk.set_size_request(400, 400)
    vbox.pack_start(gvtk)
    gvtk.show()
    gvtk.Initialize()
    gvtk.Start()
    gvtk.AddObserver('ExitEvent', lambda o, e, x=None: x)
    cone = vtk.vtkConeSource()
    cone.SetResolution(80)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(0.5, 0.5, 1.0)
    ren = vtk.vtkRenderer()
    gvtk.GetRenderWindow().AddRenderer(ren)
    ren.AddActor(coneActor)
    quit = gtk.Button('Quit!')
    quit.connect('clicked', gtk.main_quit)
    vbox.pack_start(quit)
    quit.show()
    window.show()
    gtk.main()
    return


if __name__ == '__main__':
    main()