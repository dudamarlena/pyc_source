# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/broken.py
# Compiled at: 2017-07-28 03:18:39
# Size of source mod 2**32: 4006 bytes
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def dfx(_ax, x, d):
    x0 = _ax.get_xlim()[0]
    x1 = _ax.get_xlim()[1]
    xs = x1 - x0
    o = (x - x0) / (x1 - x0)
    return (o - d, o + d)


def dfy(_ax, y, d):
    y0 = _ax.get_ylim()[0]
    y1 = _ax.get_ylim()[1]
    ys = y1 - y0
    o = (y - y0) / (y1 - y0)
    return (o - d, o + d)


def break_the_ax(f, _ax, break_at=[], scale=[1, 1]):
    if type(break_at) is int or type(break_at) is float:
        break0 = break_at
        break1 = break_at
    else:
        if type(break_at) is list:
            if len(break_at) == 0:
                return
            if len(break_at) == 1:
                break0 = break_at[0]
                break1 = break_at[0]
            else:
                break0 = break_at[0]
                break1 = break_at[1]
        else:
            return
        start = _ax.get_ylim()[0]
        end = _ax.get_ylim()[1]
        ratio0 = int((break0 - start) / scale[0])
        ratio1 = int((end - break1) / scale[1])
        perc = 100 * (ratio1 / ratio0)
        ax_old = _ax
        divider = make_axes_locatable(ax_old)
        print(str(perc) + '%')
        ax_new = divider.new_vertical(size=(str(perc) + '%'), pad=0.1)
        f.add_axes(ax_new)
        ax_new.spines['right'].set_visible(ax_old.spines['right'].get_visible())
        ax_new.spines['top'].set_visible(ax_old.spines['top'].get_visible())
        ax_old.set_ylim(start, break0)
        ax_old.spines['top'].set_visible(False)
        ax_new.set_ylim(break1, end)
        ax_new.tick_params(bottom='off', labelbottom='off')
        ax_new.spines['bottom'].set_visible(False)
        for each_line in ax_old.get_lines():
            x, y = each_line.get_data()
            ax_new.plot(x, y)
            if y[0] <= break0:
                curax = 0
            if y[0] >= break1:
                curax = 1
            pts = []
            for i, allx in enumerate(x[1:]):
                if y[i] <= break0:
                    if curax == 1:
                        pts.append([x[i], y[i]])
                    curax = 0
                if y[i] >= break1:
                    if curax == 0:
                        pts.append([x[(i - 1)], y[(i - 1)]])
                    curax = 1

        d0 = 0.01 * scale[0]
        d1 = 0.01 * scale[1] * (ratio1 / ratio0)
        dx = 0.01
        d = d1
        kwargs = dict(transform=(ax_new.transAxes), color='k', clip_on=False)
        (ax_new.plot)((-dx, +dx), (-d, +d), **kwargs)
        if ax_old.spines['right'].get_visible():
            (ax_new.plot)((1 - dx, 1 + dx), (-d, +d), **kwargs)
        d = d0
        kwargs.update(transform=(ax_old.transAxes))
        (ax_old.plot)((-dx, +dx), (1 - d, 1 + d), **kwargs)
        if ax_old.spines['right'].get_visible():
            (ax_old.plot)((1 - dx, 1 + dx), (1 - d, 1 + d), **kwargs)
    for ps in pts:
        ax_old.plot((dfx(ax_old, ps[0], dx)), (dfy(ax_old, break0, d0)), 'k', clip_on=False, transform=(ax_old.transAxes))
        ax_new.plot((dfx(ax_new, ps[0], dx)), (dfy(ax_new, break1, d1)), 'k', clip_on=False, transform=(ax_new.transAxes))

    return [
     ax_old, ax_new]


np.random.seed(42)
N = 100
x = np.linspace(0, 10, num=N)
A = 10
listA = []
even = np.arange(0, 10, 2).astype(int)
for i in range(A):
    if i in even:
        listA.append(np.random.uniform(0, 1, int(N / A)))
    else:
        listA.append(np.random.uniform(20, 25, int(N / A)))

y = np.concatenate(listA)
y2 = np.random.uniform(0, 1, N)
f, axes = plt.subplots(nrows=2)
axes[0].plot(x, y)
axes[0].spines['right'].set_visible(False)
axes[0].spines['top'].set_visible(False)
axes[0].set_ylim([0, 25])
axes[0] = break_the_ax(f, (axes[0]), break_at=6, scale=[1, 5])
axes[0][1].set_yticks([10, 15, 20, 25])
axes[0][0].set_yticks([0, 1, 2, 3, 4, 5])
axes[1].plot(x, y2)
plt.show()