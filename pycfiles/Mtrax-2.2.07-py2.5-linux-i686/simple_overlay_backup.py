# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/simple_overlay_backup.py
# Compiled at: 2008-02-01 11:07:49
import wx, wx.xrc as xrc, pkg_resources, numpy, motmot.imops.imops as imops, pyglet.gl as gl
from pygarrayimage.arrayimage import ArrayInterfaceImage
import motmot.wxglvideo.wxglvideo as vid

class PointDisplayCanvas(vid.DynamicImageCanvas):

    def __init__(self, *args, **kw):
        super(PointDisplayCanvas, self).__init__(*args, **kw)
        self.extra_points_linesegs = (None, None, None, None)
        self.red_points = None
        return

    def core_draw(self):
        super(PointDisplayCanvas, self).core_draw()
        (points, point_colors, linesegs, lineseg_colors) = self.extra_points_linesegs
        gl.glColor4f(0.0, 1.0, 0.0, 1.0)
        if points is not None:
            if point_colors is None:
                point_colors = [
                 (0, 1, 0, 1)] * len(points)
            gl.glBegin(gl.GL_POINTS)
            for (color_4tuple, pt) in zip(point_colors, points):
                gl.glColor4f(*color_4tuple)
                gl.glVertex2f(pt[0], pt[1])

            gl.glEnd()
        if linesegs is not None:
            if lineseg_colors is None:
                lineseg_colors = [
                 (0, 1, 0, 1)] * len(linesegs)
            gl.glBegin(gl.GL_LINES)
            for (color_4tuple, (x0, y0, x1, y1)) in zip(lineseg_colors, linesegs):
                gl.glColor4f(*color_4tuple)
                gl.glVertex2f(x0, y0)
                gl.glVertex2f(x1, y1)

            gl.glEnd()
        if self.red_points is not None:
            gl.glColor4f(1.0, 0.0, 0.0, 1.0)
            gl.glBegin(gl.GL_POINTS)
            for pt in self.red_points:
                gl.glVertex2f(pt[0], pt[1])

            gl.glEnd()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        return

    def extra_initgl(self):
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glPointSize(5)


class DynamicImageCanvas(wx.Panel):

    def __init__(self, *args, **kw):
        super(DynamicImageCanvas, self).__init__(*args, **kw)
        self.rotate_180 = False
        self.flip_lr = False
        self.children = {}
        self.lbrt = {}
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.box)

    def _new_child(self, id_val, image):
        child = PointDisplayCanvas(self, -1)
        child.set_fullcanvas(True)
        self.box.Add(child, 1, wx.EXPAND)
        self.Layout()
        pygim = ArrayInterfaceImage(image, allow_copy=False)
        child.new_image(pygim)
        child.set_rotate_180(self.rotate_180)
        child.set_flip_lr(self.flip_lr)
        self.children[id_val] = child
        self.lbrt[id_val] = ()

    def set_rotate_180(self, value):
        self.rotate_180 = value
        for id_val in self.children:
            child = self.children[id_val]
            child.set_rotate_180(value)

    def set_flip_LR(self, value):
        self.flip_lr = value
        for id_val in self.children:
            child = self.children[id_val]
            child.set_flip_lr(value)

    def set_red_points(self, id_val, points):
        try:
            child = self.children[id_val]
        except KeyError:
            pass
        else:
            child.red_points = points

    def set_lbrt(self, id_val, lbrt):
        self.lbrt[id_val] = lbrt

    def get_child_canvas(self, id_val):
        if id_val not in self.children:
            return
        else:
            return self.children[id_val]
        return

    def update_image(self, id_val, image, format='MONO8', xoffset=0, yoffset=0):
        image = numpy.asarray(image)
        if format == 'RGB8':
            image = imops.rgb8_to_rgb8(image)
        elif format == 'ARGB8':
            image = imops.argb8_to_rgb8(image)
        elif format == 'YUV411':
            image = imops.yuv411_to_rgb8(image)
        elif format == 'YUV422':
            image = imops.yuv422_to_rgb8(image)
        elif format == 'MONO8':
            pass
        elif format == 'RAW8':
            pass
        elif format == 'MONO16':
            image = imops.mono16_to_mono8_middle8bits(image)
        else:
            raise ValueError("Unknown format '%s'" % (format,))
        if id_val not in self.children:
            self._new_child(id_val, image)
        else:
            child = self.children[id_val]
            child.update_image(image)

    def update_image_and_drawings(self, id_val, image, format='MONO8', points=None, point_colors=None, linesegs=None, lineseg_colors=None, xoffset=0, yoffset=0):
        try:
            child = self.children[id_val]
        except KeyError:
            pass
        else:
            child.extra_points_linesegs = (
             points, point_colors, linesegs, lineseg_colors)

        self.update_image(id_val, image, format=format, xoffset=xoffset, yoffset=yoffset)

    def OnDraw(self):
        for id_val in self.children:
            child = self.children[id_val]
            child.OnDraw()

    def OnIdle(self, event):
        for id_val in self.children:
            child = self.children[id_val]
            child.OnDraw()

        event.RequestMore(True)