# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/app/backends/_qt.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 25206 bytes
"""
Base code for the Qt backends. Note that this is *not* (anymore) a
backend by itself! One has to explicitly use either PySide, PyQt4 or
PyQt5. Note that the automatic backend selection prefers a GUI toolkit
that is already imported.

The _pyside, _pyqt4 and _pyqt5 modules will import * from this module,
and also keep a ref to the module object. Note that if two of the
backends are used, this module is actually reloaded. This is a sorts
of poor mans "subclassing" to get a working version for both backends
using the same code.

Note that it is strongly discouraged to use the PySide/PyQt4/PyQt5
backends simultaneously. It is known to cause unpredictable behavior
and segfaults.
"""
from __future__ import division
from time import sleep, time
import os, sys, atexit, ctypes
from ...util import logger
from ..base import BaseApplicationBackend, BaseCanvasBackend, BaseTimerBackend
from ...util import keys
from ext.six import text_type
from ext.six import string_types
from ... import config
from . import qt_lib
USE_EGL = config['gl_backend'].lower().startswith('es')
IS_LINUX = IS_OSX = IS_WIN = IS_RPI = False
if sys.platform.startswith('linux'):
    if os.uname()[4].startswith('arm'):
        IS_RPI = True
    else:
        IS_LINUX = True
else:
    if sys.platform.startswith('darwin'):
        IS_OSX = True
    else:
        if sys.platform.startswith('win'):
            IS_WIN = True
        else:

            def _check_imports(lib):
                libs = [
                 'PyQt4', 'PyQt5', 'PySide']
                libs.remove(lib)
                for lib2 in libs:
                    lib2 += '.QtCore'
                    if lib2 in sys.modules:
                        raise RuntimeError('Refusing to import %s because %s is already imported.' % (
                         lib, lib2))


            QGLWidget = object
            if qt_lib == 'pyqt4':
                _check_imports('PyQt4')
                if not USE_EGL:
                    from PyQt4.QtOpenGL import QGLWidget, QGLFormat
                from PyQt4 import QtGui, QtCore, QtTest
                QWidget, QApplication = QtGui.QWidget, QtGui.QApplication
            else:
                if qt_lib == 'pyqt5':
                    _check_imports('PyQt5')
                    if not USE_EGL:
                        from PyQt5.QtOpenGL import QGLWidget, QGLFormat
                    from PyQt5 import QtGui, QtCore, QtWidgets, QtTest
                    QWidget, QApplication = QtWidgets.QWidget, QtWidgets.QApplication
                else:
                    if qt_lib == 'pyside':
                        _check_imports('PySide')
                        if not USE_EGL:
                            from PySide.QtOpenGL import QGLWidget, QGLFormat
                        from PySide import QtGui, QtCore, QtTest
                        QWidget, QApplication = QtGui.QWidget, QtGui.QApplication
                    else:
                        if qt_lib:
                            raise RuntimeError('Invalid value for qt_lib %r.' % qt_lib)
                        else:
                            raise RuntimeError('Module backends._qt should not be imported directly.')
            KEYMAP = {QtCore.Qt.Key_Shift: keys.SHIFT, 
             QtCore.Qt.Key_Control: keys.CONTROL, 
             QtCore.Qt.Key_Alt: keys.ALT, 
             QtCore.Qt.Key_AltGr: keys.ALT, 
             QtCore.Qt.Key_Meta: keys.META, 
             QtCore.Qt.Key_Left: keys.LEFT, 
             QtCore.Qt.Key_Up: keys.UP, 
             QtCore.Qt.Key_Right: keys.RIGHT, 
             QtCore.Qt.Key_Down: keys.DOWN, 
             QtCore.Qt.Key_PageUp: keys.PAGEUP, 
             QtCore.Qt.Key_PageDown: keys.PAGEDOWN, 
             QtCore.Qt.Key_Insert: keys.INSERT, 
             QtCore.Qt.Key_Delete: keys.DELETE, 
             QtCore.Qt.Key_Home: keys.HOME, 
             QtCore.Qt.Key_End: keys.END, 
             QtCore.Qt.Key_Escape: keys.ESCAPE, 
             QtCore.Qt.Key_Backspace: keys.BACKSPACE, 
             QtCore.Qt.Key_F1: keys.F1, 
             QtCore.Qt.Key_F2: keys.F2, 
             QtCore.Qt.Key_F3: keys.F3, 
             QtCore.Qt.Key_F4: keys.F4, 
             QtCore.Qt.Key_F5: keys.F5, 
             QtCore.Qt.Key_F6: keys.F6, 
             QtCore.Qt.Key_F7: keys.F7, 
             QtCore.Qt.Key_F8: keys.F8, 
             QtCore.Qt.Key_F9: keys.F9, 
             QtCore.Qt.Key_F10: keys.F10, 
             QtCore.Qt.Key_F11: keys.F11, 
             QtCore.Qt.Key_F12: keys.F12, 
             QtCore.Qt.Key_Space: keys.SPACE, 
             QtCore.Qt.Key_Enter: keys.ENTER, 
             QtCore.Qt.Key_Return: keys.ENTER, 
             QtCore.Qt.Key_Tab: keys.TAB}
            BUTTONMAP = {0:0, 
             1:1,  2:2,  4:3,  8:4,  16:5}

            def message_handler(*args):
                if qt_lib in ('pyqt4', 'pyside'):
                    msg_type, msg = args
                else:
                    if qt_lib == 'pyqt5':
                        msg_type, context, msg = args
                    else:
                        if qt_lib:
                            raise RuntimeError('Invalid value for qt_lib %r.' % qt_lib)
                        else:
                            raise RuntimeError('Module backends._qt ', 'should not be imported directly.')
                if msg == 'QCocoaView handleTabletEvent: This tablet device is unknown (received no proximity event for it). Discarding event.':
                    return
                msg = msg.decode() if not isinstance(msg, string_types) else msg
                logger.warning(msg)


            try:
                QtCore.qInstallMsgHandler(message_handler)
            except AttributeError:
                QtCore.qInstallMessageHandler(message_handler)

            capability = dict(title=True,
              size=True,
              position=True,
              show=True,
              vsync=True,
              resizable=True,
              decorate=True,
              fullscreen=True,
              context=True,
              multi_window=True,
              scroll=True,
              parent=True,
              always_on_top=True)

            def _set_config(c):
                """Set the OpenGL configuration"""
                glformat = QGLFormat()
                glformat.setRedBufferSize(c['red_size'])
                glformat.setGreenBufferSize(c['green_size'])
                glformat.setBlueBufferSize(c['blue_size'])
                glformat.setAlphaBufferSize(c['alpha_size'])
                glformat.setAccum(False)
                glformat.setRgba(True)
                glformat.setDoubleBuffer(True if c['double_buffer'] else False)
                glformat.setDepth(True if c['depth_size'] else False)
                glformat.setDepthBufferSize(c['depth_size'] if c['depth_size'] else 0)
                glformat.setStencil(True if c['stencil_size'] else False)
                glformat.setStencilBufferSize(c['stencil_size'] if c['stencil_size'] else 0)
                glformat.setSampleBuffers(True if c['samples'] else False)
                glformat.setSamples(c['samples'] if c['samples'] else 0)
                glformat.setStereo(c['stereo'])
                return glformat


            class ApplicationBackend(BaseApplicationBackend):

                def __init__(self):
                    BaseApplicationBackend.__init__(self)

                def _vispy_get_backend_name(self):
                    name = QtCore.__name__.split('.')[0]
                    return name

                def _vispy_process_events(self):
                    app = self._vispy_get_native_app()
                    app.flush()
                    app.processEvents()

                def _vispy_run(self):
                    app = self._vispy_get_native_app()
                    if hasattr(app, '_in_event_loop') and app._in_event_loop:
                        pass
                    else:
                        return app.exec_()

                def _vispy_quit(self):
                    return self._vispy_get_native_app().quit()

                def _vispy_get_native_app(self):
                    app = QApplication.instance()
                    if app is None:
                        app = QApplication([''])
                    QtGui._qApp = app
                    return app

                def _vispy_sleep(self, duration_sec):
                    QtTest.QTest.qWait(duration_sec * 1000)


            def _get_qpoint_pos(pos):
                """Return the coordinates of a QPointF object."""
                return (
                 pos.x(), pos.y())


            class QtBaseCanvasBackend(BaseCanvasBackend):
                __doc__ = 'Base functionality of Qt backend. No OpenGL Stuff.'

                def __init__(self, *args, **kwargs):
                    (BaseCanvasBackend.__init__)(self, *args)
                    p = self._process_backend_kwargs(kwargs)
                    self._initialized = False
                    self._init_specific(p, kwargs)
                    if not self._initialized:
                        raise AssertionError
                    else:
                        self.setMouseTracking(True)
                        self._vispy_set_title(p.title)
                        (self._vispy_set_size)(*p.size)
                        if p.fullscreen is not False:
                            if p.fullscreen is not True:
                                logger.warning('Cannot specify monitor number for Qt fullscreen, using default')
                            self._fullscreen = True
                        else:
                            self._fullscreen = False
                    if not p.resizable:
                        self.setFixedSize(self.size())
                    if p.position is not None:
                        (self._vispy_set_position)(*p.position)
                    if p.show:
                        self._vispy_set_visible(True)
                    self._double_click_supported = True
                    self._physical_size = p.size
                    if sys.platform == 'darwin':
                        self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
                        self.grabGesture(QtCore.Qt.PinchGesture)

                def _vispy_warmup(self):
                    etime = time() + 0.25
                    while time() < etime:
                        sleep(0.01)
                        self._vispy_canvas.set_current()
                        self._vispy_canvas.app.process_events()

                def _vispy_set_title(self, title):
                    if self._vispy_canvas is None:
                        return
                    self.setWindowTitle(title)

                def _vispy_set_size(self, w, h):
                    self.resize(w, h)

                def _vispy_set_physical_size(self, w, h):
                    self._physical_size = (
                     w, h)

                def _vispy_get_physical_size(self):
                    if self._vispy_canvas is None:
                        return
                    return self._physical_size

                def _vispy_set_position(self, x, y):
                    self.move(x, y)

                def _vispy_set_visible(self, visible):
                    if visible:
                        if self._fullscreen:
                            self.showFullScreen()
                        else:
                            self.showNormal()
                    else:
                        self.hide()

                def _vispy_set_fullscreen(self, fullscreen):
                    self._fullscreen = bool(fullscreen)
                    self._vispy_set_visible(True)

                def _vispy_get_fullscreen(self):
                    return self._fullscreen

                def _vispy_update(self):
                    if self._vispy_canvas is None:
                        return
                    self.update()

                def _vispy_get_position(self):
                    g = self.geometry()
                    return (g.x(), g.y())

                def _vispy_get_size(self):
                    g = self.geometry()
                    return (g.width(), g.height())

                def sizeHint(self):
                    return self.size()

                def mousePressEvent(self, ev):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_mouse_press(native=ev,
                      pos=(
                     ev.pos().x(), ev.pos().y()),
                      button=(BUTTONMAP.get(ev.button(), 0)),
                      modifiers=(self._modifiers(ev)))

                def mouseReleaseEvent(self, ev):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_mouse_release(native=ev,
                      pos=(
                     ev.pos().x(), ev.pos().y()),
                      button=(BUTTONMAP[ev.button()]),
                      modifiers=(self._modifiers(ev)))

                def mouseDoubleClickEvent(self, ev):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_mouse_double_click(native=ev,
                      pos=(
                     ev.pos().x(), ev.pos().y()),
                      button=(BUTTONMAP.get(ev.button(), 0)),
                      modifiers=(self._modifiers(ev)))

                def mouseMoveEvent(self, ev):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_mouse_move(native=ev,
                      pos=(
                     ev.pos().x(), ev.pos().y()),
                      modifiers=(self._modifiers(ev)))

                def wheelEvent(self, ev):
                    if self._vispy_canvas is None:
                        return
                    deltax, deltay = (0.0, 0.0)
                    if hasattr(ev, 'orientation'):
                        if ev.orientation == QtCore.Qt.Horizontal:
                            deltax = ev.delta() / 120.0
                        else:
                            deltay = ev.delta() / 120.0
                    else:
                        delta = ev.angleDelta()
                        deltax, deltay = delta.x() / 120.0, delta.y() / 120.0
                    self._vispy_canvas.events.mouse_wheel(native=ev,
                      delta=(
                     deltax, deltay),
                      pos=(
                     ev.pos().x(), ev.pos().y()),
                      modifiers=(self._modifiers(ev)))

                def keyPressEvent(self, ev):
                    self._keyEvent(self._vispy_canvas.events.key_press, ev)

                def keyReleaseEvent(self, ev):
                    self._keyEvent(self._vispy_canvas.events.key_release, ev)

                def event(self, ev):
                    out = super(QtBaseCanvasBackend, self).event(ev)
                    t = ev.type()
                    if t == QtCore.QEvent.TouchBegin:
                        self._vispy_canvas.events.touch(type='begin')
                    elif t == QtCore.QEvent.TouchEnd:
                        self._vispy_canvas.events.touch(type='end')
                    elif t == QtCore.QEvent.Gesture:
                        gesture = ev.gesture(QtCore.Qt.PinchGesture)
                        if gesture:
                            x, y = _get_qpoint_pos(gesture.centerPoint())
                            scale = gesture.scaleFactor()
                            last_scale = gesture.lastScaleFactor()
                            rotation = gesture.rotationAngle()
                            self._vispy_canvas.events.touch(type='pinch', pos=(
                             x, y),
                              last_pos=None,
                              scale=scale,
                              last_scale=last_scale,
                              rotation=rotation)
                    elif t == QtCore.QEvent.TouchUpdate:
                        points = ev.touchPoints()
                        pos = [_get_qpoint_pos(p.pos()) for p in points]
                        lpos = [_get_qpoint_pos(p.lastPos()) for p in points]
                        self._vispy_canvas.events.touch(type='touch', pos=pos,
                          last_pos=lpos)
                    return out

                def _keyEvent(self, func, ev):
                    key = int(ev.key())
                    if key in KEYMAP:
                        key = KEYMAP[key]
                    else:
                        if key >= 32 and key <= 127:
                            key = keys.Key(chr(key))
                        else:
                            key = None
                    mod = self._modifiers(ev)
                    func(native=ev, key=key, text=(text_type(ev.text())), modifiers=mod)

                def _modifiers(self, event):
                    mod = ()
                    qtmod = event.modifiers()
                    for q, v in ([QtCore.Qt.ShiftModifier, keys.SHIFT],
                     [
                      QtCore.Qt.ControlModifier, keys.CONTROL],
                     [
                      QtCore.Qt.AltModifier, keys.ALT],
                     [
                      QtCore.Qt.MetaModifier, keys.META]):
                        if q & qtmod:
                            mod += (v,)

                    return mod


            _EGL_DISPLAY = None
            egl = None

            class CanvasBackendEgl(QtBaseCanvasBackend, QWidget):

                def _init_specific(self, p, kwargs):
                    global _EGL_DISPLAY
                    global egl
                    if egl is None:
                        from ...ext import egl as _egl
                        egl = _egl
                        if IS_LINUX:
                            if not IS_RPI:
                                os.environ['EGL_SOFTWARE'] = 'true'
                        _EGL_DISPLAY = egl.eglGetDisplay()
                        CanvasBackendEgl._EGL_VERSION = egl.eglInitialize(_EGL_DISPLAY)
                        atexit.register(egl.eglTerminate, _EGL_DISPLAY)
                    else:
                        p.context.shared.add_ref('qt-egl', self)
                        if p.context.shared.ref is self:
                            self._native_config = c = egl.eglChooseConfig(_EGL_DISPLAY)[0]
                            self._native_context = egl.eglCreateContext(_EGL_DISPLAY, c, None)
                        else:
                            self._native_config = p.context.shared.ref._native_config
                            self._native_context = p.context.shared.ref._native_context
                        if not p.always_on_top:
                            hint = p.decorate or 0
                            hint |= 0 if p.decorate else QtCore.Qt.FramelessWindowHint
                            hint |= QtCore.Qt.WindowStaysOnTopHint if p.always_on_top else 0
                        else:
                            pass
                        hint = QtCore.Qt.Widget
                    QWidget.__init__(self, p.parent, hint)
                    if IS_WIN:
                        self.setAttribute(QtCore.Qt.WA_PaintOnScreen, True)
                        self.setAutoFillBackground(False)
                    w = self.get_window_id()
                    self._surface = egl.eglCreateWindowSurface(_EGL_DISPLAY, c, w)
                    self.initializeGL()
                    self._initialized = True

                def get_window_id(self):
                    """ Get the window id of a PySide Widget. Might also work for PyQt4.
        """
                    winid = self.winId()
                    if IS_RPI:
                        nw = (ctypes.c_int * 3)(winid, self.width(), self.height())
                        return ctypes.pointer(nw)
                    if IS_LINUX:
                        return int(winid)
                    ctypes.pythonapi.PyCapsule_GetName.restype = ctypes.c_char_p
                    ctypes.pythonapi.PyCapsule_GetName.argtypes = [ctypes.py_object]
                    ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
                    ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object,
                     ctypes.c_char_p]
                    name = ctypes.pythonapi.PyCapsule_GetName(winid)
                    handle = ctypes.pythonapi.PyCapsule_GetPointer(winid, name)
                    return handle

                def _vispy_close(self):
                    if self._surface is not None:
                        egl.eglDestroySurface(_EGL_DISPLAY, self._surface)
                        self._surface = None
                    self.close()

                def _vispy_set_current(self):
                    egl.eglMakeCurrent(_EGL_DISPLAY, self._surface, self._surface, self._native_context)

                def _vispy_swap_buffers(self):
                    egl.eglSwapBuffers(_EGL_DISPLAY, self._surface)

                def initializeGL(self):
                    self._vispy_canvas.set_current()
                    self._vispy_canvas.events.initialize()

                def resizeEvent(self, event):
                    w, h = event.size().width(), event.size().height()
                    self._vispy_canvas.events.resize(size=(w, h))

                def paintEvent(self, event):
                    self._vispy_canvas.events.draw(region=None)
                    if IS_LINUX or IS_RPI:
                        from ... import gloo
                        import numpy as np
                        if not hasattr(self, '_gl_buffer'):
                            self._gl_buffer = np.ones(36000000, np.uint8) * 255
                        im = gloo.read_pixels()
                        sze = im.shape[0] * im.shape[1]
                        self._gl_buffer[0:0 + sze * 4:4] = im[:, :, 2].ravel()
                        self._gl_buffer[1:0 + sze * 4:4] = im[:, :, 1].ravel()
                        self._gl_buffer[2:2 + sze * 4:4] = im[:, :, 0].ravel()
                        img = QtGui.QImage(self._gl_buffer, im.shape[1], im.shape[0], QtGui.QImage.Format_RGB32)
                        painter = QtGui.QPainter()
                        painter.begin(self)
                        rect = QtCore.QRect(0, 0, self.width(), self.height())
                        painter.drawImage(rect, img)
                        painter.end()

                def paintEngine(self):
                    if IS_LINUX:
                        if not IS_RPI:
                            return QWidget.paintEngine(self)
                    return


            class CanvasBackendDesktop(QtBaseCanvasBackend, QGLWidget):

                def _init_specific(self, p, kwargs):
                    glformat = _set_config(p.context.config)
                    glformat.setSwapInterval(1 if p.vsync else 0)
                    widget = kwargs.pop('shareWidget', None) or self
                    p.context.shared.add_ref('qt', widget)
                    if p.context.shared.ref is widget:
                        if widget is self:
                            widget = None
                    else:
                        widget = p.context.shared.ref
                    if 'shareWidget' in kwargs:
                        raise RuntimeError('Cannot use vispy to share context and use built-in shareWidget.')
                    elif not p.always_on_top:
                        hint = p.decorate or 0
                        hint |= 0 if p.decorate else QtCore.Qt.FramelessWindowHint
                        hint |= QtCore.Qt.WindowStaysOnTopHint if p.always_on_top else 0
                    else:
                        hint = QtCore.Qt.Widget
                    QGLWidget.__init__(self, glformat, p.parent, widget, hint)
                    self._initialized = True
                    if not self.isValid():
                        raise RuntimeError('context could not be created')
                    self.setAutoBufferSwap(False)
                    self.setFocusPolicy(QtCore.Qt.WheelFocus)

                def _vispy_close(self):
                    self.close()
                    self.doneCurrent()
                    self.context().reset()

                def _vispy_set_current(self):
                    if self._vispy_canvas is None:
                        return
                    if self.isValid():
                        self.makeCurrent()

                def _vispy_swap_buffers(self):
                    if self._vispy_canvas is None:
                        return
                    self.swapBuffers()

                def initializeGL(self):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_canvas.events.initialize()

                def resizeGL(self, w, h):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_set_physical_size(w, h)
                    self._vispy_canvas.events.resize(size=(self.width(), self.height()), physical_size=(
                     w, h))

                def paintGL(self):
                    if self._vispy_canvas is None:
                        return
                    self._vispy_canvas.set_current()
                    self._vispy_canvas.events.draw(region=None)


            if USE_EGL:
                CanvasBackend = CanvasBackendEgl
            else:
                CanvasBackend = CanvasBackendDesktop

        class TimerBackend(BaseTimerBackend, QtCore.QTimer):

            def __init__(self, vispy_timer):
                app = ApplicationBackend()
                app._vispy_get_native_app()
                BaseTimerBackend.__init__(self, vispy_timer)
                QtCore.QTimer.__init__(self)
                self.timeout.connect(self._vispy_timeout)

            def _vispy_start(self, interval):
                self.start(interval * 1000.0)

            def _vispy_stop(self):
                self.stop()

            def _vispy_timeout(self):
                self._vispy_timer._timeout()