# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG\graph\put.py
# Compiled at: 2017-11-19 08:39:02
# Size of source mod 2**32: 8415 bytes
from ..default import *
from . import draw

def block(data, note, err_style='ci_band', stat_result=None, window='1ms', sig_limit=0.05, sub_plot_type='line', color='Set1', style='darkgrid', grid=True, export=None, x_len=None):
    if len(data) == 1:
        column, row = (1, 1)
        fig_size = [8, 5]
    else:
        column, row = 2, math.ceil(len(data) / 2)
        fig_size = [15, 4.5 * row]
    if x_len:
        fig_size[0] = x_len
    try:
        color = sns.color_palette(color)
    except:
        pass

    sns.set_style(style)
    fig = plt.figure(figsize=fig_size)
    for ind, (title, batch_data) in enumerate(data):
        ax = fig.add_subplot(row, column, ind + 1)
        if sub_plot_type == 'line':
            draw.line(ax, title, batch_data, note, err_style=err_style, color=color)
            if stat_result:
                if stat_result[ind] != None:
                    draw.significant(ax, stat_result[ind]['p'], window, sig_limit)
            if sub_plot_type == 'heatmap':
                draw.heatmap(ax, title, batch_data, note, 'OrRd', grid=grid)

    if export:
        fig.savefig(('%s_%d.%s' % (title, ind, export)), transparent=True)
    sns.despine()
    sns.set()
    plt.show()


def topo(data, note, topo, err_style=None, stat_result=None, window='1ms', sig_limit=0.05, color='Set1', style='white', export=None, x_len=None):
    figsize = [
     10, 10]
    if x_len:
        fig_size[0] = x_len
    try:
        color = sns.color_palette(color)
    except:
        pass

    sns.set_style(style)
    fig = plt.figure(figsize=figsize)
    for ind, (title, line_all_conditons) in enumerate(data):
        sys.stdout.write(' ' * 30 + '\r')
        sys.stdout.flush()
        sys.stdout.write('%d/%d: %s\r' % (ind + 1, len(data), title))
        sys.stdout.flush()
        ax = fig.add_subplot(10, 10, ind + 1)
        x_loc, y_loc = topo[title.split(',')[1].strip()]
        ax.set_position([x_loc, y_loc, 0.1, 0.1])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        draw.line(ax, (title.split(',')[1]), line_all_conditons, note, err_style=err_style, color=color)
        if stat_result[ind] != None:
            draw.significant(ax, stat_result[ind]['p'], window, sig_limit)
        ax.legend(bbox_to_anchor=(1.01, 1))

    if export:
        fig.savefig(('topo_output.%s' % export), transparent=True)
    sns.despine()
    sns.set()
    plt.show()


def pval_stack(stat_groups_data, note=[
 'Time(ms)', '', '', ['P > 0.1', '', 'P < 0.1', '', 'P < 0.05', '', 'P < 0.01']], export=None, x_len=None):
    row = len(stat_groups_data)
    for ind, (title, data) in enumerate(stat_groups_data):
        data = 1 - data
        data[data > 0.99] = 4
        data[(data <= 0.99) & (data > 0.95)] = 3
        data[(data <= 0.95) & (data > 0.9)] = 2
        data[data <= 0.9] = 1
        for row in range(data.shape[0]):
            for col in range(data.shape[1] - 1):
                if data.ix[(row, col - 1)] == 1 and data.ix[(row, col + 1)] == 1:
                    data.set_value(row, col, 1.0, takeable=True)

        if not x_len:
            x_len = data.shape[1] / 15
        fig = plt.figure(figsize=(x_len, data.shape[0] / 5))
        ax = fig.add_subplot(111)
        cbar_ax = fig.add_axes([0.95, 0.1, 0.01, 0.8])
        draw.heatmap(ax, title, data, note, 'OrRd', cbar_ax)
        if export:
            fig.savefig(('%s_%d.%s' % (title, ind, export)), transparent=True)

    plt.show()


def class_stack(stat_groups_data, note, export=None, x_len=None):
    row = len(stat_groups_data)
    for ind, (title, data) in enumerate(stat_groups_data):
        if not x_len:
            x_len = data.shape[1] / 40
        fig = plt.figure(figsize=(x_len, data.shape[0] / 4))
        ax = fig.add_subplot(111)
        cbar_ax = fig.add_axes([0.95, 0.1, 0.01, 0.8])
        draw.heatmap(ax, title, data, note, sns.cubehelix_palette(light=0.95, as_cmap=True), cbar_ax)
        if export:
            fig.savefig(('%s_%d.%s' % (title, ind, export)), transparent=True)

    plt.show()


def topograph_rows(data, note, topo, stat_result=None, sig_limit=0.05, export=None):
    import matplotlib.gridspec as gridspec
    for (title, batch_data), stat_result_one_group in zip(data, stat_result):
        row = len(batch_data.index.get_level_values('condition').unique())
        col = len(batch_data['data'].columns)
        w = 2 + col * 3
        h = 1 + row * 3
        gs_tp = gridspec.GridSpec(1, col)
        gs_tp.update(left=2, right=w, top=h, bottom=(h - 1), wspace=0.1)
        gs_scene = gridspec.GridSpec(row, 1)
        gs_scene.update(left=0, right=2, top=(h - 1), bottom=0, hspace=0.1)
        gs_plot = gridspec.GridSpec(row, col)
        gs_plot.update(left=2, right=w, top=(h - 1), bottom=0, wspace=0.1, hspace=0.1)
        fig = plt.figure(figsize=(0.5, 0.5))
        for ind_scene, (scene_name, scene_data) in enumerate(batch_data.groupby(level='condition')):
            ax = fig.add_subplot(gs_scene[(ind_scene, 0)])
            ax.text(text=scene_name, x=0, y=0.5, s=1, size='large', fontname='Consolas')
            ax.axis('off')
            for ind_tp, (tp, tp_data) in enumerate(scene_data.groupby(level='time', axis=1)):
                tp_in_ms = int(tp / np.timedelta64(1, 'ms'))
                tp_name = '%dms' % tp_in_ms
                tp_data.index = tp_data.index.levels[tp_data.index.names.index('channel')]
                tp_data.columns = ['data']
                ax = fig.add_subplot(gs_tp[(0, ind_tp)])
                ax.text(text=tp_name, x=(0.5 - 0.03 * len(tp_name)), y=0.5, s=1, size='large', fontname='Consolas')
                ax.axis('off')
                try:
                    stat_data = stat_result_one_group['p'][scene_name, :, tp]
                except:
                    stat_data = None

                ax = fig.add_subplot(gs_plot[(ind_scene, ind_tp)])
                draw.topograph_circle(ax, (tp_data['data']), topo, stat_data, sig_limit, zlim=(note[2]))

        if export:
            fig.savefig(('%s.%s' % (title, export)), transparent=True)

    plt.show()