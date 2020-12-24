# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/layout/layout.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 8604 bytes
import copy
from .update_threading import UpdateThreading
from ..project import attributes, data_maker, fields
from ..util import deprecated, exception, log
from ..colors import COLORS, conversions, make

class Layout(object):
    __doc__ = '\n    Base Layer class. Use Strip, Matrix, Cube, or Circle instead!\n\n    :param drivers: A list of drivers\n    :param threadedUpdate: If True, updates to this layout are done in a\n        separate thread\n    :param brightness: An initial brightness value from 0 to 255\n    :param maker: A data maker to make color_lists. TODO: Link to what a maker\n        is.\n    :param color_list: If non-Null, the layout uses this color_list instead\n        of creating its own\n\n    :ivar int numLEDs: Total number of pixels held by this layout instance\n    '
    CLONE_ATTRS = ('maker', 'brightness')
    pre_recursion = fields.default_converter

    @classmethod
    def construct(cls, project, **desc):
        """Construct a layout.
        SHOULD BE PRIVATE
        """
        return cls(project.drivers, maker=project.maker, **desc)

    def __init__(self, drivers, threadedUpdate=False, brightness=255, maker=data_maker.MAKER, color_list=None, **kwds):
        (attributes.set_reserved)(self, 'layout', **kwds)
        self.drivers = drivers if isinstance(drivers, list) else [drivers]
        self.maker = maker
        if color_list is None:
            if not hasattr(self, 'numLEDs'):
                self.numLEDs = sum(d.numLEDs for d in self.drivers)
            self._colors = maker.color_list(self.numLEDs)
        else:
            self.numLEDs = len(color_list)
            self._colors = color_list
        pos = 0
        for d in self.drivers:
            d.set_colors(self._colors, pos)
            pos += d.numLEDs

        self.frame_render_time = 0
        self.threading = UpdateThreading(threadedUpdate, self)
        self.brightness = brightness
        self.set_brightness(brightness)
        self.needs_cleanup = True

    def set_pixel_positions(self, pixel_positions):
        """SHOULD BE PRIVATE"""
        for d in self.drivers:
            d.set_pixel_positions(pixel_positions)

    def start(self):
        for d in self.drivers:
            d.start()

    def stop(self):
        self.threading.stop()
        for d in self.drivers:
            d.stop()

    def join(self, timeout=None):
        self.threading.wait()
        for d in self.drivers:
            d.join(timeout)

    def cleanup_drivers(self):
        for d in self.drivers:
            d.cleanup()

    def cleanup(self):
        if self.needs_cleanup:
            self.needs_cleanup = False
            self.all_off()
            exception.report(self.push_to_driver)
            self.threading.wait_for_update()

    def clone(self):
        """
        Return an independent copy of this layout with a completely separate
        color_list and no drivers.
        """
        args = {k:getattr(self, k) for k in self.CLONE_ATTRS}
        args['color_list'] = copy.copy(self.color_list)
        return (self.__class__)([], **args)

    @property
    def shape(self):
        """
        Return a tuple indicating the dimensions of the layout - (x,) for a
        strip, (x, y) for an array, (x, y, z) for a cube, and
        (ring_count, ring_steps) for a circle.
        """
        raise NotImplementedError

    @property
    def dimensions(self):
        deprecated.deprecated('Layout.dimensions')
        return self.shape

    @property
    def color_list(self):
        return self._colors

    @color_list.setter
    def color_list(self, color_list):
        self.set_color_list(color_list)

    def set_color_list(self, color_list, offset=0):
        """
        Set the internal colors starting at an optional offset.

        If `color_list` is a list or other 1-dimensional array, it is reshaped
        into an N x 3 list.

        If `color_list` too long it is truncated; if it is too short then only
        the initial colors are set.
        """
        if not len(color_list):
            return
        color_list = make.colors(color_list)
        size = len(self._colors) - offset
        if len(color_list) > size:
            color_list = color_list[:size]
        self._colors[offset:offset + len(color_list)] = color_list

    def _get_base(self, pixel):
        if pixel >= 0:
            if pixel < self.numLEDs:
                return self._colors[pixel]
        return COLORS.Black

    def _set_base(self, pixel, color):
        if pixel >= 0:
            if pixel < self.numLEDs:
                if isinstance(color, str):
                    color = COLORS[color]
                else:
                    color = tuple(color)
                self.color_list[pixel] = color

    def get_pixel_positions(self):
        result = []
        for x in range(len(self.numLEDs)):
            result.append([x, 0, 0])

        return result

    def push_to_driver(self):
        """
        Push the current pixel state to the driver
        Do not call this method from user code!
        """
        self.threading.push_to_driver()

    if deprecated.allowed():

        def update(self):
            """
            DEPRECATED: Use :py:func:`push_to_driver` instead
            Do not call this method from user code!
            """
            deprecated.deprecated('Layout.update')
            return self.push_to_driver()

    def set_brightness(self, brightness):
        self.brightness = brightness
        for d in self.drivers:
            d.set_brightness(brightness)

    def setRGB(self, pixel, r, g, b):
        """Set single pixel using individual RGB values instead of tuple"""
        self._set_base(pixel, (r, g, b))

    def setHSV(self, pixel, hsv):
        """Set single pixel to HSV tuple"""
        color = conversions.hsv2rgb(hsv)
        self._set_base(pixel, color)

    def setOff(self, pixel):
        """Set single pixel off"""
        self._set_base(pixel, (0, 0, 0))

    def all_off(self):
        """Set all pixels off"""
        self._colors[:] = [
         (0, 0, 0)] * self.numLEDs

    def fill(self, color, start=0, end=-1):
        """Fill the entire strip with RGB color tuple"""
        start = max(start, 0)
        if end < 0 or end >= self.numLEDs:
            end = self.numLEDs - 1
        for led in range(start, end + 1):
            self._set_base(led, color)

    def fillRGB(self, r, g, b, start=0, end=-1):
        """Fill entire strip by giving individual RGB values instead of tuple"""
        self.fill((r, g, b), start, end)

    def fillHSV(self, hsv, start=0, end=-1):
        """Fill the entire strip with HSV color tuple"""
        self.fill(conversions.hsv2rgb(hsv), start, end)


class MultiLayout(Layout):
    CLONE_ATTRS = Layout.CLONE_ATTRS + ('gen_coord_map', 'coord_map')

    def __init__(self, *args, gen_coord_map=None, coord_map=None, **kwds):
        (super().__init__)(*args, **kwds)
        self.gen_coord_map = gen_coord_map
        if gen_coord_map:
            if coord_map:
                log.warning('Cannot set both coord_map and gen_coord_map')
            else:
                if isinstance(gen_coord_map, dict):
                    coord_map = (self.gen_multi)(**gen_coord_map)
                else:
                    coord_map = self.gen_multi(gen_coord_map)
        self.coord_map = coord_map

    def gen_multi(self, *args, **kwds):
        raise NotImplementedError

    def set_colors(self, buf):
        """
        DEPRECATED: use self.color_list

        Use with extreme caution!
        Directly sets the internal buffer and bypasses all brightness and
        rotation control buf must also be in the exact format required by the
        display type.
        """
        deprecated.deprecated('layout.set_colors')
        if len(self._colors) != len(buf):
            raise IOError('Data buffer size incorrect! Expected: {} bytes / Received: {} bytes'.format(len(self._colors), len(buf)))
        self._colors[:] = buf

    def setBuffer(self, buf):
        deprecated.deprecated('layout.setBuffer')
        self.color_list = buf