# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\Waffle.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 11112 bytes
from tkinter import Canvas, BOTH, Frame
from . import utilities as utils
from .base import Widget
from .event import EventManager

class Waffle(Widget):

    def __init__(self, master, height=3, width=3, dim=20, pad=5, color='white', dotty=False, grid=None, align=None, command=None, visible=True, enabled=None, bg=None):
        description = '[Waffle] object ({}x{})'.format(height, width)
        tk = Frame(master.tk)
        self._pixel_size = dim
        self._pad = pad
        self._color = utils.convert_color(color)
        self._dotty = dotty
        self._waffle_pixels = {}
        self._canvas = None
        super(Waffle, self).__init__(master, tk, description, grid, align, visible, enabled, width, height)
        if bg is not None:
            self.bg = bg
        self.update_command(command)
        self._events = EventManager(self, self._canvas)
        self.events.set_event('<Waffle.ButtonPress-1>', '<ButtonPress-1>', self._clicked_on)

    def _create_waffle(self):
        if self._height == 'fill' or self._width == 'fill':
            utils.raise_error("{}\nCannot use 'fill' for width and height.".format(self.description))
        self._create_canvas()
        self._size_waffle()
        self._draw_waffle()

    def _create_canvas(self):
        if self._canvas:
            self._canvas.delete('all')
            self._canvas.destroy()
        self._c_height = self._height * (self._pixel_size + self._pad) + self._pad * 2
        self._c_width = self._width * (self._pixel_size + self._pad) + self._pad * 2
        self._canvas = Canvas((self.tk), height=(self._c_height), width=(self._c_width), bd=0, highlightthickness=0)
        self._canvas.pack(fill=BOTH, expand=1)
        self.events.rebind_events(self._canvas)
        self._canvas.create_rectangle(0, 0, (self._c_width), (self._c_height), fill=(self.bg), outline=(self.bg))

    def _size_waffle(self):
        new_waffle_pixels = {}
        currx = self._pad
        curry = self._pad
        for x in range(self._width):
            for y in range(self._height):
                if (
                 x, y) in self._waffle_pixels.keys():
                    old_pixel = self._waffle_pixels[(x, y)]
                    new_waffle_pixels[(x, y)] = WafflePixel(x, y, self._canvas, currx, curry, self._pixel_size, old_pixel.dotty, old_pixel.color)
                else:
                    new_waffle_pixels[(x, y)] = WafflePixel(x, y, self._canvas, currx, curry, self._pixel_size, self._dotty, self._color)
                curry += self._pixel_size + self._pad

            currx += self._pixel_size + self._pad
            curry = self._pad

        self._waffle_pixels = new_waffle_pixels

    def _draw_waffle(self):
        currx = self._pad
        curry = self._pad
        for x in range(self._width):
            for y in range(self._height):
                cell = self._waffle_pixels[(x, y)]
                cell.draw()
                curry += self._pixel_size + self._pad

            currx += self._pixel_size + self._pad
            curry = self._pad

    def set_all(self, color):
        for x in range(self._width):
            for y in range(self._height):
                self._waffle_pixels[(x, y)].color = color

    def set_pixel(self, x, y, color):
        if self.pixel(x, y):
            self._waffle_pixels[(x, y)].color = color

    def get_pixel(self, x, y):
        if self.pixel(x, y):
            return self._waffle_pixels[(x, y)].color

    def get_all(self):
        all_pixels = []
        for y in range(self._height):
            row = []
            for x in range(self._width):
                row.append(self._waffle_pixels[(x, y)].color)

            all_pixels.append(row)

        return all_pixels

    def _clicked_on(self, e):
        if self._enabled:
            canvas = e.tk_event.widget
            x = canvas.canvasx(e.tk_event.x)
            y = canvas.canvasy(e.tk_event.y)
            pixel_x = int(x / (self._pixel_size + self._pad))
            pixel_y = int(y / (self._pixel_size + self._pad))
            if self._command:
                args_expected = utils.no_args_expected(self._command)
                if args_expected == 0:
                    self._command()
                else:
                    if args_expected == 2:
                        self._command(pixel_x, pixel_y)
                    else:
                        utils.error_format('Waffle command function must accept either 0 or 2 arguments.\nThe current command has {} arguments.'.format(args_expected))

    def update_command(self, command):
        if command is None:
            self._command = lambda : None
        else:
            self._command = command

    def pixel(self, x, y):
        if (
         x, y) in self._waffle_pixels.keys():
            _pixel = self._waffle_pixels[(x, y)]
        else:
            utils.error_format('Pixel x={} y={} is off the edge of the waffle'.format(x, y))
            _pixel = None
        return _pixel

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    def disable(self):
        """Disable the widget."""
        self._enabled = False

    def enable(self):
        """Enable the widget."""
        self._enabled = True

    def resize(self, width, height):
        if self._width != width or self._height != height:
            self._width = width
            self._height = height
            self._create_waffle()

    @property
    def pixel_size(self):
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, value):
        if self._pixel_size != value:
            self._pixel_size = value
            self._create_waffle()

    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, value):
        if self._pad != value:
            self._pad = value
            self._create_waffle()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        old_color = self._color
        self._color = utils.convert_color(value)
        for x in range(self._width):
            for y in range(self._height):
                if self._waffle_pixels[(x, y)].color == old_color:
                    self._waffle_pixels[(x, y)].color = self._color

    @property
    def dotty(self):
        return self._dotty

    @dotty.setter
    def dotty(self, value):
        self._dotty = value
        for x in range(self._width):
            for y in range(self._height):
                self._waffle_pixels[(x, y)].dotty = self._dotty

    @property
    def bg(self):
        return super(Waffle, self.__class__).bg.fget(self)

    @bg.setter
    def bg(self, value):
        if self.bg != value:
            value = utils.convert_color(value)
            super(Waffle, self.__class__).bg.fset(self, value)
            self._create_waffle()

    def reset(self):
        self.set_all(self._color)
        self.dotty = self._dotty

    def __getitem__(self, index):
        return self._waffle_pixels[index]


class WafflePixel:

    def __init__(self, x, y, canvas, canvas_x, canvas_y, size, dotty, color):
        self._x = x
        self._y = y
        self._canvas = canvas
        self._canvas_x = canvas_x
        self._canvas_y = canvas_y
        self._size = size
        self._dotty = dotty
        self._color = color
        self._drawn_object = None

    def draw(self):
        if self._drawn_object:
            self._canvas.delete(self._drawn_object)
        elif self._dotty == False:
            self._drawn_object = self._canvas.create_rectangle((self._canvas_x),
              (self._canvas_y), (self._canvas_x + self._size),
              (self._canvas_y + self._size), fill=(self._color))
        else:
            self._drawn_object = self._canvas.create_oval((self._canvas_x),
              (self._canvas_y), (self._canvas_x + self._size),
              (self._canvas_y + self._size), fill=(self._color))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def canvas_x(self):
        return self._canvas_x

    @property
    def canvas_y(self):
        return self._canvas_x

    @property
    def size(self):
        return self._size

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = utils.convert_color(value)
        self._canvas.itemconfig((self._drawn_object), fill=(self._color))

    @property
    def dotty(self):
        return self._dotty

    @dotty.setter
    def dotty(self, value):
        self._dotty = value
        self.draw()