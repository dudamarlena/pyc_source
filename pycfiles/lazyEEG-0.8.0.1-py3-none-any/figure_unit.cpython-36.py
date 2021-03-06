# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG\graph\figure_unit.py
# Compiled at: 2017-12-25 13:40:57
# Size of source mod 2**32: 10887 bytes
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


def significant(ax, pv_data, win, sig_limit=0.05):
    win = int(win[:-2])
    xmin, xmax, ymin, ymax = ax.axis()
    sig_plot_list = np.zeros(int(xmax - xmin))
    for limit, alpha in zip([sig_limit, 0.1, 0.05, 0.01, 0.001], [0.1, 0.2, 0.3, 0.4, 0.5]):
        for tp, pv_df in pv_data.items():
            pv = pv_df.values[0]
            if pv and pv < limit <= sig_limit:
                sig_plot_list[int(tp) - win // 2:int(tp) + win // 2] = alpha

    for tp, alpha in enumerate(sig_plot_list):
        if alpha > 0:
            ax.axvspan(tp, (tp + 1), facecolor='0', alpha=alpha, edgecolor='none')


def plot_waveform(ax, data, plot_params):
    flat_data = data.stack('time')
    flat_data.reset_index(level=['condition_group', 'channel_group', 'subject', 'time'], inplace=True)
    flat_data['condition_group'] = flat_data['condition_group'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    flat_data['channel_group'] = flat_data['channel_group'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    if 'title' in plot_params:
        ax.set_title(plot_params['title'])
    else:
        ax.set_title(data.name)
    if len(flat_data['channel_group'].unique()) > 1:
        group = 'channel_group'
        legend = False
    else:
        group = 'condition_group'
        legend = True
    sns.tsplot(time='time', value=0, unit='subject', condition=group, data=flat_data,
      ax=ax,
      err_style=(plot_params['err_style']),
      legend=legend,
      color=(plot_params['color']))
    if 'x_title' in plot_params:
        ax.set_xlabel(plot_params['x_title'])
    if 'y_title' in plot_params:
        ax.set_ylabel(plot_params['y_title'])
    if 'ylim' in plot_params:
        ax.set_ylim(plot_params['ylim'])


def plot_spectrum(ax, data, plot_params):
    flat_data = data.stack('frequency')
    flat_data.reset_index(level=['condition_group', 'channel_group', 'subject', 'frequency'], inplace=True)
    flat_data['condition_group'] = flat_data['condition_group'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    flat_data['channel_group'] = flat_data['channel_group'].apply(lambda x: ' '.join(x.split(' ')[1:]))
    if 'title' in plot_params:
        ax.set_title(plot_params['title'])
    else:
        ax.set_title(data.name)
    if len(flat_data['channel_group'].unique()) > 1:
        group = 'channel_group'
        legend = False
    else:
        group = 'condition_group'
        legend = True
    sns.tsplot(time='frequency', value=0, unit='subject', condition=group, data=flat_data,
      ax=ax,
      err_style=(plot_params['err_style']),
      legend=legend,
      color=(plot_params['color']))
    if 'x_title' in plot_params:
        ax.set_xlabel(plot_params['x_title'])
    if 'y_title' in plot_params:
        ax.set_ylabel(plot_params['y_title'])
    if 'ylim' in plot_params:
        ax.set_ylim(plot_params['ylim'])


def plot_heatmap(ax, data, plot_params):
    cbar_ax = ax.get_figure().add_axes([
     0.95, 0.4, 0.01, 0.2])
    if data.index.name:
        if '_group' in data.index.name:
            data.index = [' '.join(i.split(' ')[1:]) for i in data.index]
    else:
        if 'cbar_values' in plot_params:
            sns.heatmap(data, ax=ax, cmap=(cmap_discretize(plot_params['color'], len(plot_params['cbar_values']))), cbar_ax=cbar_ax)
            cb_yticks = cbar_ax.get_yticks()
            cbar_ax.yaxis.set_ticks([(cb_yticks[i] + cb_yticks[(i + 1)]) / 2 for i in range(len(plot_params['cbar_values']))])
            cbar_ax.set_yticklabels(plot_params['cbar_values'])
        else:
            sns.heatmap(data, ax=ax, cbar_ax=cbar_ax, cmap=(plot_params['color']))
        if type(data.columns) is pd.MultiIndex:
            xticklabels = data[0].columns
        else:
            xticklabels = data.columns
    ax.set_title(data.name)
    if 'x_title' in plot_params:
        ax.set_xlabel(plot_params['x_title'])
    else:
        if 'y_title' in plot_params:
            ax.set_ylabel(plot_params['y_title'])
        else:
            if len(xticklabels) < 40:
                ax.set_aspect(1)
            else:
                ax.set_aspect(len(xticklabels) / 40)
        if len(ax.get_xticklabels()) >= 40:
            step_num = 11
            xticks = ax.get_xticks()
            xticks = np.linspace(xticks[0], xticks[(-1)], step_num)
            xticklabels = np.linspace((xticklabels[0]), (xticklabels[(-1)]), step_num, dtype=int)
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticklabels, rotation=45, fontname='Consolas', size='large')
        else:
            ax.set_xticklabels((ax.get_xticklabels()), rotation=45, fontname='Consolas', size='large')
    ax.set_yticklabels((ax.get_yticklabels()), rotation=0, fontname='Consolas')
    cbar_ax.set_title(plot_params['cbar_title'])
    if 'grid' in plot_params:
        if plot_params['grid']:
            for i in ax.get_xticks():
                ax.axvline(i, c='w', linewidth=1, linestyle='dotted')

            for i in range(len(data.index)):
                ax.axhline(i, c='w', linewidth=1)


def plot_topograph(ax, data, plot_params):
    amp_data = pd.DataFrame(data['Amp'])
    channel_index = data['Amp'].index.get_level_values('channel')
    amp_data['y_locs'] = [plot_params['chan_locs'][ch][0] for ch in channel_index]
    amp_data['x_locs'] = [plot_params['chan_locs'][ch][1] for ch in channel_index]
    N = 50
    bottom, top = amp_data['y_locs'].min() - 0.1, amp_data['y_locs'].max() + 0.1
    left, right = bottom, top
    corners = pd.DataFrame([[0, left, bottom], [0, right, bottom], [0, left, top], [0, right, top]], columns=['Amp', 'x_locs', 'y_locs'])
    amp_data = amp_data.append(corners)
    x, y, z = amp_data['y_locs'] - left, amp_data['x_locs'] - bottom, amp_data['Amp']
    xi = np.linspace(0, right - left, N)
    yi = np.linspace(0, top - bottom, N)
    zi = scipy.interpolate.griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
    if 'zlim' in plot_params:
        zlim = plot_params['zlim']
        zi[zi < zlim[0]] = zlim[0]
        zi[zi > zlim[1]] = zlim[1]
    else:
        if 'mask' not in plot_params or plot_params['mask']:
            xy_center = [
             (right - left) / 2, (top - bottom) / 2]
            radius = (amp_data['x_locs'].max() - amp_data['x_locs'].min()) / 2 + 0.05
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
        if 'zlim' in plot_params:
            zlim = plot_params['zlim']
            CS = ax.contourf(xi, yi, zi, 60, cmap=(plot_params['color']), zorder=1, levels=(np.linspace(zlim[0], zlim[1], 40)))
        else:
            CS = ax.contourf(xi, yi, zi, 60, cmap=(plot_params['color']), zorder=1)
    ax.contour(xi, yi, zi, colors='grey', alpha=0.5, zorder=2, linestyles='solid')
    ax.scatter((x[:-4]), (y[:-4]), marker='o', c='b', alpha=0.5, s=2, zorder=3)
    if 'p_val' in data.columns:
        pval_data = pd.DataFrame(data['p_val'])
        channel_index = data['p_val'].index.get_level_values('channel')
        pval_data['y_locs'] = [plot_params['chan_locs'][ch][0] for ch in channel_index]
        pval_data['x_locs'] = [plot_params['chan_locs'][ch][1] for ch in channel_index]
        for ind, i in pval_data.iterrows():
            if i.p_val < plot_params['sig_limit']:
                ax.scatter((i.y_locs - bottom), (i.x_locs - left), c='w', s=25, alpha=1, zorder=3, linewidths=0.5, edgecolors='b')

    ax.axis('off')


def channel_locs(topo):
    label = [i for i in topo.keys()]
    x = [i[0] for i in topo.values()]
    y = [i[1] for i in topo.values()]
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i, txt in enumerate(label):
        ax.annotate(txt, (x[i], y[i]))

    ax.axis('off')
    plt.show()