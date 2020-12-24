# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/RemoteGraphicsView.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 11749 bytes
from ..Qt import QtGui, QtCore, USE_PYSIDE
if not USE_PYSIDE:
    import sip
from .. import multiprocess as mp
from .GraphicsView import GraphicsView
from .. import CONFIG_OPTIONS
import numpy as np, mmap, tempfile, ctypes, atexit, sys, random
__all__ = ['RemoteGraphicsView']

class RemoteGraphicsView(QtGui.QWidget):
    __doc__ = '\n    Replacement for GraphicsView that does all scene management and rendering on a remote process,\n    while displaying on the local widget.\n    \n    GraphicsItems must be created by proxy to the remote process.\n    \n    '

    def __init__(self, parent=None, *args, **kwds):
        """
        The keyword arguments 'useOpenGL' and 'backgound', if specified, are passed to the remote
        GraphicsView.__init__(). All other keyword arguments are passed to multiprocess.QtProcess.__init__().
        """
        self._img = None
        self._imgReq = None
        self._sizeHint = (640, 480)
        QtGui.QWidget.__init__(self)
        remoteKwds = {}
        for kwd in ('useOpenGL', 'background'):
            if kwd in kwds:
                remoteKwds[kwd] = kwds.pop(kwd)

        self._proc = (mp.QtProcess)(**kwds)
        self.pg = self._proc._import('pyqtgraph')
        (self.pg.setConfigOptions)(**CONFIG_OPTIONS)
        rpgRemote = self._proc._import('pyqtgraph.widgets.RemoteGraphicsView')
        self._view = (rpgRemote.Renderer)(*args, **remoteKwds)
        self._view._setProxyOptions(deferGetattr=True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setMouseTracking(True)
        self.shm = None
        shmFileName = self._view.shmFileName()
        if sys.platform.startswith('win'):
            self.shmtag = shmFileName
        else:
            self.shmFile = open(shmFileName, 'r')
        self._view.sceneRendered.connect(mp.proxy(self.remoteSceneChanged))
        for method in ('scene', 'setCentralItem'):
            setattr(self, method, getattr(self._view, method))

    def resizeEvent(self, ev):
        ret = QtGui.QWidget.resizeEvent(self, ev)
        self._view.resize((self.size()), _callSync='off')
        return ret

    def sizeHint(self):
        return (QtCore.QSize)(*self._sizeHint)

    def remoteSceneChanged(self, data):
        w, h, size, newfile = data
        if self.shm is None or self.shm.size != size:
            if self.shm is not None:
                self.shm.close()
            if sys.platform.startswith('win'):
                self.shmtag = newfile
                self.shm = mmap.mmap(-1, size, self.shmtag)
        else:
            self.shm = mmap.mmap(self.shmFile.fileno(), size, mmap.MAP_SHARED, mmap.PROT_READ)
        self.shm.seek(0)
        data = self.shm.read(w * h * 4)
        self._img = QtGui.QImage(data, w, h, QtGui.QImage.Format_ARGB32)
        self._img.data = data
        self.update()

    def paintEvent(self, ev):
        if self._img is None:
            return
        p = QtGui.QPainter(self)
        p.drawImage(self.rect(), self._img, QtCore.QRect(0, 0, self._img.width(), self._img.height()))
        p.end()

    def mousePressEvent(self, ev):
        self._view.mousePressEvent((int(ev.type())), (ev.pos()), (ev.globalPos()), (int(ev.button())), (int(ev.buttons())), (int(ev.modifiers())), _callSync='off')
        ev.accept()
        return QtGui.QWidget.mousePressEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        self._view.mouseReleaseEvent((int(ev.type())), (ev.pos()), (ev.globalPos()), (int(ev.button())), (int(ev.buttons())), (int(ev.modifiers())), _callSync='off')
        ev.accept()
        return QtGui.QWidget.mouseReleaseEvent(self, ev)

    def mouseMoveEvent(self, ev):
        self._view.mouseMoveEvent((int(ev.type())), (ev.pos()), (ev.globalPos()), (int(ev.button())), (int(ev.buttons())), (int(ev.modifiers())), _callSync='off')
        ev.accept()
        return QtGui.QWidget.mouseMoveEvent(self, ev)

    def wheelEvent(self, ev):
        self._view.wheelEvent((ev.pos()), (ev.globalPos()), (ev.delta()), (int(ev.buttons())), (int(ev.modifiers())), (int(ev.orientation())), _callSync='off')
        ev.accept()
        return QtGui.QWidget.wheelEvent(self, ev)

    def keyEvent(self, ev):
        if self._view.keyEvent(int(ev.type()), int(ev.modifiers()), text, autorep, count):
            ev.accept()
        return QtGui.QWidget.keyEvent(self, ev)

    def enterEvent(self, ev):
        self._view.enterEvent((int(ev.type())), _callSync='off')
        return QtGui.QWidget.enterEvent(self, ev)

    def leaveEvent(self, ev):
        self._view.leaveEvent((int(ev.type())), _callSync='off')
        return QtGui.QWidget.leaveEvent(self, ev)

    def remoteProcess(self):
        """Return the remote process handle. (see multiprocess.remoteproxy.RemoteEventHandler)"""
        return self._proc

    def close(self):
        """Close the remote process. After this call, the widget will no longer be updated."""
        self._proc.close()


class Renderer(GraphicsView):
    sceneRendered = QtCore.Signal(object)

    def __init__(self, *args, **kwds):
        if sys.platform.startswith('win'):
            self.shmtag = 'pyqtgraph_shmem_' + ''.join([chr(random.getrandbits(20) % 25 + 97) for i in range(20)])
            self.shm = mmap.mmap(-1, mmap.PAGESIZE, self.shmtag)
        else:
            self.shmFile = tempfile.NamedTemporaryFile(prefix='pyqtgraph_shmem_')
            self.shmFile.write(b'\x00' * (mmap.PAGESIZE + 1))
            fd = self.shmFile.fileno()
            self.shm = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)
        atexit.register(self.close)
        (GraphicsView.__init__)(self, *args, **kwds)
        self.scene().changed.connect(self.update)
        self.img = None
        self.renderTimer = QtCore.QTimer()
        self.renderTimer.timeout.connect(self.renderView)
        self.renderTimer.start(16)

    def close(self):
        self.shm.close()
        if not sys.platform.startswith('win'):
            self.shmFile.close()

    def shmFileName(self):
        if sys.platform.startswith('win'):
            return self.shmtag
        return self.shmFile.name

    def update(self):
        self.img = None
        return GraphicsView.update(self)

    def resize(self, size):
        oldSize = self.size()
        GraphicsView.resize(self, size)
        self.resizeEvent(QtGui.QResizeEvent(size, oldSize))
        self.update()

    def renderView(self):
        if self.img is None:
            if not self.width() == 0:
                if self.height() == 0:
                    return
                size = self.width() * self.height() * 4
                if size > self.shm.size():
                    if sys.platform.startswith('win'):
                        self.shm.close()
                        self.shmtag = 'pyqtgraph_shmem_' + ''.join([chr(random.getrandbits(20) % 25 + 97) for i in range(20)])
                        self.shm = mmap.mmap(-1, size, self.shmtag)
            else:
                self.shm.resize(size)
            if USE_PYSIDE:
                ch = ctypes.c_char.from_buffer(self.shm, 0)
                self.img = QtGui.QImage(ch, self.width(), self.height(), QtGui.QImage.Format_ARGB32)
            else:
                address = ctypes.addressof(ctypes.c_char.from_buffer(self.shm, 0))
                try:
                    self.img = QtGui.QImage(sip.voidptr(address), self.width(), self.height(), QtGui.QImage.Format_ARGB32)
                except TypeError:
                    try:
                        self.img = QtGui.QImage(memoryview(buffer(self.shm)), self.width(), self.height(), QtGui.QImage.Format_ARGB32)
                    except TypeError:
                        self.img = QtGui.QImage(address, self.width(), self.height(), QtGui.QImage.Format_ARGB32)

                self.img.fill(4294967295)
                p = QtGui.QPainter(self.img)
                self.render(p, self.viewRect(), self.rect())
                p.end()
                self.sceneRendered.emit((self.width(), self.height(), self.shm.size(), self.shmFileName()))

    def mousePressEvent(self, typ, pos, gpos, btn, btns, mods):
        typ = QtCore.QEvent.Type(typ)
        btn = QtCore.Qt.MouseButton(btn)
        btns = QtCore.Qt.MouseButtons(btns)
        mods = QtCore.Qt.KeyboardModifiers(mods)
        return GraphicsView.mousePressEvent(self, QtGui.QMouseEvent(typ, pos, gpos, btn, btns, mods))

    def mouseMoveEvent(self, typ, pos, gpos, btn, btns, mods):
        typ = QtCore.QEvent.Type(typ)
        btn = QtCore.Qt.MouseButton(btn)
        btns = QtCore.Qt.MouseButtons(btns)
        mods = QtCore.Qt.KeyboardModifiers(mods)
        return GraphicsView.mouseMoveEvent(self, QtGui.QMouseEvent(typ, pos, gpos, btn, btns, mods))

    def mouseReleaseEvent(self, typ, pos, gpos, btn, btns, mods):
        typ = QtCore.QEvent.Type(typ)
        btn = QtCore.Qt.MouseButton(btn)
        btns = QtCore.Qt.MouseButtons(btns)
        mods = QtCore.Qt.KeyboardModifiers(mods)
        return GraphicsView.mouseReleaseEvent(self, QtGui.QMouseEvent(typ, pos, gpos, btn, btns, mods))

    def wheelEvent(self, pos, gpos, d, btns, mods, ori):
        btns = QtCore.Qt.MouseButtons(btns)
        mods = QtCore.Qt.KeyboardModifiers(mods)
        ori = (None, QtCore.Qt.Horizontal, QtCore.Qt.Vertical)[ori]
        return GraphicsView.wheelEvent(self, QtGui.QWheelEvent(pos, gpos, d, btns, mods, ori))

    def keyEvent(self, typ, mods, text, autorep, count):
        typ = QtCore.QEvent.Type(typ)
        mods = QtCore.Qt.KeyboardModifiers(mods)
        GraphicsView.keyEvent(self, QtGui.QKeyEvent(typ, mods, text, autorep, count))
        return ev.accepted()

    def enterEvent(self, typ):
        ev = QtCore.QEvent(QtCore.QEvent.Type(typ))
        return GraphicsView.enterEvent(self, ev)

    def leaveEvent(self, typ):
        ev = QtCore.QEvent(QtCore.QEvent.Type(typ))
        return GraphicsView.leaveEvent(self, ev)