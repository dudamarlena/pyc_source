# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\openvr\glframework\wx_app.py
# Compiled at: 2019-09-17 21:10:27
# Size of source mod 2**32: 3308 bytes
import sys, wx
from wx import glcanvas

class WxApp(wx.App):
    __doc__ = 'HelloApp uses wxPython library to create an opengl context, listen to keyboard events, and clean up'
    renderer = None
    title = None
    _is_initialized = False
    window = None
    canvas = None
    context = None
    running = False

    def __init__(self, renderer, title='wx test'):
        """Creates an OpenGL context and a window, and acquires OpenGL resources"""
        self.renderer = renderer
        self.title = title
        self._is_initialized = False
        self.window = None
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        self.init_gl()
        return True

    def OnIdle(self, evt):
        self.window.Refresh(False)
        evt.RequestMore()

    def __enter__(self):
        """setup for RAII using 'with' keyword"""
        return self

    def __exit__(self, type_arg, value, traceback):
        """cleanup for RAII using 'with' keyword"""
        self.dispose_gl()

    def init_gl(self):
        print('creating Frame')
        self.window = wx.Frame(parent=None, id=(wx.ID_ANY), title=(self.title), style=(wx.DEFAULT_FRAME_STYLE | wx.WS_EX_PROCESS_IDLE))
        print('creating GLCanvas')
        self.canvas = glcanvas.GLCanvas(self.window, glcanvas.WX_GL_RGBA)
        print('creating GLContext')
        self.context = glcanvas.GLContext(self.canvas)
        self.canvas.SetFocus()
        self.window.SetSize((self.renderer.window_size[0], self.renderer.window_size[1]))
        print('showing Frame')
        self.window.Show(True)
        print('calling SetTopWindow')
        self.SetTopWindow(self.window)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.canvas.Bind(wx.EVT_SIZE, self.OnCanvasSize)
        self.canvas.Bind(wx.EVT_PAINT, self.OnCanvasPaint)
        wx.IdleEvent.SetMode(wx.IDLE_PROCESS_SPECIFIED)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        print('making context current')
        self.canvas.SetCurrent(self.context)
        self.renderer.init_gl()

    def OnCanvasPaint(self, event):
        self.render_scene()

    def render_scene(self):
        """render scene one time"""
        self.canvas.SetCurrent(self.context)
        self.renderer.render_scene()
        if self.canvas.IsDoubleBuffered():
            self.canvas.SwapBuffers()
            print('double buffered')
        else:
            self.canvas.SwapBuffers()

    def dispose_gl(self):
        pass

    def OnCanvasSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.canvas.GetClientSize()
        self.canvas.SetCurrent(self.context)
        self.renderer.size_callback(self.window, size.width, size.height)

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key == ord('q') or key == ord('Q') or key == wx.WXK_ESCAPE:
            self.window.Close()
            sys.exit(0)
            return
        event.Skip()

    def run_loop(self):
        self.MainLoop()