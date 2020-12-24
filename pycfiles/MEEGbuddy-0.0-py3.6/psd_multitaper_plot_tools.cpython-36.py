# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/MEEGbuddy/psd_multitaper_plot_tools.py
# Compiled at: 2019-02-12 17:24:47
# Size of source mod 2**32: 6153 bytes
import numpy as np, matplotlib.pyplot as plt
from matplotlib.widgets import Button

class DraggableResizeableRectangle:
    __doc__ = '\n    Draggable and resizeable rectangle with the animation blit techniques.\n    Based on example code at\n    http://matplotlib.sourceforge.net/users/event_handling.html\n    If *allow_resize* is *True* the recatngle can be resized by dragging its\n    lines. *border_tol* specifies how close the pointer has to be to a line for\n    the drag to be considered a resize operation. Dragging is still possible by\n    clicking the interior of the rectangle. *fixed_aspect_ratio* determines if\n    the recatngle keeps its aspect ratio during resize operations.\n    '
    lock = None

    def __init__(self, rect, border_tol=0.15, allow_resize=True, fixed_aspect_ratio=True):
        self.rect = rect
        self.border_tol = border_tol
        self.allow_resize = allow_resize
        self.fixed_aspect_ratio = fixed_aspect_ratio
        self.press = None
        self.background = None

    def connect(self):
        """connect to all the events we need"""
        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        """on button press we will see if the mouse is over us and store some data"""
        if event.inaxes != self.rect.axes:
            return
        else:
            if DraggableResizeableRectangle.lock is not None:
                return
            else:
                contains, attrd = self.rect.contains(event)
                return contains or None
        x0, y0 = self.rect.xy
        w0, h0 = self.rect.get_width(), self.rect.get_height()
        aspect_ratio = np.true_divide(w0, h0)
        self.press = (x0, y0, w0, h0, aspect_ratio, event.xdata, event.ydata)
        DraggableResizeableRectangle.lock = self
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        self.rect.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)
        axes.draw_artist(self.rect)
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        """on motion we will move the rect if the mouse is over us"""
        if DraggableResizeableRectangle.lock is not self:
            return
        if event.inaxes != self.rect.axes:
            return
        x0, y0, w0, h0, aspect_ratio, xpress, ypress = self.press
        self.dx = event.xdata - xpress
        self.dy = event.ydata - ypress
        self.update_rect()
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.rect)
        canvas.blit(axes.bbox)

    def on_release(self, event):
        """on release we reset the press data"""
        if DraggableResizeableRectangle.lock is not self:
            return
        self.press = None
        DraggableResizeableRectangle.lock = None
        self.rect.set_animated(False)
        self.background = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        """disconnect all the stored connection ids"""
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

    def update_rect(self):
        x0, y0, w0, h0, aspect_ratio, xpress, ypress = self.press
        dx, dy = self.dx, self.dy
        bt = self.border_tol
        fixed_ar = self.fixed_aspect_ratio
        if not self.allow_resize or abs(x0 + np.true_divide(w0, 2) - xpress) < np.true_divide(w0, 2) - bt * w0 and abs(y0 + np.true_divide(h0, 2) - ypress) < np.true_divide(h0, 2) - bt * h0:
            self.rect.set_x(x0 + dx)
            self.rect.set_y(y0 + dy)
        else:
            if abs(x0 - xpress) < bt * w0:
                self.rect.set_x(x0 + dx)
                self.rect.set_width(w0 - dx)
                if fixed_ar:
                    dy = np.true_divide(dx, aspect_ratio)
                    self.rect.set_y(y0 + dy)
                    self.rect.set_height(h0 - dy)
            else:
                if abs(x0 + w0 - xpress) < bt * w0:
                    self.rect.set_width(w0 + dx)
                    if fixed_ar:
                        dy = np.true_divide(dx, aspect_ratio)
                        self.rect.set_height(h0 + dy)
                else:
                    if abs(y0 - ypress) < bt * h0:
                        self.rect.set_y(y0 + dy)
                        self.rect.set_height(h0 - dy)
                        if fixed_ar:
                            dx = dy * aspect_ratio
                            self.rect.set_x(x0 + dx)
                            self.rect.set_width(w0 - dx)
                    elif abs(y0 + h0 - ypress) < bt * h0:
                        self.rect.set_height(h0 + dy)
                        if fixed_ar:
                            dx = dy * aspect_ratio
                            self.rect.set_width(w0 + dx)


class ButtonClickProcessor(object):

    def __init__(self, label_ax, label, color, ax, drs, image):
        self.ax = ax
        self.drs = drs
        self.image = image
        self.color = color
        self.label = label
        self.button = Button(label_ax, label, color=color)
        self.button.on_clicked(self.process)

    def process(self, event):
        rect = self.ax.bar((self.image.shape[1] / 20), (self.image.shape[0] * 0.9), (self.image.shape[1] / 10),
          edgecolor=(self.color), fill=False,
          linewidth=1)
        rect = rect[0]
        dr = DraggableResizeableRectangle(rect, fixed_aspect_ratio=False)
        dr.connect()
        self.drs[self.label].append(dr)