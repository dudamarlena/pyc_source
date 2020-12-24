# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\utility\visualization.py
# Compiled at: 2019-07-11 07:42:40
# Size of source mod 2**32: 33764 bytes
__doc__ = 'Visualization functionality for pyrates networks and backend simulations.\n'
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from typing import Union, Optional
__author__ = 'Richard Gast, Daniel Rose'
__status__ = 'development'

def create_cmap(name: str=None, palette_type: str=None, as_cmap: bool=True, **kwargs) -> Union[(list, plt.Axes)]:
    """Create a colormap or color palette object.

    Parameters
    ----------
    name
        Name of the pyrates colormap. If specified, palette_type will be ignored.
    palette_type
        Type of the seaborn color palette to use. Only necessary if no name is specified.
    as_cmap
        If true, a matplotlib colormap object will be returned. Else a seaborn color palette (list).
    kwargs
        Keyword arguments for the wrapped seaborn functions.

    Returns
    -------
    Union[list, plt.Axes]
        cmap or seaborn color palette.

    """
    from seaborn import cubehelix_palette, dark_palette, light_palette, diverging_palette, hls_palette, husl_palette, color_palette, crayon_palette, xkcd_palette, mpl_palette
    import matplotlib.colors as mcolors
    if '/' in name:
        name1, name2 = name.split('/')
        vmin = kwargs.pop('vmin', 0.0)
        vmax = kwargs.pop('vmax', 1.0)
        if type(vmin) is float:
            vmin = (
             vmin, vmin)
        if type(vmax) is float:
            vmax = (
             vmax, vmax)
        kwargs1 = kwargs.pop(name1, kwargs)
        kwargs2 = kwargs.pop(name2, kwargs)
        cmap1 = create_cmap(name1, **kwargs1, **{'as_cmap': True})
        cmap2 = create_cmap(name2, **kwargs2, **{'as_cmap': True})
        n = kwargs.pop('n_colors', 10)
        if type(n) is int:
            n = (
             n, n)
        colors = np.vstack((cmap1(np.linspace(vmin[0], vmax[0], n[0])),
         cmap2(np.linspace(vmin[1], vmax[1], n[1])[::-1])))
        return mcolors.LinearSegmentedColormap.from_list('cmap_diverging', colors)
    else:
        if as_cmap:
            vmin = kwargs.pop('vmin', 0.0)
            vmax = kwargs.pop('vmax', 1.0)
            n = kwargs.pop('n_colors', 10)
            crange = np.linspace(vmin, vmax, n) if vmax - vmin < 1.0 else None
        else:
            crange = None
        if 'pyrates' in name:
            if name == 'pyrates_red':
                cmap = cubehelix_palette(as_cmap=as_cmap, start=-2.0, rot=-0.1, **kwargs)
            else:
                if name == 'pyrates_green':
                    cmap = cubehelix_palette(as_cmap=as_cmap, start=2.5, rot=-0.1, **kwargs)
                else:
                    if name == 'pyrates_blue':
                        cmap = dark_palette((210, 90, 60), as_cmap=as_cmap, input='husl', **kwargs)
                    else:
                        if name == 'pyrates_yellow':
                            cmap = dark_palette((70, 95, 65), as_cmap=as_cmap, input='husl', **kwargs)
                        else:
                            if name == 'pyrates_purple':
                                cmap = dark_palette((270, 50, 55), as_cmap=as_cmap, input='husl', **kwargs)
        else:
            if palette_type == 'cubehelix':
                cmap = cubehelix_palette(as_cmap=as_cmap, **kwargs)
            else:
                if palette_type == 'dark':
                    cmap = dark_palette(as_cmap=as_cmap, **kwargs)
                else:
                    if palette_type == 'light':
                        cmap = light_palette(as_cmap=as_cmap, **kwargs)
                    else:
                        if palette_type == 'hls':
                            cmap = hls_palette(**kwargs)
                        else:
                            if palette_type == 'husl':
                                cmap = husl_palette(**kwargs)
                            else:
                                if palette_type == 'diverging':
                                    cmap = diverging_palette(as_cmap=as_cmap, **kwargs)
                                else:
                                    if palette_type == 'crayon':
                                        cmap = crayon_palette(**kwargs)
                                    else:
                                        if palette_type == 'xkcd':
                                            cmap = xkcd_palette(**kwargs)
                                        else:
                                            if palette_type == 'mpl':
                                                cmap = mpl_palette(name, **kwargs)
                                            else:
                                                cmap = color_palette(name, **kwargs)
        if crange is not None:
            cmap = mcolors.LinearSegmentedColormap.from_list(name, cmap(crange))
        return cmap


def plot_timeseries(data: pd.DataFrame, variable: str='value', plot_style: str='line_plot', bg_style: str='darkgrid', **kwargs) -> plt.Axes:
    """Plot timeseries from a data frame.

    Parameters
    ----------
    data
        Results of a pyrates simulation.
    variable
        Name of the variable to be plotted
    plot_style
        Can be either `line_plot` for plotting with seaborn.lineplot() or `ridge_plot` for using seaborn.lineplot()
        on a grid with the y-axis being separated for each population.
    bg_style
        Background style of the seaborn plot
    kwargs
        Additional key-word arguments for the seaborn function.

    Returns
    -------
    plt.Axes
        Handle of the figure axes the time-series were plotted into.

    """
    import seaborn as sb
    sb.set_style(bg_style)
    demean = kwargs.pop('demean', False)
    if demean:
        for i in range(data.shape[1]):
            data.iloc[:, i] -= np.mean(data.iloc[:, i])
            data.iloc[:, i] /= np.std(data.iloc[:, i])

    else:
        title = kwargs.pop('title', '')
        xlim, ylim = kwargs.pop('xlim', None), kwargs.pop('ylim', None)
        if type(data) is pd.Series:
            data_tmp = pd.DataFrame(data=(data.values), columns=[variable], index=(data.index))
        else:
            data_tmp = data.copy()
        idx = kwargs.pop('tmin', data_tmp.index[0])
        data_tmp = data_tmp.loc[idx:, :]
        data_tmp['time'] = data_tmp.index
        df = pd.melt(data_tmp, id_vars='time',
          var_name='node',
          value_name=variable)
        if 'cmap' in kwargs:
            cmap = kwargs.pop('cmap')
        else:
            col_pal_args = [
             'start', 'rot', 'gamma', 'hue', 'light', 'dark', 'reverse', 'n_colors']
            col_pal_defs = [0.0, 0.4, 1.0, 0.8, 0.85, 0.15, True, data_tmp.shape[1] - 1]
            kwargs_tmp = {}
            for arg, default in zip(col_pal_args, col_pal_defs):
                kwargs_tmp[arg] = kwargs.pop(arg, default)

            cmap = (sb.cubehelix_palette)(**kwargs_tmp)
        if 'ax' not in kwargs.keys():
            _, ax = plt.subplots()
            kwargs['ax'] = ax
        if plot_style == 'line_plot':
            if 'ci' not in kwargs:
                kwargs['ci'] = None
            ylabel = kwargs.pop('ylabel', df.columns.values[0] if len(df.columns.values) == 1 else df.columns.values[0][(-1)])
            xlabel = kwargs.pop('xlabel', 'time')
            ax = (sb.lineplot)(data=df, x='time', y=variable, hue='node', palette=cmap, **kwargs)
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.set_xlabel(xlabel)
            if xlim:
                ax.set_xlim(xlim)
            if ylim:
                ax.set_ylim(ylim)
        else:
            if plot_style == 'ridge_plot':
                grid_args = [
                 'col_wrap', 'sharex', 'sharey', 'height', 'aspect', 'row_order', 'col_order',
                 'dropna', 'legend_out', 'margin_titles', 'xlim', 'ylim', 'gridspec_kws', 'size',
                 'subplot_kws']
                kwargs_tmp = {}
                for key in kwargs.copy().keys():
                    if key in grid_args:
                        kwargs_tmp[key] = kwargs.pop(key)

                facet_hue = kwargs.pop('facet_hue', 'node')
                facet_row = kwargs.pop('facet_row', 'node')
                ax = (sb.FacetGrid)(df, row=facet_row, hue=facet_hue, palette=cmap, **kwargs_tmp)
                plt.close(plt.figure(plt.get_fignums()[(-2)]))
                ax.map((sb.lineplot), 'time', variable, ci=None)
                ax.map((plt.axhline), y=0, lw=2, clip_on=False)
                label_args = [
                 'fontsize']
                kwargs_tmp = {}
                for key in kwargs.copy().keys():
                    if key in label_args:
                        kwargs_tmp[key] = kwargs.pop(key)

                def label(x, color, label):
                    ax_tmp = plt.gca()
                    (ax_tmp.text)(0, 0.1, label, fontweight='bold', color=color, ha='left', 
                     va='center', transform=ax_tmp.transAxes, **kwargs_tmp)

                ax.map(label, 'time')
                hspace = kwargs.pop('hspace', -0.05)
                ax.fig.subplots_adjust(hspace=hspace)
                ax.set_titles('')
                ax.set(yticks=[])
                ax.despine(bottom=True, left=True)
            else:
                raise ValueError(f"Plot style is not supported by this function: {plot_style}. Check the documentation of the argument `plot_style` for valid options.")
    return ax


def plot_connectivity(fc: Union[(np.ndarray, pd.DataFrame)], threshold: Optional[float]=None, plot_style: str='heatmap', bg_style: str='whitegrid', node_order: Optional[list]=None, auto_cluster: bool=False, **kwargs) -> plt.Axes:
    """Plot functional connectivity between nodes in backend.

    Parameters
    ----------
    fc
        Pandas dataframe containing or numpy array containing the functional connectivities.
    threshold
        Connectivtiy threshold to be applied (only connectivities larger than the threshold will be shown).
    plot_style
        Can either be `heatmap` for plotting with seaborn.heatmap or `circular_graph` for plotting with
         mne.viz.plot_connectivity_circle. Check out the respective function docstrings for information on
         their arguments (can be passed to kwargs).
    bg_style
        Only relevant if plot_style == heatmap. Then this will define the style of the background of the plot.
    node_order
        Order in which the nodes should appear in the plot.
    auto_cluster
        If true, automatic cluster detection will be used to arange the nodes
    kwargs
        Additional arguments for the fc calculation or fc plotting that can be passed.

    Returns
    -------
    plt.Axes
        Handle of the axis the plot was created in.

    """
    import seaborn as sb
    if type(fc) is np.ndarray:
        rows = kwargs.pop('yticklabels') if 'yticklabels' in kwargs.keys() else [str(i) for i in range(fc.shape[0])]
        cols = kwargs.pop('xticklabels') if 'xticklabels' in kwargs.keys() else [str(i) for i in range(fc.shape[0])]
        fc = pd.DataFrame(fc, index=[str(r) for r in rows], columns=[str(c) for c in cols])
    elif threshold:
        fc[fc < threshold] = 0.0
    else:
        if auto_cluster:
            idx_r = [i for i in range(fc.shape[0])]
            idx_c = [i for i in range(fc.shape[1])]
            col_pal_args = [
             'h', 's', 'l']
            kwargs_tmp = {}
            for key in kwargs.keys():
                if key in col_pal_args:
                    kwargs_tmp[key] = kwargs.pop(key)

            node_pal = (sb.husl_palette)((len(idx_c)), **kwargs_tmp)
            nodes = fc.columns.values
            node_lut = dict(zip(map(str, nodes), node_pal))
            node_colors = pd.Series(nodes, index=(fc.columns)).map(node_lut)
        else:
            if node_order:
                idx_c = [node_order.index(n) for n in fc.columns.values]
                idx_r = [i for i in range(fc.shape[0])]
            else:
                idx_r = [i for i in range(fc.shape[0])]
                idx_c = [i for i in range(fc.shape[1])]
        fc = fc.iloc[(idx_r, idx_c)]
        if plot_style == 'heatmap':
            if 'xticklabels' not in kwargs:
                kwargs['xticklabels'] = fc.columns.values[idx_c]
            else:
                if 'yticklabels' not in kwargs:
                    kwargs['yticklabels'] = fc.index[idx_r]
                sb.set_style(bg_style)
                if auto_cluster:
                    ax = (sb.clustermap)(data=fc, row_colors=node_colors, col_colors=node_colors, **kwargs)
                else:
                    ax = (sb.heatmap)(fc, **kwargs)
            ax.invert_yaxis()
        else:
            if plot_style == 'circular_graph':
                from mne.viz import circular_layout, plot_connectivity_circle
                node_names = fc.columns.values
                if auto_cluster:
                    cluster_args = [
                     'method', 'metric', 'z_score', 'standard_scale']
                    kwargs_tmp = {}
                    for key in kwargs.keys():
                        if key in cluster_args:
                            kwargs_tmp[key] = kwargs.pop(key)

                    clust_map = (sb.clustermap)(data=fc, row_colors=node_colors, col_colors=node_colors, **kwargs_tmp)
                    node_order = [node_names[idx] for idx in clust_map.dendrogram_row.reordered_ind]
                else:
                    if not node_order:
                        node_order = list(node_names)
                kwargs_tmp = {}
                layout_args = ['start_pos', 'start_between', 'group_boundaries', 'group_sep']
                for key in kwargs.keys():
                    if key in layout_args:
                        kwargs_tmp[key] = kwargs.pop(key)

                node_angles = circular_layout(node_names, node_order, **kwargs_tmp)
                ax = plot_connectivity_circle(fc.values, node_names, node_angles=node_angles, **kwargs)
            else:
                raise ValueError(f"Plot style is not supported by this function: {plot_style}. Check the documentation of the argument `plot_style` for valid options.")
    return ax


def plot_phase(data: pd.DataFrame, bg_style: str='whitegrid', **kwargs):
    """Plot phase of populations in a polar plot.

    Parameters
    ----------
    data
        Long (tidy) format dataframe containing fields `node`, `phase` and `amplitude`.
    bg_style
        Background style of the plot.
    kwargs
        Additional keyword args to be passed to `seaborn.FacetGrid` or `seaborn.scatterplot`

    Returns
    -------
    sb.FacetGrid
        Axis handle of the created plot.

    """
    import seaborn as sb
    sb.set(style=bg_style)
    grid_args = [
     'col_wrap', 'sharex', 'sharey', 'height', 'aspect', 'palette', 'row_order', 'col_order',
     'hue_order', 'hue_kws', 'dropna', 'legend_out', 'margin_titles', 'xlim', 'ylim',
     'gridspec_kws', 'size']
    kwargs_tmp = {}
    for key in kwargs.keys():
        if key in grid_args:
            kwargs_tmp[key] = kwargs.pop(key)

    ax = (sb.FacetGrid)(data, hue='node', subplot_kws=dict(polar=True), despine=False, **kwargs_tmp)
    scatter_kwargs = [
     'style', 'sizes', 'size_order', 'size_norm', 'markers', 'style_order', 'x_bins', 'y_bins',
     'units', 'estimator', 'ci', 'n_boot', 'alpha', 'x_jitter', 'y_jitter', 'legend', 'ax']
    kwargs_tmp2 = {}
    for key in kwargs.keys():
        if key in scatter_kwargs:
            kwargs_tmp2[key] = kwargs.pop(key)

    (ax.map)((sb.scatterplot), 'phase', 'amplitude', **kwargs_tmp2)
    ax_tmp = ax.facet_axis(0, 0)
    ax_tmp.set_ylim(np.min(data['amplitude']), np.max(data['amplitude']))
    ax_tmp.axes.yaxis.set_label_coords(1.15, 0.75)
    ax_tmp.set_ylabel((ax_tmp.get_ylabel()), rotation=0)
    locs, _ = plt.yticks()
    plt.yticks(locs)
    locs, labels = plt.xticks()
    labels = [np.round(l._x, 3) for l in labels]
    plt.xticks(locs, labels)
    return ax


def plot_psd(data: pd.DataFrame, fmin: float=0.0, fmax: float=100.0, tmin: float=0.0, **kwargs) -> plt.Axes:
    """Plots the power-spectral density for each column in data.

    Parameters
    ----------
    data
        Dataframe with simulation results.
    fmin
        Minimum frequency to be displayed.
    fmax
        Maximum frequency to be displayed.
    tmin
        Time at which to start psd calculation.
    kwargs
        Additional keyword arguments to be passed to `mne.viz.plot_raw_psd`.

    Returns
    -------
    plt.Axes
        Handle of the created plot.

    """
    from pyrates.utility import mne_from_dataframe
    from mne.viz import plot_raw_psd
    if type(data) is pd.DataFrame and 'out_var' in data.columns.names and len(data.columns.names) > 1:
        psd_keys = [
         'n_fft', 'picks', 'n_overlap', 'dB', 'estimate', 'average', 'n_jobs']
        psd_kwargs = {}
        for k in kwargs.copy():
            if k in psd_keys:
                psd_kwargs[k] = kwargs.pop(k)

        data_col = []
        col_names = []
        for col in data.columns.values:
            _ = plot_psd(data[col[:-1]], show=False, fmin=fmin, fmax=fmax, tmin=tmin, **psd_kwargs)
            pow = list(plt.gca().get_lines()[(-1)].get_ydata())
            freqs = list(plt.gca().get_lines()[(-1)].get_xdata())
            data_col.append(pow)
            col_names.append(col[:-1])
            plt.close(plt.gcf())

        df = pd.DataFrame(data=(np.asarray(data_col).T), columns=col_names, index=np.round(freqs, decimals=1))
        ax = plot_connectivity(df.values[::-1, :], xticklabels=df.columns.values, yticklabels=df.index[::-1], 
         plot_style='heatmap', **kwargs)
        return ax
    else:
        if len(data.shape) < 2:
            data = pd.DataFrame(data=(data.values), columns=['data'], index=(data.index))
        raw = mne_from_dataframe(data)
        return plot_raw_psd(raw, tmin=tmin, fmin=fmin, fmax=fmax, **kwargs).axes


def plot_tfr(data: np.ndarray, freqs: list, nodes: Optional[list]=None, separate_nodes: bool=True, **kwargs) -> plt.Axes:
    """

    Parameters
    ----------
    data
        Numpy array (n x f x t) containing the instantaneous power estimates for each node (n), each frequency (f) at
        every timestep (t).
    freqs
        Frequencies of interest.
    nodes
        Nodes of interest in order of interest.
    separate_nodes
        If true, create a separate figure for each node.
    kwargs
        Additional keyword arguments to be passed to `seaborn.heatmap` or `seaborn.FacetGrid`.

    Returns
    -------
    plt.Axes
        Handle of the created plot.

    """
    import seaborn as sb
    if not nodes:
        nodes = [i for i in range(data.shape[0])]
    if 'xticklabels' not in kwargs.keys():
        if 'step_size' in kwargs.keys():
            xticks = np.round((np.arange(0, data.shape[2]) * kwargs.pop('step_size')), decimals=3)
            kwargs['xticklabels'] = [str(t) for t in xticks]
    if 'yticklabels' not in kwargs.keys():
        kwargs['yticklabels'] = [str(f) for f in freqs]
    if separate_nodes:
        for n in range(data.shape[0]):
            _, ax = plt.subplots()
            ax = (sb.heatmap)(data[n, :, :], ax=ax, **kwargs)

    else:
        indices = pd.MultiIndex.from_product((nodes, freqs, range(data.shape[2])), names=('nodes',
                                                                                          'freqs',
                                                                                          'time'))
        data = pd.DataFrame((data.flatten()), index=indices, columns=('values', )).reset_index()
        grid_args = [
         'col_wrap', 'sharex', 'sharey', 'height', 'aspect', 'palette', 'col_order',
         'dropna', 'legend_out', 'margin_titles', 'xlim', 'ylim', 'gridspec_kws', 'size']
        kwargs_tmp = {}
        for key in kwargs.keys():
            if key in grid_args:
                kwargs_tmp[key] = kwargs.pop(key)

        ax = (sb.FacetGrid)(data, col='nodes', **kwargs_tmp)
        (ax.map_dataframe)(_draw_heatmap, 'time', 'freqs', 'values', cbar=False, square=True, **kwargs)
    return ax


def plot_network_graph(circuit, _format: str='png', path: str=None, prog='dot', **pydot_args):
    """Simple straight plot using graphviz via pydot.

    Parameters
    ----------
    circuit
        `CircuitIR` instance to plot graph from
    _format
        output format
    path
        path to print image to. If `None` is given, will try to plot using matplotlib/IPython
    prog
        graphviz layout algorithm name. Defaults to "dot". Another recommendation is "circo". Other valid options:
        "fdp", "neato", "osage", "patchwork", "twopi", "pydot_args". See graphviz documentation for more info.

    Returns
    -------

    """
    import networkx as nx
    graph = nx.MultiDiGraph()
    nodes = (node for node in circuit.graph.nodes)
    graph.add_nodes_from(nodes)
    edges = (edge for edge in circuit.graph.edges)
    graph.add_edges_from(edges)
    dot_graph = nx.drawing.nx_pydot.to_pydot(graph)
    if path:
        return write_graph(path, dot_graph, prog, **pydot_args)
    else:
        return show_graph(dot_graph, _format, prog, **pydot_args)


def plot_graph_with_subgraphs(circuit, _format: str='png', path: str=None, prog='dot', node_style='solid', cluster_style='rounded', **pydot_args):
    """Simple straight plot using graphviz via pydot.

    Parameters
    ----------
    circuit
        `CircuitIR` instance to plot graph from
    _format
        output format
    path
        path to print image to. If `None` is given, will try to plot using matplotlib/IPython
    prog
        graphviz layout algorithm name. Defaults to "dot". Another recommendation is "circo". Other valid options:
        "fdp", "neato", "osage", "patchwork", "twopi", "pydot_args". See graphviz documentation for more info.

    Returns
    -------

    """
    import pydot
    graph = pydot.Dot(graph_type='digraph', fontname='Verdana')
    clusters = {}
    for subcircuit in circuit.sub_circuits:
        clusters[subcircuit] = pydot.Cluster(subcircuit, label=subcircuit)

    for label, data in circuit.nodes(data=True):
        *subcircuit, node = label.split('/')
        node = pydot.Node(label, label=(node.split('.')[0]))
        node.set_style(node_style)
        if subcircuit:
            subcircuit = '/'.join(subcircuit)
            cluster = clusters[subcircuit]
            cluster.add_node(node)
        else:
            graph.add_node(node)

    for cluster in clusters.values():
        cluster.set_style(cluster_style)
        graph.add_subgraph(cluster)

    for source, target, _ in circuit.edges:
        graph.add_edge(pydot.Edge(source, target))

    if path:
        return write_graph(path, graph, prog, **pydot_args)
    else:
        return show_graph(graph, _format, prog, **pydot_args)


def write_graph(path, dot_graph, prog, **pydot_args):
    """Write DOT graph to file.

    Parameters
    ----------
    path
    dot_graph
    prog
    pydot_args

    Returns
    -------

    """
    import os
    path = os.path.normpath(path)
    return (dot_graph.write)(path, format=format, prog=prog, **pydot_args)


def show_graph(dot_graph, _format, prog, **pydot_args):
    """Show DOT graph using matplotlib or IPython.display

    Parameters
    ----------
    dot_graph
    _format
    prog
    pydot_args

    Returns
    -------

    """
    import matplotlib.pyplot as plt, matplotlib.image as mpimg
    if _format == 'png':
        image_bytes = (dot_graph.create_png)(prog=prog, **pydot_args)
        try:
            import sys
            _ = sys.ps1
        except AttributeError:
            from io import BytesIO
            bio = BytesIO()
            bio.write(image_bytes)
            bio.seek(0)
            img = mpimg.imread(bio)
            imgplot = plt.imshow(img, aspect='equal')
            plt.show(block=False)
            return imgplot
        else:
            from IPython.display import Image, display
            return Image(data=image_bytes)
    else:
        raise NotImplementedError(f"No plotting option implemented for format '{_format}'")


def _draw_heatmap(*args, **kwargs):
    """Wraps seaborn.heatmap to work with long, tidy format dataframes.
    """
    import seaborn as sb
    data = kwargs.pop('data')
    d = data.pivot(index=(args[1]), columns=(args[0]), values=(args[2]))
    return (sb.heatmap)(d, **kwargs)


class Interactive2DParamPlot(object):

    def __init__(self, data_map: np.array, data_series: pd.DataFrame, x_values: np.array, y_values: np.array, tmin=0.0, **kwargs):
        """Creates an interactive 2D plot that allows visualization of time series using button press events

        Derive child class and change get_data() respectively to utilize this plotting method

        Parameters
        ----------
        data_map
            2D ndarray containing a value based on each column data_series, respectively.
        data_series
            DataFrame containing all data series used to crate the data map
        x_values
            ndarray containing values used to access a column in data_series
        y_values
            ndarray containing values used to access a column in data_series
        tmin
            Starting point for time-series plots in time units (float).
        kwargs
            Additional information to access a column in data_series if necessary

        Returns
        -------

        """
        dt = kwargs.pop('dt', data_series.index[1] - data_series.index[0])
        tmin = int(tmin / dt)
        self.data = data_series.iloc[tmin:, :]
        self.x_values = x_values
        self.y_values = y_values
        self.kwargs = kwargs
        if 'subplots' in kwargs:
            self.fig, self.ax = kwargs.pop('subplots')
        else:
            self.fig, self.ax = plt.subplots(ncols=2, nrows=1, figsize=(12, 6), gridspec_kw={})
        self.marker = self.ax[0].plot(0, 0, 'x', color='white', markersize='10')
        plot_connectivity(data_map, ax=self.ax[0], yticklabels=list(np.round(y_values, decimals=2)), xticklabels=list(np.round(x_values, decimals=2)), **kwargs)
        set_num_axis_ticks(ax=(self.ax[0]), num_x_ticks_old=(data_map.shape[1]), num_y_ticks_old=(data_map.shape[0]))
        self.ax[1].grid(visible=True, color='silver')
        x, y = self.x_values[0], self.y_values[0]
        time_series = self.get_data(x, y)
        data_min, data_max = np.min(self.data.values), np.max(self.data.values)
        data_margin = (data_max - data_min) * 0.1
        cmap = create_cmap('pyrates_purple', as_cmap=False, n_colors=1, reverse=True)
        plot_timeseries(time_series, ax=(self.ax[1]), ylim=[data_min - data_margin, data_max + data_margin], cmap=cmap)
        self.ax[1].set_title(f"x: {np.round(x, decimals=2)}, y: {np.round(y, decimals=2)}")
        self.fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        """Try to access a column in data_series using x and y values based on cursor position

        Is called on mouse button press event. Converts the current cursor coordinates inside the plot into x and y
        values based on the data in x_values and y_values. x and y values are used to access a column in data_series.
        Access of data_series can be customized in self.get_data().

        :param event:
        :return:
        """
        if event.inaxes != self.ax[0]:
            return
        self.marker[0].remove()
        x_sample = event.xdata
        y_sample = event.ydata
        x_value = self.x_values[int(x_sample)]
        y_value = self.y_values[int(y_sample)]
        self.marker = self.ax[0].plot(x_sample, y_sample, 'x', color='white', markersize='10')
        self.update_lineplot(x_value, y_value)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update_lineplot(self, x, y):
        line = self.ax[1].get_lines()[0]
        data = self.get_data(x, y)
        line.set_data(data.index, data.values)
        self.ax[1].set_title(f"x: {np.round(x, decimals=2)}, y: {np.round(y, decimals=2)}")
        self.ax[1].autoscale_view()

    def set_map_xlabel(self, label):
        self.ax[0].set_xlabel(label)

    def set_map_ylabel(self, label):
        self.ax[0].set_ylabel(label)

    def set_map_title(self, title):
        self.ax[0].set_title(title)

    def set_series_xlabel(self, label):
        self.ax[1].set_xlabel(label)

    def set_series_ylabel(self, label):
        self.ax[1].set_ylabel(label)

    def get_data(self, x_value, y_value, *argv, **kwargs):
        """Virtual method

        Derive a child class from Interactive2DParamPlotTemplate and rewrite this function to access data using
        x_value, y_value und kwargs (accessible using self.kwargs[])

        Example:
            class Interactive2DParamPlot(Interactive2DParamPlotTemplate):

                def get_data(self, x_value, y_value):
                    return self.data[y_value][x_value][self.kwargs["param_1"]][self.kwargs["param_2"]]

        """
        raise NotImplementedError


def save_fig_as_pickle(fp, fig):
    """Save a figure object in pickle format.

    Parameters
    ----------
    fp
        /desired_dir/desired_filename.pickle
    fig
        Figure object as returned by matplotlib.pyplot.subplots

    Returns
    -------

    """
    import pickle
    pickle_out = open(fp, 'wb')
    pickle.dump(fig, pickle_out)
    pickle_out.close()


def load_fig_from_pickle():
    """Opens a file dialog to select and load a *.pickle file.

    If the pickle file contains a figure object it will automatically be plotted

    Returns
    -------

    """
    import pickle
    from tkinter import Tk, filedialog
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=(('pickle files', '*.pickle'),
                                                      ('all files', '*.*')))
    try:
        pickle_in = open(file_path, 'rb')
        pickle.load(pickle_in)
        plt.show()
    except (FileNotFoundError, TypeError, pickle.UnpicklingError):
        pass


def set_num_axis_ticks(ax, num_x_ticks_old, num_y_ticks_old, num_x_ticks_new=10, num_y_ticks_new=10):
    """Set the number of x and y ticks of a plot axis

    Parameters
    ----------
    ax
    num_x_ticks_old
    num_y_ticks_old
    num_x_ticks_new
    num_y_ticks_new

    Returns
    -------

    """
    step_tick_x, step_tick_y = int(num_x_ticks_old / num_x_ticks_new), int(num_y_ticks_old / num_y_ticks_new)
    for n, tick in enumerate(ax.xaxis.iter_ticks()):
        if n % step_tick_x != 0:
            tick[0].set_visible(False)

    for n, tick in enumerate(ax.yaxis.iter_ticks()):
        if n % step_tick_y != 0:
            tick[0].set_visible(False)