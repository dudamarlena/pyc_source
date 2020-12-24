# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/gsnowflake.py
# Compiled at: 2014-07-01 12:56:15
try:
    import svgwrite
except ImportError:
    import sys, os
    parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parentdir)
    try:
        import svgwrite
    except ImportError:
        raise Exception("Please install module 'svgwrite'")

import math, time
try:
    import gterm
except ImportError:
    import graphterm.bin.gterm as gterm

def write_svg(drawing, overwrite=False):
    """Display SVG drawing as block image
    """
    blob_url = gterm.create_blob(drawing.tostring(), content_type='image/svg+xml')
    gterm.display_blockimg(blob_url, overwrite=overwrite)


def koch_snowflake(name):

    def tf(x0, y0, x1, y1, x2, y2):
        a = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        b = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        c = math.sqrt((x0 - x2) ** 2 + (y0 - y2) ** 2)
        if a < stop_val or b < stop_val or c < stop_val:
            return
        x3 = (x0 + x1) / 2
        y3 = (y0 + y1) / 2
        x4 = (x1 + x2) / 2
        y4 = (y1 + y2) / 2
        x5 = (x2 + x0) / 2
        y5 = (y2 + y0) / 2
        points = [(x3, y3), (x4, y4), (x5, y5)]
        snowflake.add(dwg.polygon(points))
        tf(x0, y0, x3, y3, x5, y5)
        tf(x3, y3, x1, y1, x4, y4)
        tf(x5, y5, x4, y4, x2, y2)

    def sf(ax, ay, bx, by):
        f = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
        if f < 1.0:
            return
        f3 = f / 3
        cs = (bx - ax) / f
        sn = (by - ay) / f
        cx = ax + cs * f3
        cy = ay + sn * f3
        h = f3 * math.sqrt(3) / 2
        dx = (ax + bx) / 2 + sn * h
        dy = (ay + by) / 2 - cs * h
        ex = bx - cs * f3
        ey = by - sn * f3
        tf(cx, cy, dx, dy, ex, ey)
        sf(ax, ay, cx, cy)
        sf(cx, cy, dx, dy)
        sf(dx, dy, ex, ey)
        sf(ex, ey, bx, by)

    stop_val = 8.0
    imgx = 512
    imgy = 512
    overwrite = False
    for stop_val in (256.0, 128.0, 64.0, 32.0, 16.0, 8.0):
        dwg = svgwrite.Drawing(name, (imgx, imgy), profile='tiny', debug=True)
        snowflake = dwg.g(stroke='blue', fill='rgb(90%,90%,100%)', stroke_width=0.25)
        dwg.defs.add(snowflake)
        mx2 = imgx / 2
        my2 = imgy / 2
        r = my2
        a = 2 * math.pi / 3
        for k in range(3):
            x0 = mx2 + r * math.cos(a * k)
            y0 = my2 + r * math.sin(a * k)
            x1 = mx2 + r * math.cos(a * (k + 1))
            y1 = my2 + r * math.sin(a * (k + 1))
            sf(x0, y0, x1, y1)

        x2 = mx2 + r * math.cos(a)
        y2 = my2 + r * math.sin(a)
        tf(x0, y0, x1, y1, x2, y2)
        use_snowflake = dwg.use(snowflake)
        dwg.add(use_snowflake)
        write_svg(dwg, overwrite=overwrite)
        overwrite = True
        time.sleep(0.5)


if __name__ == '__main__':
    koch_snowflake('koch_snowflake.svg')