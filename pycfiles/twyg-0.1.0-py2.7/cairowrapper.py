# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/twyg/cairowrapper.py
# Compiled at: 2014-03-16 18:05:13
import cairo, colorsys, math

class Color(object):

    def __init__(self, c1, c2, c3, a, mode='rgb'):
        c1 = min(max(0.0, c1), 1.0)
        c2 = min(max(0.0, c2), 1.0)
        c3 = min(max(0.0, c3), 1.0)
        a = min(max(0.0, a), 1.0)
        if mode == 'rgb':
            self.r = c1
            self.g = c2
            self.b = c3
            self.a = a
            self._update_hsv()
        elif mode == 'hsv':
            self.h = c1
            self.s = c2
            self.v = c3
            self.a = a
            self._update_rgb()
        else:
            raise ValueError, 'Invalid color mode: ' + mode

    def __repr__(self):
        return 'Color(r=%.3f, g=%.3f, b=%.3f, a=%.3f)' % (self.r, self.g, self.b, self.a)

    def copy(self):
        return Color(self.r, self.g, self.b, self.a)

    def rgba(self):
        return (
         self.r, self.g, self.b, self.a)

    def darken(self, step=0.1):
        return Color(self.h, self.s, self.v - step, self.a, mode='hsv')

    def lighten(self, step=0.1):
        return Color(self.h, self.s, self.v + step, self.a, mode='hsv')

    def blend(self, clr, factor=0.5):
        r = self.r * (1.0 - factor) + clr.r * factor
        g = self.g * (1.0 - factor) + clr.g * factor
        b = self.b * (1.0 - factor) + clr.b * factor
        a = self.a * (1.0 - factor) + clr.a * factor
        return Color(r, g, b, a)

    def _update_hsv(self):
        self.h, self.s, self.v = colorsys.rgb_to_hsv(self.r, self.g, self.b)

    def _update_rgb(self):
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h, self.s, self.v)


def color(*args):
    n = len(args)
    if n == 1:
        r = g = b = args[0]
        a = 1.0
    elif n == 2:
        r = g = b = args[0]
        a = args[1]
    elif n == 3:
        r, g, b = args
        a = 1.0
    elif n == 4:
        r, g, b, a = args
    else:
        raise ValueError, "Invalid color value: '%s'" % args
    r = min(max(0.0, r), 1.0)
    g = min(max(0.0, g), 1.0)
    b = min(max(0.0, b), 1.0)
    a = min(max(0.0, a), 1.0)
    return Color(r, g, b, a)


class Context(object):

    def __init__(self):
        self._backgroundcolor = None
        self._fillcolor = None
        self._strokecolor = None
        self._strokewidth = 1.0
        self._autoclosepath = True
        self._fontname = 'Helvetica'
        self._fontsize = 12.0
        self._lineheight = 1.5
        self._shadow = False
        self._shadow_dx = 0
        self._shadow_dy = 0
        self._shadow_radius = 3
        self._shadow_color = color(0, 0, 0, 1)
        self._shadow_blur_passes = 2
        self._bitmap_dpi = 150
        return

    def init():
        self.font(self._fontname, self._fontsize)
        self.strokewidth(self._strokewidth)

    def rect(self, x, y, width, height, roundness=0.0, draw=True):
        c = self._ctx
        if roundness == 0:
            c.rectangle(x, y, width, height)
        else:
            curve = min(width * roundness, height * roundness)
            xw = x + width
            yh = y + height
            c.move_to(x, y + curve)
            c.curve_to(x, y, x, y, x + curve, y)
            c.line_to(xw - curve, y)
            c.curve_to(xw, y, xw, y, xw, y + curve)
            c.line_to(xw, yh - curve)
            c.curve_to(xw, yh, xw, yh, xw - curve, yh)
            c.line_to(x + curve, yh)
            c.curve_to(x, yh, x, yh, x, yh - curve)
            c.close_path()
        if draw:
            self._draw()
        else:
            path = c.copy_path()
            c.new_path()
            return path

    def oval(self, x, y, width, height, draw=True):
        c = self._ctx
        if width == 0 or height == 0:
            return
        cx = x + width / 2.0
        cy = y + height / 2.0
        r = width / 2.0
        yscale = float(height) / width
        c.new_path()
        c.save()
        c.scale(1, yscale)
        c.arc(cx, cy / yscale, r, 0, 2 * math.pi)
        c.restore()
        if draw:
            self._draw()
        else:
            path = c.copy_path()
            c.new_path()
            return path

    def line(self, x1, y1, x2, y2, draw=True):
        c = self._ctx
        c.move_to(x1, y1)
        c.line_to(x2, y2)
        if draw:
            self._draw_stroke()
        else:
            path = c.copy_path()
            c.new_path()
            return path

    def arrow(x, y, width, type, draw=True):
        raise NotImplementedError

    def star(x, y, points=20, outer=100, inner=50, draw=True):
        raise NotImplementedError

    def beginpath(self, x, y):
        self._ctx.move_to(x, y)

    def moveto(self, x, y):
        self._ctx.move_to(x, y)

    def lineto(self, x, y):
        self._ctx.line_to(x, y)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        self._ctx.curve_to(x1, y1, x2, y2, x3, y3)

    def findpath(list, curvature=1.0):
        raise NotImplementedError

    def endpath(self, draw=True):
        if self._autoclosepath:
            self._ctx.close_path()
        if draw:
            self._draw()
        else:
            path = self._ctx.copy_path()
            self._ctx.new_path()
            return path

    def drawpath(self, path):
        self._ctx.append_path(path)
        self._draw()

    def beginclip(self, path):
        self._ctx.save()
        self._ctx.new_path()
        self._ctx.append_path(path)
        self._ctx.clip()

    def endclip(self):
        self._ctx.restore()

    def autoclosepath(self, close=True):
        self._autoclosepath = close

    def transform(mode):
        raise NotImplementedError

    def translate(self, x, y):
        self._ctx.translate(x, y)

    def rotate(self, degrees=0.0, radians=0.0):
        if degrees != 0:
            radians = degrees * math.pi / 180
        self._ctx.translate(radians)

    def scale(self, x, y=None):
        if not y:
            y = 1.0
        self._ctx.scale(x, y)

    def skew(x, y=None):
        raise NotImplementedError

    def push(self):
        self._ctx.save()

    def pop(self):
        self._ctx.restore()

    def reset(self):
        self._ctx.identity_matrix()

    def outputmode(self, mode):
        raise NotImplementedError

    def colormode(self, mode):
        pass

    def color(self, *args):
        return color(*args)

    def fill(self, *args):
        self._fillcolor = self._make_color_obj(*args)

    def nofill(self):
        self._fillcolor = None
        return

    def stroke(self, *args):
        self._strokecolor = self._make_color_obj(*args)

    def nostroke(self):
        self._strokecolor = None
        return

    def strokewidth(self, width):
        self._ctx.set_line_width(width)

    def background(self, *args):
        if len(args) == 1 and args[0] == None:
            return
        else:
            col = self._make_color_obj(*args)
            self._backgroundcolor = col
            c = self._ctx
            c.set_source_rgba(*col.rgba())
            c.rectangle(0, 0, self._width, self._height)
            c.fill()
            return

    def font(self, fontname, fontsize=None):
        self._ctx.select_font_face(fontname, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self._fontname = fontname
        if fontsize:
            self.fontsize(fontsize)

    def fontsize(self, fontsize):
        self._ctx.set_font_size(fontsize)
        self._fontsize = fontsize

    def text(self, txt, x, y):
        c = self._ctx
        c.set_source_rgba(*self._fillcolor.rgba())
        c.move_to(x, y)
        c.show_text(txt)

    def textpath(txt, x, y, width=None, height=1000000):
        raise NotImplementedError

    def textwidth(self, txt):
        width, height = self.textmetrics(txt)
        return width

    def textheight(self, txt):
        width, height = self.textmetrics(txt)
        return height

    def textmetrics(self, txt):
        ascent, descent, height, max_x_advance, max_y_advance = self._ctx.font_extents()
        linewidth = self._ctx.text_extents(txt)[4]
        return (linewidth, height + descent)

    def lineheight(self, height=None):
        if height:
            self._lineheight = height
        return self._lineheight

    def align(self, align):
        raise NotImplementedError

    def image(path, x, y, width=None, height=None, alpha=1.0, data=None):
        raise NotImplementedError

    def imagesize(path):
        raise NotImplementedError

    def size(w, h):
        raise NotImplementedError

    def var(name, type, default, min, max):
        raise NotImplementedError

    def random(v1=None, v2=None):
        raise NotImplementedError

    def choice(list):
        raise NotImplementedError

    def grid(cols, rows, colsize=1, rowsize=1):
        raise NotImplementedError

    def files(path):
        raise NotImplementedError

    def autotext(xml):
        raise NotImplementedError

    def rgba_color(self, c):
        return self.color(*c)

    def gradientfill(self, path, clr1, clr2, dx=0.0, dy=0.0, type='linear', spread=1.0):
        c = self._ctx
        c.append_path(path)
        x1, y1, x2, y2 = c.fill_extents()
        pat = cairo.LinearGradient(0, y1, 0, y2)
        pat.add_color_stop_rgba(1, *clr1.rgba())
        pat.add_color_stop_rgba(0, *clr2.rgba())
        if self._shadow:
            self._draw_shadow()
        c.set_source(pat)
        if self._strokecolor:
            c.fill_preserve()
            c.set_source_rgba(*self._strokecolor.rgba())
            c.stroke()
        else:
            c.fill()

    def shadow(self, dx=0.0, dy=0.0, blur=3.0, clr=color(0, 0, 0, 1)):
        self._shadow_dx = dx
        self._shadow_dy = dy
        self._shadow_radius = blur / 2
        self._shadow_color = clr
        self._shadow = True

    def noshadow(self):
        self._shadow = False

    def initsurface(self, w, h, fmt, fname=None, scale=1.0):
        self._width = w
        self._height = h
        w *= scale
        h *= scale
        if fmt == 'pdf':
            self._surface = cairo.PDFSurface(fname, w, h)
        elif fmt == 'svg':
            self._surface = cairo.SVGSurface(fname, w, h)
        elif fmt == 'png':
            w = int(w + 0.5)
            h = int(h + 0.5)
            self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        elif fmt == 'ps':
            self._surface = cairo.PSSurface(fname, w, h)
        else:
            raise ValueError, "Invalid output format: '%s'" % fmt
        self._format = fmt
        self._filename = fname
        self._ctx = cairo.Context(self._surface)
        self._ctx.scale(scale, scale)

    def writesurface(self):
        if self._format == 'png':
            self._surface.write_to_png(self._filename)
        else:
            self._ctx.show_page()

    def _make_color_obj(self, *args):
        if len(args) == 1 and type(args[0]).__name__ == 'Color':
            return args[0]
        else:
            return self.color(*args)

    def _draw_stroke(self):
        c = self._ctx
        if self._strokecolor:
            c.set_source_rgba(*self._strokecolor.rgba())
            c.stroke()

    def _draw(self):
        c = self._ctx
        if self._fillcolor:
            if self._shadow:
                self._draw_shadow()
            c.set_source_rgba(*self._fillcolor.rgba())
            if self._strokecolor:
                c.fill_preserve()
                c.set_source_rgba(*self._strokecolor.rgba())
                c.stroke()
            else:
                c.fill()
        else:
            self._draw_stroke()

    def _draw_shadow(self):
        c = self._ctx
        img, padding = self._render_bitmap_shadow()
        x1, y1, x2, y2 = c.fill_extents()
        dpi_scale = 72.0 / self._bitmap_dpi
        c.save()
        c.set_source_rgba(*self._shadow_color.rgba())
        c.translate(x1 + self._shadow_dx, y1 + self._shadow_dy)
        c.scale(dpi_scale, dpi_scale)
        c.translate(-padding, -padding)
        c.mask_surface(img, 0, 0)
        c.restore()

    def _render_bitmap_shadow(self):
        dpi_scale = self._bitmap_dpi / 72.0
        radius = self._shadow_radius * dpi_scale
        passes = self._shadow_blur_passes
        m = int(radius)
        alpha = radius - m
        scale = 1.0 / (2 * radius + 1)
        padding = int((m + 2) * passes * 1.5 + 0.5)
        c = self._ctx
        x1, y1, x2, y2 = c.fill_extents()
        width = int((x2 - x1) * dpi_scale + padding * 2 + 0.5) + 3
        height = int((y2 - y1) * dpi_scale + padding * 2 + 0.5) + 3
        data = bytearray(width * (height + m + 2) * 4)
        img = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, width, height)
        imgctx = cairo.Context(img)
        offsx = int(-x1 * dpi_scale + padding + 0.5)
        offsy = int(-y1 * dpi_scale + padding + 0.5)
        imgctx.translate(offsx, offsy)
        imgctx.scale(dpi_scale, dpi_scale)
        imgctx.append_path(c.copy_path())
        col = self._shadow_color.copy()
        col.a = 1.0
        imgctx.set_source_rgba(*col.rgba())
        imgctx.fill()
        row = bytearray(width * 4)
        for y in range(0, height):
            for p in range(passes):
                yoffs = y * width * 4 + 3
                sum_ = data[yoffs]
                for x in range(m):
                    sum_ += data[(yoffs - x * 4)] + data[(yoffs + x * 4)]

                sum_ += alpha * data[(yoffs - m * 4)] + data[(yoffs + m * 4)]
                for x in range(width):
                    a = int(sum_ * scale)
                    row[x * 4] = a
                    a = data[(yoffs + (x + m + 1) * 4)]
                    b = data[(yoffs + (x + m + 2) * 4)]
                    sum_ += a + alpha * (b - a)
                    a = data[(yoffs + (x - m) * 4)]
                    b = data[(yoffs + (x - m - 1) * 4)]
                    sum_ -= a + alpha * (b - a)

                data[yoffs:(yoffs + width * 4)] = row

        col = bytearray(height)
        for x in range(width):
            for p in range(passes):
                xoffs = x * 4 + 3
                sum_ = data[xoffs]
                for y in range(m):
                    sum_ += data[(xoffs - y * width * 4)] + data[(xoffs + y * width * 4)]

                sum_ += alpha * data[(xoffs - m * width * 4)] + data[(xoffs + m * width * 4)]
                for y in range(0, height):
                    a = int(sum_ * scale)
                    col[y] = a
                    a = data[(xoffs + (y + m + 1) * width * 4)]
                    b = data[(xoffs + (y + m + 2) * width * 4)]
                    sum_ += a + alpha * (b - a)
                    a = data[(xoffs + (y - m) * width * 4)]
                    b = data[(xoffs + (y - m - 1) * width * 4)]
                    sum_ -= a + alpha * (b - a)

                for y in range(1, height - 1):
                    data[xoffs + y * width * 4] = col[y]

        return (
         img, padding)


context = Context()