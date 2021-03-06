# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/scene/cameras/magnify.py
# Compiled at: 2016-11-03 01:40:19
from __future__ import division
import numpy as np
from .panzoom import PanZoomCamera
from ...visuals.transforms.nonlinear import MagnifyTransform, Magnify1DTransform
from ...app import Timer

class MagnifyCamera(PanZoomCamera):
    """Camera implementing a MagnifyTransform combined with PanZoomCamera.
    
    Parameters
    ----------
    size_factor : float
        The size factor to use.
    radius_ratio : float
        The radius ratio to use.
    **kwargs : dict
        Keyword arguments to pass to `PanZoomCamera` and create a transform.

    Notes
    -----
    This Camera uses the mouse cursor position to set the center position of
    the MagnifyTransform, and uses mouse wheel events to adjust the 
    magnification factor.
    
    At high magnification, very small mouse movements can result in large
    changes, so we use a timer to animate transitions in the transform 
    properties.
    
    The camera also adjusts the size of its "lens" area when the view is
    resized.

    """
    transform_class = MagnifyTransform

    def __init__(self, size_factor=0.25, radius_ratio=0.9, **kwargs):
        self.size_factor = size_factor
        self.radius_ratio = radius_ratio
        camkwargs = {}
        for key in ('parent', 'name', 'rect', 'aspect'):
            if key in kwargs:
                camkwargs[key] = kwargs.pop(key)

        self.mag = self.transform_class(**kwargs)
        self.mag_target = self.mag.mag
        self.mag._mag = self.mag_target
        self.mouse_pos = None
        self.timer = Timer(interval=0.016, connect=self.on_timer)
        super(MagnifyCamera, self).__init__(**camkwargs)
        self.pre_transform = self.mag
        return

    def _viewbox_set(self, viewbox):
        PanZoomCamera._viewbox_set(self, viewbox)

    def _viewbox_unset(self, viewbox):
        PanZoomCamera._viewbox_unset(self, viewbox)
        self.timer.stop()

    def viewbox_mouse_event(self, event):
        """ViewBox mouse event handler

        Parameters
        ----------
        event : instance of Event
            The mouse event.
        """
        self.mouse_pos = event.pos[:2]
        if event.type == 'mouse_wheel':
            m = self.mag_target
            m *= 1.2 ** event.delta[1]
            m = m if m > 1 else 1
            self.mag_target = m
        else:
            super(MagnifyCamera, self).viewbox_mouse_event(event)
        if not self.timer.running:
            self.timer.start()
        self._update_transform()

    def on_timer(self, event=None):
        """Timer event handler

        Parameters
        ----------
        event : instance of Event
            The timer event.
        """
        k = np.clip(100.0 / self.mag.mag, 10, 100)
        s = 10 ** (-k * event.dt)
        c = np.array(self.mag.center)
        c1 = c * s + self.mouse_pos * (1 - s)
        m = self.mag.mag * s + self.mag_target * (1 - s)
        if np.all(np.abs((c - c1) / c1) < 1e-05) and np.abs(np.log(m / self.mag.mag)) < 0.001:
            self.timer.stop()
        self.mag.center = c1
        self.mag.mag = m
        self._update_transform()

    def viewbox_resize_event(self, event):
        """ViewBox resize event handler

        Parameters
        ----------
        event : instance of Event
            The viewbox resize event.
        """
        PanZoomCamera.viewbox_resize_event(self, event)
        self.view_changed()

    def view_changed(self):
        if self._viewbox is not None:
            vbs = self._viewbox.size
            r = min(vbs) * self.size_factor
            self.mag.radii = (r * self.radius_ratio, r)
        PanZoomCamera.view_changed(self)
        return


class Magnify1DCamera(MagnifyCamera):
    transform_class = Magnify1DTransform
    __doc__ = MagnifyCamera.__doc__