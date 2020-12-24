# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\lazyEEG\graph\draw.py
# Compiled at: 2017-11-26 19:59:51
# Size of source mod 2**32: 12426 bytes
from ..default import *
import math
from pylab import get_cmap
from matplotlib.patches import Rectangle

def cmap_discretize(cmap, N):
    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1.0, N), (0.0, 0.0, 0.0, 0.0)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1.0, N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[(i - 1, ki)], colors_rgba[(i, ki)]) for i in range(N + 1)]

    return matplotlib.colors.LinearSegmentedColormap(cmap.name + '_%d' % N, cdict, 1024)


def line(ax, title, batch_data, note, color, err_style='ci_band'):
    if type(batch_data.columns) == pd.TimedeltaIndex:
        batch_data.columns = [
         [
          'data'] * len(batch_data.columns), batch_data.columns]
    else:
        try:
            tps = (batch_data['data'].columns / np.timedelta64(1, 'ms')).astype(int)
        except:
            tps = batch_data['data'].columns

        batch_data.columns.names = ['data', 'time']
        batch_data = batch_data.stack('time')
        if 'subject' not in batch_data.index.names:
            batch_data.reset_index(level=['condition', 'time'], inplace=True)
            sns.tsplot(time='time', value='data', condition='condition', data=batch_data,
              ax=ax,
              err_style=None,
              color=color)
        else:
            try:
                batch_data.reset_index(level=['subject', 'channel', 'condition', 'time'], inplace=True)
            except:
                batch_data.index = pd.MultiIndex.from_tuples([('1', old[0], old[1], old[2]) for old in batch_data.index])
                batch_data.index = batch_data.index.set_names(['subject', 'channel', 'condition', 'time'])
                batch_data.reset_index(level=['subject', 'channel', 'condition', 'time'], inplace=True)

            if len(batch_data['channel'].unique()) > 1:
                if len(batch_data['condition'].unique()) > 1:
                    raise Exception('Allowed only one condition!')
                sns.tsplot(time='time', value='data', unit='subject', condition='channel', data=batch_data,
                  ax=ax,
                  err_style=None,
                  legend=False,
                  color=color)
            else:
                sns.tsplot(time='time', value='data', unit='subject', condition='condition', data=batch_data,
                  ax=ax,
                  err_style=err_style,
                  color=color)
        ax.set_title(title)
        ax.set_xlabel(note[0])
        ax.set_ylabel(note[1])
        if 'Spectrum' not in title:
            if ax.get_xticks() != []:
                if tps[(-1)] - tps[0] < 201:
                    step_num = 11
                    xticks = np.linspace(ax.get_xticks()[0], ax.get_xticks()[(-1)], step_num)
                    xticklabels = np.round(np.linspace(tps[0], tps[(-1)], step_num)).astype(int)
                else:
                    xticklabels = [tp for ind, tp in enumerate(tps) if tp % 50 == 0]
                    xticks = np.linspace(ax.get_xticks()[0], ax.get_xticks()[(-1)] * (xticklabels[(-1)] / tps[(-1)]), len(xticklabels))
                ax.set_xticks(xticks)
                ax.set_xticklabels(xticklabels)
        if note[2] != []:
            ax.set_ylim(note[2])


def heatmap(ax, title, stat_data, note, color, cbar_ax=None, grid=True):
    if len(note) > 3:
        if note[3] != '':
            sns.heatmap(stat_data, ax=ax, cmap=(cmap_discretize(color, len(note[3]))), cbar_ax=cbar_ax)
        else:
            sns.heatmap(stat_data, ax=ax, cbar_ax=cbar_ax)
        names = stat_data.index
        if type(stat_data.columns) == pd.core.indexes.multi.MultiIndex:
            stat_data.columns = stat_data['data'].columns
        try:
            tps = (stat_data.columns / np.timedelta64(1, 'ms')).astype(int)
        except:
            tps = stat_data.columns

        if tps[(-1)] - tps[0] < 201:
            step_num = 11
            xticks = np.linspace(0, len(tps), step_num)
            xticklabels = np.linspace((tps[0]), (tps[(-1)]), step_num, dtype=int)
        else:
            xticks = [ind for ind, tp in enumerate(tps) if tp % 50 == 0]
            xticklabels = [tp for ind, tp in enumerate(tps) if tp % 50 == 0]
        ax.set_title(title)
        ax.set_xlabel(note[0])
        ax.set_ylabel(note[1])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, fontname='Consolas', size='large')
        ax.set_yticklabels((ax.get_yticklabels()), rotation=0, fontname='Consolas')
        if note[2] != []:
            cbar_ax.set_title(note[2])
    else:
        if len(note) > 3:
            cbar_ax.set_yticklabels(note[3])
        if grid:
            for i in xticks:
                ax.axvline(i, c='w', linewidth=1, linestyle='dotted')

            for i in range(len(names)):
                ax.axhline(i, c='w', linewidth=1)


def significant(ax, result, win, sig_limit=0.05):
    win = int(win[:-2])
    xmin, xmax, ymin, ymax = ax.axis()
    sig_plot_list = np.zeros(xmax - xmin)
    for limit, alpha in zip([sig_limit, 0.1, 0.05, 0.01, 0.001], [0.1, 0.2, 0.3, 0.4, 0.5]):
        for tp, pv in result.items():
            tp = (tp / np.timedelta64(1, 'ms')).astype(int)
            if pv and pv < limit <= sig_limit:
                sig_plot_list[tp:tp + win] = alpha

    for tp, alpha in enumerate(sig_plot_list):
        if alpha > 0:
            ax.axvspan(tp, (tp + 1), facecolor='0', alpha=alpha, edgecolor='none')


def channel_locs(topo):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for ch, (x, y) in topo.items():
        ax.annotate(ch, (x, y))
        ax.scatter(x, y, c='b', s=1)

    ax.axis('off')


def topograph_circle(ax, data, topo, stat_data=None, sig_limit=0.05, zlim=None):
    N = 50
    scale = 3
    coord = np.array([[topo[ch][0] * scale, topo[ch][1] * scale, amp] for ch, amp in data.items()])
    bottom, top = coord[:, 0].min() - 0.1, coord[:, 0].max() + 0.1
    left, right = bottom, top
    coord = np.concatenate([coord, [[left, bottom, 0], [right, bottom, 0], [left, top, 0], [right, top, 0]]])
    x, y, z = coord[:, 0] - left, coord[:, 1] - bottom, coord[:, 2]
    xi = np.linspace(0, right - left, N)
    yi = np.linspace(0, top - bottom, N)
    zi = scipy.interpolate.griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
    zi[zi < zlim[0]] = zlim[0]
    zi[zi > zlim[1]] = zlim[1]
    xy_center = [
     (right - left) / 2, (top - bottom) / 2]
    radius = (coord[:, 1].max() - coord[:, 1].min()) / 2 + 0.05
    dr = xi[1] - xi[0]
    for i in range(N):
        for j in range(N):
            r = np.sqrt((xi[i] - xy_center[0]) ** 2 + (yi[j] - xy_center[1]) ** 2)
            if r - dr / 2 > radius:
                zi[(j, i)] = 'nan'

    circle = matplotlib.patches.Circle(xy=xy_center, radius=(radius - 0.5), edgecolor='k', facecolor='none')
    ax.add_patch(circle)
    points = [
     (
      xy_center[0] - (radius - 0.5) / 5, xy_center[1] + radius - 0.5), (xy_center[0], xy_center[1] + radius), (xy_center[0] + (radius - 0.5) / 5, xy_center[1] + radius - 0.5)]
    line = plt.Polygon(points, closed=None, fill=None, edgecolor='k', facecolor='none')
    ax.add_patch(line)
    if zlim:
        CS = ax.contourf(xi, yi, zi, 60, cmap=(plt.cm.jet), zorder=1, levels=(np.linspace(zlim[0], zlim[1], 40)))
    else:
        CS = ax.contourf(xi, yi, zi, 60, cmap=(plt.cm.jet), zorder=1)
    ax.contour(xi, yi, zi, colors='grey', alpha=0.5, zorder=2, linestyles='solid')
    ax.scatter((x[:-4]), (y[:-4]), marker='o', c='b', alpha=0.5, s=2, zorder=3)
    if type(stat_data) is pd.Series:
        for ch, pv in stat_data.items():
            if pv < sig_limit:
                xv = topo[ch][0] * scale - left
                yv = topo[ch][1] * scale - bottom
                ax.scatter(xv, yv, c='w', s=25, alpha=1, zorder=3, linewidths=0.5, edgecolors='b')

    ax.axis('off')


def topograph_square(ax, data, topo, stat_data=None, sig_limit=0.05, zlim=None):
    N = 30
    scale = 3
    coord = np.array([[topo[ch][0] * scale, topo[ch][1] * scale, amp] for ch, amp in data.items()])
    bottom, top = coord[:, 0].min(), coord[:, 0].max()
    left, right = bottom, top
    coord = np.concatenate([coord, [[left, bottom, 0], [right, bottom, 0], [left, top, 0], [right, top, 0]]])
    x, y, z = coord[:, 0] - left, coord[:, 1] - bottom, coord[:, 2]
    xi = np.linspace(0, right - left, N)
    yi = np.linspace(0, top - bottom, N)
    zi = scipy.interpolate.griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
    print(zi)
    if zlim:
        CS = ax.contourf(xi, yi, zi, 60, cmap=(plt.cm.jet), zorder=1, levels=(np.linspace(zlim[0], zlim[1], 40)))
    else:
        CS = ax.contourf(xi, yi, zi, 60, cmap=(plt.cm.jet), zorder=1)
    ax.contour(xi, yi, zi, colors='grey', alpha=0.5, zorder=2, linestyles='solid')
    ax.scatter(x, y, marker='o', c='b', s=5, zorder=3)
    if stat_data != None:
        for xv, yv, zv in zip(x, y, pv):
            ax.scatter(xv, yv, c='w', s=zv, zorder=3, linewidths=1)

    ax.axis('off')