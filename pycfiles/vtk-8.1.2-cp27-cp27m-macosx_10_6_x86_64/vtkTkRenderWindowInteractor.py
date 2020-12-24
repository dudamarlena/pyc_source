# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/tk/vtkTkRenderWindowInteractor.py
# Compiled at: 2018-11-28 17:07:58
"""

A fully functional VTK widget for tkinter that uses
vtkGenericRenderWindowInteractor.  The widget is called
vtkTkRenderWindowInteractor.  The initialization part of this code is
similar to that of the vtkTkRenderWidget.

Created by Prabhu Ramachandran, April 2002

"""
from __future__ import absolute_import
import math, os, sys, vtk
if sys.hexversion < 50331648:
    import Tkinter as tkinter
else:
    import tkinter
from .vtkLoadPythonTkWidgets import vtkLoadPythonTkWidgets

class vtkTkRenderWindowInteractor(tkinter.Widget):
    """ A vtkTkRenderWidndowInteractor for Python.

    Use GetRenderWindow() to get the vtkRenderWindow.

    Create with the keyword stereo=1 in order to generate a
    stereo-capable window.

    Create with the keyword focus_on_enter=1 to enable
    focus-follows-mouse.  The default is for a click-to-focus mode.

    __getattr__ is used to make the widget also behave like a
    vtkGenericRenderWindowInteractor.
    """

    def __init__(self, master, cnf={}, **kw):
        """
        Constructor.

        Keyword arguments:

          rw -- Use passed render window instead of creating a new one.

          stereo -- If True, generate a stereo-capable window.
          Defaults to False.

          focus_on_enter -- If True, use a focus-follows-mouse mode.
          Defaults to False where the widget will use a click-to-focus
          mode.
        """
        vtkLoadPythonTkWidgets(master.tk)
        try:
            renderWindow = kw['rw']
        except KeyError:
            renderWindow = vtk.vtkRenderWindow()

        try:
            if kw['stereo']:
                renderWindow.StereoCapableWindowOn()
                del kw['stereo']
        except KeyError:
            pass

        if kw.get('focus_on_enter'):
            self._FocusOnEnter = 1
            del kw['focus_on_enter']
        else:
            self._FocusOnEnter = 0
        kw['rw'] = renderWindow.GetAddressAsString('vtkRenderWindow')
        tkinter.Widget.__init__(self, master, 'vtkTkRenderWidget', cnf, kw)
        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._Iren.SetRenderWindow(self._RenderWindow)
        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)
        self._OldFocus = None
        self.__InExpose = 0
        self.BindEvents()
        return

    def __getattr__(self, attr):
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        if attr == '_RenderWindow':
            return self.GetRenderWindow()
        if hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        raise AttributeError(self.__class__.__name__ + ' has no attribute named ' + attr)

    def BindEvents(self):
        """ Bind all the events.  """
        self.bind('<Motion>', lambda e, s=self: s.MouseMoveEvent(e, 0, 0))
        self.bind('<Control-Motion>', lambda e, s=self: s.MouseMoveEvent(e, 1, 0))
        self.bind('<Shift-Motion>', lambda e, s=self: s.MouseMoveEvent(e, 1, 1))
        self.bind('<Control-Shift-Motion>', lambda e, s=self: s.MouseMoveEvent(e, 0, 1))
        self.bind('<ButtonPress-1>', lambda e, s=self: s.LeftButtonPressEvent(e, 0, 0))
        self.bind('<Control-ButtonPress-1>', lambda e, s=self: s.LeftButtonPressEvent(e, 1, 0))
        self.bind('<Shift-ButtonPress-1>', lambda e, s=self: s.LeftButtonPressEvent(e, 0, 1))
        self.bind('<Control-Shift-ButtonPress-1>', lambda e, s=self: s.LeftButtonPressEvent(e, 1, 1))
        self.bind('<ButtonRelease-1>', lambda e, s=self: s.LeftButtonReleaseEvent(e, 0, 0))
        self.bind('<Control-ButtonRelease-1>', lambda e, s=self: s.LeftButtonReleaseEvent(e, 1, 0))
        self.bind('<Shift-ButtonRelease-1>', lambda e, s=self: s.LeftButtonReleaseEvent(e, 0, 1))
        self.bind('<Control-Shift-ButtonRelease-1>', lambda e, s=self: s.LeftButtonReleaseEvent(e, 1, 1))
        self.bind('<ButtonPress-2>', lambda e, s=self: s.MiddleButtonPressEvent(e, 0, 0))
        self.bind('<Control-ButtonPress-2>', lambda e, s=self: s.MiddleButtonPressEvent(e, 1, 0))
        self.bind('<Shift-ButtonPress-2>', lambda e, s=self: s.MiddleButtonPressEvent(e, 0, 1))
        self.bind('<Control-Shift-ButtonPress-2>', lambda e, s=self: s.MiddleButtonPressEvent(e, 1, 1))
        self.bind('<ButtonRelease-2>', lambda e, s=self: s.MiddleButtonReleaseEvent(e, 0, 0))
        self.bind('<Control-ButtonRelease-2>', lambda e, s=self: s.MiddleButtonReleaseEvent(e, 1, 0))
        self.bind('<Shift-ButtonRelease-2>', lambda e, s=self: s.MiddleButtonReleaseEvent(e, 0, 1))
        self.bind('<Control-Shift-ButtonRelease-2>', lambda e, s=self: s.MiddleButtonReleaseEvent(e, 1, 1))
        self.bind('<ButtonPress-3>', lambda e, s=self: s.RightButtonPressEvent(e, 0, 0))
        self.bind('<Control-ButtonPress-3>', lambda e, s=self: s.RightButtonPressEvent(e, 1, 0))
        self.bind('<Shift-ButtonPress-3>', lambda e, s=self: s.RightButtonPressEvent(e, 0, 1))
        self.bind('<Control-Shift-ButtonPress-3>', lambda e, s=self: s.RightButtonPressEvent(e, 1, 1))
        self.bind('<ButtonRelease-3>', lambda e, s=self: s.RightButtonReleaseEvent(e, 0, 0))
        self.bind('<Control-ButtonRelease-3>', lambda e, s=self: s.RightButtonReleaseEvent(e, 1, 0))
        self.bind('<Shift-ButtonRelease-3>', lambda e, s=self: s.RightButtonReleaseEvent(e, 0, 1))
        self.bind('<Control-Shift-ButtonRelease-3>', lambda e, s=self: s.RightButtonReleaseEvent(e, 1, 1))
        if sys.platform == 'win32':
            self.bind('<MouseWheel>', lambda e, s=self: s.MouseWheelEvent(e, 0, 0))
            self.bind('<Control-MouseWheel>', lambda e, s=self: s.MouseWheelEvent(e, 1, 0))
            self.bind('<Shift-MouseWheel>', lambda e, s=self: s.MouseWheelEvent(e, 0, 1))
            self.bind('<Control-Shift-MouseWheel>', lambda e, s=self: s.MouseWheelEvent(e, 1, 1))
        else:
            self.bind('<ButtonPress-4>', lambda e, s=self: s.MouseWheelForwardEvent(e, 0, 0))
            self.bind('<Control-ButtonPress-4>', lambda e, s=self: s.MouseWheelForwardEvent(e, 1, 0))
            self.bind('<Shift-ButtonPress-4>', lambda e, s=self: s.MouseWheelForwardEvent(e, 0, 1))
            self.bind('<Control-Shift-ButtonPress-4>', lambda e, s=self: s.MouseWheelForwardEvent(e, 1, 1))
            self.bind('<ButtonPress-5>', lambda e, s=self: s.MouseWheelBackwardEvent(e, 0, 0))
            self.bind('<Control-ButtonPress-5>', lambda e, s=self: s.MouseWheelBackwardEvent(e, 1, 0))
            self.bind('<Shift-ButtonPress-5>', lambda e, s=self: s.MouseWheelBackwardEvent(e, 0, 1))
            self.bind('<Control-Shift-ButtonPress-5>', lambda e, s=self: s.MouseWheelBackwardEvent(e, 1, 1))
        self.bind('<KeyPress>', lambda e, s=self: s.KeyPressEvent(e, 0, 0))
        self.bind('<Control-KeyPress>', lambda e, s=self: s.KeyPressEvent(e, 1, 0))
        self.bind('<Shift-KeyPress>', lambda e, s=self: s.KeyPressEvent(e, 0, 1))
        self.bind('<Control-Shift-KeyPress>', lambda e, s=self: s.KeyPressEvent(e, 1, 1))
        self.bind('<KeyRelease>', lambda e, s=self: s.KeyReleaseEvent(e, 0, 0))
        self.bind('<Control-KeyRelease>', lambda e, s=self: s.KeyReleaseEvent(e, 1, 0))
        self.bind('<Shift-KeyRelease>', lambda e, s=self: s.KeyReleaseEvent(e, 0, 1))
        self.bind('<Control-Shift-KeyRelease>', lambda e, s=self: s.KeyReleaseEvent(e, 1, 1))
        self.bind('<Enter>', lambda e, s=self: s.EnterEvent(e, 0, 0))
        self.bind('<Control-Enter>', lambda e, s=self: s.EnterEvent(e, 1, 0))
        self.bind('<Shift-Enter>', lambda e, s=self: s.EnterEvent(e, 0, 1))
        self.bind('<Control-Shift-Enter>', lambda e, s=self: s.EnterEvent(e, 1, 1))
        self.bind('<Leave>', lambda e, s=self: s.LeaveEvent(e, 0, 0))
        self.bind('<Control-Leave>', lambda e, s=self: s.LeaveEvent(e, 1, 0))
        self.bind('<Shift-Leave>', lambda e, s=self: s.LeaveEvent(e, 0, 1))
        self.bind('<Control-Shift-Leave>', lambda e, s=self: s.LeaveEvent(e, 1, 1))
        self.bind('<Configure>', self.ConfigureEvent)
        self.bind('<Expose>', lambda e, s=self: s.ExposeEvent())

    def CreateTimer(self, obj, evt):
        self.after(10, self._Iren.TimerEvent)

    def DestroyTimer(self, obj, event):
        """The timer is a one shot timer so will expire automatically."""
        return 1

    def _GrabFocus(self, enter=0):
        self._OldFocus = self.focus_get()
        self.focus()

    def MouseMoveEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.MouseMoveEvent()
        return

    def LeftButtonPressEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.LeftButtonPressEvent()
        if not self._FocusOnEnter:
            self._GrabFocus()
        return

    def LeftButtonReleaseEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.LeftButtonReleaseEvent()
        return

    def MiddleButtonPressEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.MiddleButtonPressEvent()
        if not self._FocusOnEnter:
            self._GrabFocus()
        return

    def MiddleButtonReleaseEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.MiddleButtonReleaseEvent()
        return

    def RightButtonPressEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.RightButtonPressEvent()
        if not self._FocusOnEnter:
            self._GrabFocus()
        return

    def RightButtonReleaseEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.RightButtonReleaseEvent()
        return

    def MouseWheelEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        if event.delta > 0:
            self._Iren.MouseWheelForwardEvent()
        else:
            self._Iren.MouseWheelBackwardEvent()
        return

    def MouseWheelForwardEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.MouseWheelForwardEvent()
        return

    def MouseWheelBackwardEvent(self, event, ctrl, shift):
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.MouseWheelBackwardEvent()
        return

    def KeyPressEvent(self, event, ctrl, shift):
        key = chr(0)
        if event.keysym_num < 256:
            key = chr(event.keysym_num)
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, key, 0, event.keysym)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()

    def KeyReleaseEvent(self, event, ctrl, shift):
        key = chr(0)
        if event.keysym_num < 256:
            key = chr(event.keysym_num)
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, key, 0, event.keysym)
        self._Iren.KeyReleaseEvent()

    def ConfigureEvent(self, event):
        self._Iren.SetSize(event.width, event.height)
        self._Iren.ConfigureEvent()

    def EnterEvent(self, event, ctrl, shift):
        if self._FocusOnEnter:
            self._GrabFocus()
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.EnterEvent()
        return

    def LeaveEvent(self, event, ctrl, shift):
        if self._FocusOnEnter and self._OldFocus != None:
            self._OldFocus.focus()
        self._Iren.SetEventInformationFlipY(event.x, event.y, ctrl, shift, chr(0), 0, None)
        self._Iren.LeaveEvent()
        return

    def ExposeEvent(self):
        if not self.__InExpose:
            self.__InExpose = 1
            if not self._RenderWindow.IsA('vtkCocoaRenderWindow'):
                self.update()
            self._RenderWindow.Render()
            self.__InExpose = 0

    def GetRenderWindow(self):
        addr = self.tk.call(self._w, 'GetRenderWindow')[5:]
        return vtk.vtkRenderWindow('_%s_vtkRenderWindow_p' % addr)

    def Render(self):
        self._RenderWindow.Render()


def vtkRenderWindowInteractorConeExample():
    """Like it says, just a simple example
    """
    root = tkinter.Tk()
    pane = vtkTkRenderWindowInteractor(root, width=300, height=300)
    pane.Initialize()

    def quit(obj=root):
        obj.quit()

    pane.AddObserver('ExitEvent', lambda o, e, q=quit: q())
    ren = vtk.vtkRenderer()
    pane.GetRenderWindow().AddRenderer(ren)
    cone = vtk.vtkConeSource()
    cone.SetResolution(8)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    ren.AddActor(coneActor)
    pane.pack(fill='both', expand=1)
    pane.Start()
    root.mainloop()


if __name__ == '__main__':
    vtkRenderWindowInteractorConeExample()