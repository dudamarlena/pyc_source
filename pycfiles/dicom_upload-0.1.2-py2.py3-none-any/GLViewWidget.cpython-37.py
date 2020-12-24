# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/GLViewWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 18189 bytes
from ..Qt import QtCore, QtGui, QtOpenGL, USE_PYQT5
from OpenGL.GL import *
import OpenGL.GL.framebufferobjects as glfbo
import numpy as np
from .. import Vector
from .. import functions as fn
ShareWidget = None

class GLViewWidget(QtOpenGL.QGLWidget):
    """GLViewWidget"""

    def __init__(self, parent=None):
        global ShareWidget
        if ShareWidget is None:
            ShareWidget = QtOpenGL.QGLWidget()
        QtOpenGL.QGLWidget.__init__(self, parent, ShareWidget)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.opts = {'center':Vector(0, 0, 0), 
         'distance':10.0, 
         'fov':60, 
         'elevation':30, 
         'azimuth':45, 
         'viewport':None}
        self.setBackgroundColor('k')
        self.items = []
        self.noRepeatKeys = [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]
        self.keysPressed = {}
        self.keyTimer = QtCore.QTimer()
        self.keyTimer.timeout.connect(self.evalKeyState)
        self.makeCurrent()

    def addItem(self, item):
        self.items.append(item)
        if hasattr(item, 'initializeGL'):
            self.makeCurrent()
            try:
                item.initializeGL()
            except:
                self.checkOpenGLVersion('Error while adding item %s to GLViewWidget.' % str(item))

        item._setView(self)
        self.update()

    def removeItem(self, item):
        self.items.remove(item)
        item._setView(None)
        self.update()

    def initializeGL(self):
        self.resizeGL(self.width(), self.height())

    def setBackgroundColor(self, *args, **kwds):
        """
        Set the background color of the widget. Accepts the same arguments as
        pg.mkColor().
        """
        self.opts['bgcolor'] = (fn.mkColor)(*args, **kwds)
        self.update()

    def getViewport(self):
        vp = self.opts['viewport']
        if vp is None:
            return (0, 0, self.width(), self.height())
        return vp

    def resizeGL(self, w, h):
        pass

    def setProjection(self, region=None):
        m = self.projectionMatrix(region)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        a = np.array(m.copyDataTo()).reshape((4, 4))
        glMultMatrixf(a.transpose())

    def projectionMatrix(self, region=None):
        if region is None:
            region = (
             0, 0, self.width(), self.height())
        x0, y0, w, h = self.getViewport()
        dist = self.opts['distance']
        fov = self.opts['fov']
        nearClip = dist * 0.001
        farClip = dist * 1000.0
        r = nearClip * np.tan(fov * 0.5 * np.pi / 180.0)
        t = r * h / w
        left = r * ((region[0] - x0) * (2.0 / w) - 1)
        right = r * ((region[0] + region[2] - x0) * (2.0 / w) - 1)
        bottom = t * ((region[1] - y0) * (2.0 / h) - 1)
        top = t * ((region[1] + region[3] - y0) * (2.0 / h) - 1)
        tr = QtGui.QMatrix4x4()
        tr.frustum(left, right, bottom, top, nearClip, farClip)
        return tr

    def setModelview(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        m = self.viewMatrix()
        a = np.array(m.copyDataTo()).reshape((4, 4))
        glMultMatrixf(a.transpose())

    def viewMatrix(self):
        tr = QtGui.QMatrix4x4()
        tr.translate(0.0, 0.0, -self.opts['distance'])
        tr.rotate(self.opts['elevation'] - 90, 1, 0, 0)
        tr.rotate(self.opts['azimuth'] + 90, 0, 0, -1)
        center = self.opts['center']
        tr.translate(-center.x(), -center.y(), -center.z())
        return tr

    def itemsAt(self, region=None):
        """
        Return a list of the items displayed in the region (x, y, w, h)
        relative to the widget.        
        """
        region = (
         region[0], self.height() - (region[1] + region[3]), region[2], region[3])
        buf = glSelectBuffer(100000)
        try:
            glRenderMode(GL_SELECT)
            glInitNames()
            glPushName(0)
            self._itemNames = {}
            self.paintGL(region=region, useItemNames=True)
        finally:
            hits = glRenderMode(GL_RENDER)

        items = [(h.near, h.names[0]) for h in hits]
        items.sort(key=(lambda i: i[0]))
        return [self._itemNames[i[1]] for i in items]

    def paintGL(self, region=None, viewport=None, useItemNames=False):
        """
        viewport specifies the arguments to glViewport. If None, then we use self.opts['viewport']
        region specifies the sub-region of self.opts['viewport'] that should be rendered.
        Note that we may use viewport != self.opts['viewport'] when exporting.
        """
        if viewport is None:
            glViewport(*self.getViewport())
        else:
            glViewport(*viewport)
        self.setProjection(region=region)
        self.setModelview()
        bgcolor = self.opts['bgcolor']
        glClearColor(bgcolor.red(), bgcolor.green(), bgcolor.blue(), 1.0)
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        self.drawItemTree(useItemNames=useItemNames)

    def drawItemTree(self, item=None, useItemNames=False):
        if item is None:
            items = [x for x in self.items if x.parentItem() is None]
        else:
            items = item.childItems()
            items.append(item)
        items.sort(key=(lambda a: a.depthValue()))
        for i in items:
            if not i.visible():
                continue
            if i is item:
                try:
                    try:
                        glPushAttrib(GL_ALL_ATTRIB_BITS)
                        if useItemNames:
                            glLoadName(i._id)
                            self._itemNames[i._id] = i
                        i.paint()
                    except:
                        from .. import debug
                        debug.printExc()
                        msg = 'Error while drawing item %s.' % str(item)
                        ver = glGetString(GL_VERSION)
                        if ver is not None:
                            ver = ver.split()[0]
                            if int(ver.split('.')[0]) < 2:
                                print(msg + ' The original exception is printed above; however, pyqtgraph requires OpenGL version 2.0 or greater for many of its 3D features and your OpenGL version is %s. Installing updated display drivers may resolve this issue.' % ver)
                            else:
                                print(msg)

                finally:
                    glPopAttrib()

            else:
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                try:
                    tr = i.transform()
                    a = np.array(tr.copyDataTo()).reshape((4, 4))
                    glMultMatrixf(a.transpose())
                    self.drawItemTree(i, useItemNames=useItemNames)
                finally:
                    glMatrixMode(GL_MODELVIEW)
                    glPopMatrix()

    def setCameraPosition(self, pos=None, distance=None, elevation=None, azimuth=None):
        if distance is not None:
            self.opts['distance'] = distance
        if elevation is not None:
            self.opts['elevation'] = elevation
        if azimuth is not None:
            self.opts['azimuth'] = azimuth
        self.update()

    def cameraPosition(self):
        """Return current position of camera based on center, dist, elevation, and azimuth"""
        center = self.opts['center']
        dist = self.opts['distance']
        elev = self.opts['elevation'] * np.pi / 180.0
        azim = self.opts['azimuth'] * np.pi / 180.0
        pos = Vector(center.x() + dist * np.cos(elev) * np.cos(azim), center.y() + dist * np.cos(elev) * np.sin(azim), center.z() + dist * np.sin(elev))
        return pos

    def orbit(self, azim, elev):
        """Orbits the camera around the center position. *azim* and *elev* are given in degrees."""
        self.opts['azimuth'] += azim
        self.opts['elevation'] = np.clip(self.opts['elevation'] + elev, -90, 90)
        self.update()

    def pan(self, dx, dy, dz, relative=False):
        """
        Moves the center (look-at) position while holding the camera in place. 
        
        If relative=True, then the coordinates are interpreted such that x
        if in the global xy plane and points to the right side of the view, y is
        in the global xy plane and orthogonal to x, and z points in the global z
        direction. Distances are scaled roughly such that a value of 1.0 moves
        by one pixel on screen.
        
        """
        if not relative:
            self.opts['center'] += QtGui.QVector3D(dx, dy, dz)
        else:
            cPos = self.cameraPosition()
            cVec = self.opts['center'] - cPos
            dist = cVec.length()
            xDist = dist * 2.0 * np.tan(0.5 * self.opts['fov'] * np.pi / 180.0)
            xScale = xDist / self.width()
            zVec = QtGui.QVector3D(0, 0, 1)
            xVec = QtGui.QVector3D.crossProduct(zVec, cVec).normalized()
            yVec = QtGui.QVector3D.crossProduct(xVec, zVec).normalized()
            self.opts['center'] = self.opts['center'] + xVec * xScale * dx + yVec * xScale * dy + zVec * xScale * dz
        self.update()

    def pixelSize(self, pos):
        """
        Return the approximate size of a screen pixel at the location pos
        Pos may be a Vector or an (N,3) array of locations
        """
        cam = self.cameraPosition()
        if isinstance(pos, np.ndarray):
            cam = np.array(cam).reshape((1, ) * (pos.ndim - 1) + (3, ))
            dist = ((pos - cam) ** 2).sum(axis=(-1)) ** 0.5
        else:
            dist = (pos - cam).length()
        xDist = dist * 2.0 * np.tan(0.5 * self.opts['fov'] * np.pi / 180.0)
        return xDist / self.width()

    def mousePressEvent(self, ev):
        self.mousePos = ev.pos()

    def mouseMoveEvent(self, ev):
        diff = ev.pos() - self.mousePos
        self.mousePos = ev.pos()
        if ev.buttons() == QtCore.Qt.LeftButton:
            self.orbit(-diff.x(), diff.y())
        elif ev.buttons() == QtCore.Qt.MidButton:
            if ev.modifiers() & QtCore.Qt.ControlModifier:
                self.pan((diff.x()), 0, (diff.y()), relative=True)
            else:
                self.pan((diff.x()), (diff.y()), 0, relative=True)

    def mouseReleaseEvent(self, ev):
        pass

    def wheelEvent(self, ev):
        delta = 0
        if not USE_PYQT5:
            delta = ev.delta()
        else:
            delta = ev.angleDelta().x()
        if delta == 0:
            delta = ev.angleDelta().y()
        elif ev.modifiers() & QtCore.Qt.ControlModifier:
            self.opts['fov'] *= 0.999 ** delta
        else:
            self.opts['distance'] *= 0.999 ** delta
        self.update()

    def keyPressEvent(self, ev):
        if ev.key() in self.noRepeatKeys:
            ev.accept()
            if ev.isAutoRepeat():
                return
            self.keysPressed[ev.key()] = 1
            self.evalKeyState()

    def keyReleaseEvent(self, ev):
        if ev.key() in self.noRepeatKeys:
            ev.accept()
            if ev.isAutoRepeat():
                return
            try:
                del self.keysPressed[ev.key()]
            except:
                self.keysPressed = {}

            self.evalKeyState()

    def evalKeyState(self):
        speed = 2.0
        if len(self.keysPressed) > 0:
            for key in self.keysPressed:
                if key == QtCore.Qt.Key_Right:
                    self.orbit(azim=(-speed), elev=0)
                elif key == QtCore.Qt.Key_Left:
                    self.orbit(azim=speed, elev=0)
                elif key == QtCore.Qt.Key_Up:
                    self.orbit(azim=0, elev=(-speed))
                elif key == QtCore.Qt.Key_Down:
                    self.orbit(azim=0, elev=speed)
                elif key == QtCore.Qt.Key_PageUp:
                    pass
                elif key == QtCore.Qt.Key_PageDown:
                    pass
                self.keyTimer.start(16)

        else:
            self.keyTimer.stop()

    def checkOpenGLVersion(self, msg):
        ver = glGetString(GL_VERSION).split()[0]
        if int(ver.split('.')[0]) < 2:
            from .. import debug
            pyqtgraph.debug.printExc()
            raise Exception(msg + ' The original exception is printed above; however, pyqtgraph requires OpenGL version 2.0 or greater for many of its 3D features and your OpenGL version is %s. Installing updated display drivers may resolve this issue.' % ver)
        else:
            raise

    def readQImage(self):
        """
        Read the current buffer pixels out as a QImage.
        """
        w = self.width()
        h = self.height()
        self.repaint()
        pixels = np.empty((h, w, 4), dtype=(np.ubyte))
        pixels[:] = 128
        pixels[(Ellipsis, 0)] = 50
        pixels[(Ellipsis, 3)] = 255
        glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
        tmp = pixels[(Ellipsis, 0)].copy()
        pixels[(Ellipsis, 0)] = pixels[(Ellipsis, 2)]
        pixels[(Ellipsis, 2)] = tmp
        pixels = pixels[::-1]
        img = fn.makeQImage(pixels, transpose=False)
        return img

    def renderToArray(self, size, format=GL_BGRA, type=GL_UNSIGNED_BYTE, textureSize=1024, padding=256):
        w, h = map(int, size)
        self.makeCurrent()
        tex = None
        fb = None
        try:
            output = np.empty((w, h, 4), dtype=(np.ubyte))
            fb = glfbo.glGenFramebuffers(1)
            glfbo.glBindFramebuffer(glfbo.GL_FRAMEBUFFER, fb)
            glEnable(GL_TEXTURE_2D)
            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            texwidth = textureSize
            data = np.zeros((texwidth, texwidth, 4), dtype=(np.ubyte))
            glTexImage2D(GL_PROXY_TEXTURE_2D, 0, GL_RGBA, texwidth, texwidth, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
            if glGetTexLevelParameteriv(GL_PROXY_TEXTURE_2D, 0, GL_TEXTURE_WIDTH) == 0:
                raise Exception('OpenGL failed to create 2D texture (%dx%d); too large for this hardware.' % shape[:2])
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texwidth, texwidth, 0, GL_RGBA, GL_UNSIGNED_BYTE, data.transpose((1,
                                                                                                                      0,
                                                                                                                      2)))
            self.opts['viewport'] = (
             0, 0, w, h)
            p2 = 2 * padding
            for x in range(-padding, w - padding, texwidth - p2):
                for y in range(-padding, h - padding, texwidth - p2):
                    x2 = min(x + texwidth, w + padding)
                    y2 = min(y + texwidth, h + padding)
                    w2 = x2 - x
                    h2 = y2 - y
                    glfbo.glFramebufferTexture2D(glfbo.GL_FRAMEBUFFER, glfbo.GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0)
                    self.paintGL(region=(x, h - y - h2, w2, h2), viewport=(0, 0, w2, h2))
                    data = glGetTexImage(GL_TEXTURE_2D, 0, format, type)
                    data = np.fromstring(data, dtype=(np.ubyte)).reshape(texwidth, texwidth, 4).transpose(1, 0, 2)[:, ::-1]
                    output[x + padding:x2 - padding, y + padding:y2 - padding] = data[padding:w2 - padding, -(h2 - padding):-padding]

        finally:
            self.opts['viewport'] = None
            glfbo.glBindFramebuffer(glfbo.GL_FRAMEBUFFER, 0)
            glBindTexture(GL_TEXTURE_2D, 0)
            if tex is not None:
                glDeleteTextures([tex])
            if fb is not None:
                glfbo.glDeleteFramebuffers([fb])

        return output