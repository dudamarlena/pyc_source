# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/generate.py
# Compiled at: 2020-04-04 16:23:02
# Size of source mod 2**32: 5502 bytes
from __future__ import division
import pytplot
from pyqtgraph import LabelItem
import pyqtgraph as pg
from .TVarFigureAxisOnly import TVarFigureAxisOnly

def generate_stack(name, var_label=None, combine_axes=True, vert_spacing=25):
    new_stack = pg.GraphicsLayoutWidget()
    xaxis_thickness = 35
    varlabel_xaxis_thickness = 20
    title_thickness = 50
    new_stack.setWindowTitle(pytplot.tplot_opt_glob['title_text'])
    new_stack.resize(pytplot.tplot_opt_glob['window_size'][0], pytplot.tplot_opt_glob['window_size'][1])
    all_plots = []
    axis_types = []
    i = 0
    num_plots = len(name)
    total_psize = 0
    j = 0
    while j < num_plots:
        total_psize += pytplot.data_quants[name[j]].attrs['plot_options']['extras']['panel_size']
        j += 1

    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [
             var_label]
        varlabel_correction = len(var_label) * varlabel_xaxis_thickness
    else:
        varlabel_correction = 0
        xaxis_thickness = 0
        title_thickness = 0
    p_to_use = (pytplot.tplot_opt_glob['window_size'][1] - xaxis_thickness - title_thickness - varlabel_correction) / total_psize
    titlerow = 0
    spacing_in_pixels = vert_spacing
    new_stack.ci.layout.setSpacing(spacing_in_pixels)
    while i < num_plots:
        last_plot = i == num_plots - 1
        p_height = int(pytplot.data_quants[name[i]].attrs['plot_options']['extras']['panel_size'] * p_to_use)
        if last_plot:
            p_height += xaxis_thickness
        elif i == 0:
            if _set_pyqtgraph_title(new_stack):
                titlerow = 1
            new_stack.ci.layout.setRowPreferredHeight(i + titlerow, p_height)
            new_fig = _get_figure_class((name[i]), show_xaxis=last_plot)
            new_stack.addItem(new_fig, row=(i + titlerow), col=0)
            axis_types.append(new_fig.getaxistype())
            new_fig.buildfigure()
            if pytplot.tplot_opt_glob['black_background']:
                pg.setConfigOptions(background='k')
        else:
            pg.setConfigOptions(background='w')
        all_plots.append(new_fig.getfig())
        i = i + 1

    if var_label is not None:
        x_axes_index = 0
        for new_x_axis in var_label:
            new_axis = TVarFigureAxisOnly(new_x_axis)
            new_stack.addItem(new_axis, row=(num_plots + titlerow + x_axes_index), col=0)
            x_axes_index += 1
            axis_types.append(('time', False))
            all_plots.append(new_axis)

    first_type = {}
    if combine_axes:
        k = 0
        while k < len(axis_types):
            if axis_types[k][0] not in first_type:
                first_type[axis_types[k][0]] = k
            else:
                all_plots[k].plotwindow.setXLink(all_plots[first_type[axis_types[k][0]]].plotwindow)
            k += 1

    return new_stack


def _set_pyqtgraph_title(layout):
    """
    Private function to add a title to the first row of the window.
    Returns True if a Title is set.  Else, returns False.
    """
    title_set = False
    if 'title_size' in pytplot.tplot_opt_glob:
        size = pytplot.tplot_opt_glob['title_size']
    elif 'title_text' in pytplot.tplot_opt_glob:
        title_set = True
        if pytplot.tplot_opt_glob['title_text'] != '' and pytplot.tplot_opt_glob['black_background']:
            layout.addItem(LabelItem((pytplot.tplot_opt_glob['title_text']), size=size, color='w'), row=0, col=0)
        else:
            layout.addItem(LabelItem((pytplot.tplot_opt_glob['title_text']), size=size, color='k'), row=0, col=0)
    return title_set


def _get_figure_class(tvar_name, show_xaxis=True):
    if 'plotter' in pytplot.data_quants[tvar_name].attrs['plot_options']['extras'] and pytplot.data_quants[tvar_name].attrs['plot_options']['extras']['plotter'] in pytplot.qt_plotters:
        cls = pytplot.qt_plotters[pytplot.data_quants[tvar_name].attrs['plot_options']['extras']['plotter']]
    else:
        spec_keyword = pytplot.data_quants[tvar_name].attrs['plot_options']['extras'].get('spec', False)
        alt_keyword = pytplot.data_quants[tvar_name].attrs['plot_options']['extras'].get('alt', False)
        map_keyword = pytplot.data_quants[tvar_name].attrs['plot_options']['extras'].get('map', False)
        if spec_keyword:
            cls = pytplot.qt_plotters['qtTVarFigureSpec']
        else:
            if alt_keyword:
                cls = pytplot.qt_plotters['qtTVarFigureAlt']
            else:
                if map_keyword:
                    cls = pytplot.qt_plotters['qtTVarFigureMap']
                else:
                    cls = pytplot.qt_plotters['qtTVarFigure1D']
    return cls(tvar_name, show_xaxis=show_xaxis)