# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\niplot.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 3554 bytes
from pylab import axis, draw, close, gcf, gca

def zoom(event):
    ax = gca()
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    base_scale = 1.1
    xdata = event.xdata
    ydata = event.ydata
    if xdata != None:
        if ydata != None:
            if event.button == 'up':
                scale_factor = 1 / base_scale
            else:
                if event.button == 'down':
                    scale_factor = base_scale
                else:
                    scale_factor = 1
                    print(event.button)
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
            ax.figure.canvas.draw()
    return zoom


def on_key_press(event):
    if event.key == '+':
        a = axis()
        w = a[1] - a[0]
        axis([a[0] + w * 0.2, a[1] - w * 0.2, a[2], a[3]])
        draw()
    if event.key in ('-', "'"):
        a = axis()
        w = a[1] - a[0]
        axis([a[0] - w / 3.0, a[1] + w / 3.0, a[2], a[3]])
        draw()
    if event.key in ('.', 'right'):
        a = axis()
        w = a[1] - a[0]
        axis([a[0] + w * 0.2, a[1] + w * 0.2, a[2], a[3]])
        draw()
    if event.key in (',', 'left'):
        a = axis()
        w = a[1] - a[0]
        axis([a[0] - w * 0.2, a[1] - w * 0.2, a[2], a[3]])
        draw()
    if event.key == 'up':
        a = axis()
        w = a[3] - a[2]
        axis([a[0], a[1], a[2] + w * 0.2, a[3] + w * 0.2])
        draw()
    if event.key == 'down':
        a = axis()
        w = a[3] - a[2]
        axis([a[0], a[1], a[2] - w * 0.2, a[3] - w * 0.2])
        draw()
    if event.key == 'q':
        close()


def on_key_release(event):
    pass


def niplot():
    """
    This script extends the native matplolib keyboard bindings.
    This script allows to use the `up`, `down`, `left`, and `right` keys
    to move the visualization window. Zooming can be performed using the `+`
    and `-` keys. Finally, the scroll wheel can be used to zoom under cursor.

    Returns
    -------

    """
    fig = gcf()
    cid = fig.canvas.mpl_connect('key_press_event', on_key_press)
    cid = fig.canvas.mpl_connect('key_release_event', on_key_release)
    cid = fig.canvas.mpl_connect('scroll_event', zoom)