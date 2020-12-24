# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/misc.py
# Compiled at: 2003-05-13 05:44:11
from nxplot import *

class CanvasObjectBase(NxpCanvasObject):

    def real_draw(self, pl):
        pass

    def real_configure(self, new_bbox, interaction):
        pass

    def real_size_request(self):
        return NxplotPoint(0, 0)

    def real_enter(self):
        pass

    def real_leave(self):
        pass

    def real_button_press(self, event):
        pass

    def real_button_release(self, event):
        pass

    def real_motion_notify(self, event):
        pass

    def __init__(self):
        NxpCanvasObject.__init__(self)
        self._set_drawable(1)
        self._set_visible(1)
        self.set_property('interaction-mask', 0)
        self.connect('draw', self.__class__.real_draw)
        self.connect('configure', self.__class__.real_configure)
        self.connect('size-request', self.__class__.real_size_request)
        self.connect('enter', self.__class__.real_enter)
        self.connect('leave', self.__class__.real_leave)
        self.connect('button-press', self.__class__.real_button_press)
        self.connect('button-release', self.__class__.real_button_release)
        self.connect('motion-notify', self.__class__.real_motion_notify)


class CanvasContainerBase(NxpCanvasContainer):

    def real_draw(self, pl):
        pass

    def real_configure(self, new_bbox, interaction):
        pass

    def real_size_request(self):
        return NxplotPoint(0, 0)

    def real_enter(self):
        pass

    def real_leave(self):
        pass

    def real_get_children(self):
        pass

    def real_get_child_at_point(self, x, y):
        pass

    def real_button_press(self, event):
        pass

    def real_button_release(self, event):
        pass

    def real_motion_notify(self, event):
        pass

    def __init__(self):
        NxpCanvasContainer.__init__(self)
        self._set_drawable(1)
        self._set_visible(1)
        self.set_property('interaction-mask', 0)
        self.connect('draw', self.__class__.real_draw)
        self.connect('configure', self.__class__.real_configure)
        self.connect('size-request', self.__class__.real_size_request)
        self.connect('enter', self.__class__.real_enter)
        self.connect('leave', self.__class__.real_leave)
        self.connect('get_children', self.__class__.real_get_children)
        self.connect('get_child_at_point', self.__class__.real_get_child_at_point)
        self.connect('button-press', self.__class__.real_button_press)
        self.connect('button-release', self.__class__.real_button_release)
        self.connect('motion-notify', self.__class__.real_motion_notify)