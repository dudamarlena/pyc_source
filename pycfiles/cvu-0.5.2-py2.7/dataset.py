# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/dataset.py
# Compiled at: 2015-07-04 01:08:25
from __future__ import division
from traits.api import HasTraits, Any, Range, Bool, Float, Enum, Str, List, Int, Instance, Dict, Either, Property, Method, Constant, cached_property, on_trait_change, TraitError
import numpy as np
from color_map import CustomColormap
from color_legend import ColorLegend, LegendEntry
from matplotlib.colors import LinearSegmentedColormap
from dataview import DataView, DVMayavi, DVMatrix, DVCircle
from options_struct import ScalarDisplaySettings, DisplayOptions
from utils import CVUError
from threading import Thread

class SurfData(HasTraits):
    lh_verts = Any
    lh_tris = Any
    rh_verts = Any
    rh_tris = Any
    surftype = Str

    def __init__(self, lhv, lht, rhv, rht, sft):
        super(SurfData, self).__init__()
        self.lh_verts = lhv
        self.lh_tris = lht
        self.rh_verts = rhv
        self.rh_tris = rht
        self.surftype = sft


class Dataset(HasTraits):
    name = Str
    gui = Any
    nr_labels = Int
    nr_edges = Int
    labnam = List(Str)
    adj = Any
    adj_thresdiag = Property(depends_on='adj')

    @cached_property
    def _get_adj_thresdiag(self):
        adjt = self.adj.copy()
        adjt[np.where(np.eye(self.nr_labels))] = np.min(adjt[np.where(adjt)])
        return adjt

    starts = Any
    vecs = Any
    edges = Any
    srf = Instance(SurfData)
    labv = Dict
    lab_pos = Any
    dv_3d = Either(Instance(DataView), None)
    dv_mat = Either(Instance(DataView), None)
    dv_circ = Either(Instance(DataView), None)
    soft_max_edges = Int
    adjdat = Any
    left = Any
    right = Any
    interhemi = Any
    masked = Any
    lhnodes = Property(depends_on='labnam')
    rhnodes = Property(depends_on='labnam')

    @cached_property
    def _get_lhnodes(self):
        return np.where(map(lambda r: r[0] == 'l', self.labnam))[0]

    @cached_property
    def _get_rhnodes(self):
        return np.where(map(lambda r: r[0] == 'r', self.labnam))[0]

    node_colors = Any
    node_colors_default = List
    node_labels_numberless = List(Str)
    group_colors = List
    nr_groups = Int
    group_labels = List(Str)
    color_legend = Instance(ColorLegend)
    module_colors = List
    default_glass_brain_color = Constant((0.82, 0.82, 0.82))
    node_scalars = Dict
    scalar_display_settings = Instance(ScalarDisplaySettings)
    modules = List
    nr_modules = Int
    graph_stats = Dict
    opts = Instance(DisplayOptions)
    display_mode = Enum('normal', 'scalar', 'module_single', 'module_multi')
    reset_thresh = Property(Method)

    def _get_reset_thresh(self):
        if self.opts.thresh_type == 'prop':
            return self.prop_thresh
        if self.opts.thresh_type == 'abs':
            return self.abs_thresh

    thresval = Float
    curr_node = Either(Int, None)
    cur_module = Either(Int, 'custom', None)
    custom_module = List

    def __init__(self, name, lab_pos, labnam, srf, labv, gui=None, adj=None, soft_max_edges=20000, **kwargs):
        super(Dataset, self).__init__(**kwargs)
        self.gui = gui
        self.name = name
        self.opts = DisplayOptions(self)
        self.scalar_display_settings = ScalarDisplaySettings(self)
        self.lab_pos = lab_pos
        self.labnam = labnam
        self.srf = srf
        self.labv = labv
        self.nr_labels = len(labnam)
        if adj is not None:
            self.adj = adj
            self.soft_max_edges = soft_max_edges
            self.pos_helper_gen()
            self.adj_helper_gen()
        self.color_legend = ColorLegend()
        self.node_colors_gen()
        self.dv_3d = DVMayavi(self)
        self.dv_mat = DVMatrix(self)
        self.dv_circ = DVCircle(self)
        self.chg_scalar_colorbar()
        return

    def __repr__(self):
        return 'Dataset: %s' % self.name

    def __getitem__(self, key):
        if key == 0:
            return self
        if key == 1:
            return self.name
        raise KeyError('Invalid indexing to dataset.  Dataset indexing is implemented to appease CheckListEditor and can only be 0 or 1.')

    def pos_helper_gen(self, reset_scalars=True):
        self.nr_labels = n = len(self.lab_pos)
        self.nr_edges = self.nr_labels * (self.nr_labels - 1) // 2
        tri_ixes = np.triu(np.ones((n, n)), 1)
        ixes, = np.where(tri_ixes.flat)
        A_r = np.tile(self.lab_pos, (n, 1, 1))
        self.starts = np.reshape(A_r, (n * n, 3))[ixes, :]
        self.vecs = np.reshape(A_r - np.transpose(A_r, (1, 0, 2)), (n * n, 3))[ixes, :]
        self.edges = np.transpose(np.where(tri_ixes.T))[:, ::-1]
        if reset_scalars:
            self.node_scalars = {}
        self.display_mode = 'normal'

    def adj_helper_gen(self):
        self.nr_edges = self.nr_labels * (self.nr_labels - 1) // 2
        self.adjdat = np.zeros(self.nr_edges, dtype=float)
        self.interhemi = np.zeros(self.nr_edges, dtype=bool)
        self.left = np.zeros(self.nr_edges, dtype=bool)
        self.right = np.zeros(self.nr_edges, dtype=bool)
        self.masked = np.zeros(self.nr_edges, dtype=bool)
        i = 0
        self.adj[(xrange(self.nr_labels), xrange(self.nr_labels))] = 0
        n = self.nr_labels
        ixes, = np.where(np.triu(np.ones((n, n)), 1).flat)
        self.adjdat = self.adj.flat[::-1][ixes][::-1]
        from parsing_utils import same_hemi
        sh = np.vectorize(same_hemi)
        L_r = np.tile(self.labnam, (self.nr_labels, 1))
        self.interhemi = np.logical_not(sh(L_r, L_r.T)).flat[::-1][ixes][::-1]
        self.left = sh(L_r, L_r.T, 'l').flat[::-1][ixes][::-1]
        self.right = sh(L_r, L_r.T, 'r').flat[::-1][ixes][::-1]
        if self.nr_edges > self.soft_max_edges:
            cutoff = sorted(self.adjdat)[(self.nr_edges - self.soft_max_edges - 1)]
            zi = np.where(self.adjdat >= cutoff)
            if len(zi[0]) > self.soft_max_edges + 200:
                zi = np.where(self.adjdat > cutoff)
            self.starts = self.starts[zi[0], :]
            self.vecs = self.vecs[zi[0], :]
            self.edges = self.edges[zi[0], :]
            self.adjdat = self.adjdat[zi[0]]
            self.interhemi = self.interhemi[zi[0]]
            self.left = self.left[zi[0]]
            self.right = self.right[zi[0]]
            self.nr_edges = len(self.adjdat)
            self.verbose_msg(str(self.nr_edges) + ' total connections')
        sort_idx = np.argsort(self.adjdat, axis=0)
        self.adjdat = self.adjdat[sort_idx].squeeze()
        self.edges = self.edges[sort_idx].squeeze()
        self.starts = self.starts[sort_idx].squeeze()
        self.vecs = self.vecs[sort_idx].squeeze()
        self.left = self.left[sort_idx].squeeze()
        self.right = self.right[sort_idx].squeeze()
        self.interhemi = self.interhemi[sort_idx].squeeze()
        self.masked = self.masked[sort_idx].squeeze()
        if self.nr_edges < 500:
            self.opts.pthresh = 0.01
        else:
            thr = (self.nr_edges - 500) / self.nr_edges
            self.opts.pthresh = thr
        self.opts.thresh_type = 'prop'
        self.display_mode = 'normal'

    def node_colors_gen(self):
        hi_contrast_clist = ('#26ed1a', '#eaf60b', '#e726f4', '#002aff', '#05d5d5',
                             '#f4a5e0', '#bbb27e', '#641179', '#068c40')
        hi_contrast_cmap = LinearSegmentedColormap.from_list('hi_contrast', hi_contrast_clist)
        self.node_labels_numberless = map(lambda n: n.replace('div', '').strip('1234567890_'), self.labnam)
        node_groups = map(lambda n: n[3:], self.node_labels_numberless)
        node_groups_hemi1 = map(lambda n: n[3:], self.node_labels_numberless[:len(self.lhnodes)])
        node_groups_hemi2 = map(lambda n: n[3:], self.node_labels_numberless[-len(self.rhnodes):])
        a_set = set()
        self.group_labels = [ i for i in node_groups_hemi1 if i not in a_set and not a_set.add(i) ]
        last_grp = None
        for grp in node_groups_hemi2:
            if grp not in self.group_labels:
                if last_grp is None:
                    self.group_labels.insert(grp, 0)
                else:
                    self.group_labels.insert(self.group_labels.index(last_grp) + 1, grp)
            else:
                last_grp = grp

        self.nr_groups = len(self.group_labels)
        grp_ids = dict(zip(self.group_labels, xrange(self.nr_groups)))
        self.group_colors = [ hi_contrast_cmap(i / self.nr_groups) for i in range(self.nr_groups) ]
        self.node_colors = map(lambda n: self.group_colors[grp_ids[n]], node_groups)
        self.node_colors_default = list(self.node_colors)

        def create_color_legend_entry(zipped):
            label, color = zipped
            return LegendEntry(metaregion=label, col=color)

        self.color_legend.entries = map(create_color_legend_entry, zip(self.group_labels, self.group_colors))
        self.module_colors = [
         [
          255, 255, 255, 255], [204, 0, 0, 255], [51, 204, 51, 255], [66, 0, 204, 255],
         [
          80, 230, 230, 255], [51, 153, 255, 255], [255, 181, 255, 255],
         [
          255, 163, 71, 255], [221, 221, 149, 255], [183, 230, 46, 255],
         [
          77, 219, 184, 255], [255, 255, 204, 255], [0, 0, 204, 255], [204, 69, 153, 255],
         [
          255, 255, 0, 255], [0, 128, 0, 255], [163, 117, 25, 255], [255, 25, 117, 255]]
        return

    def draw(self, skip_circ=False):
        self.draw_surfs()
        self.draw_nodes(skip_circ=skip_circ)
        self.draw_conns(skip_circ=skip_circ)

    def draw_surfs(self):
        for data_view in (self.dv_3d, self.dv_mat, self.dv_circ):
            data_view.draw_surfs()

    def draw_nodes(self, skip_circ=False):
        self.set_node_colors()
        for data_view in (self.dv_3d, self.dv_mat, self.dv_circ):
            if skip_circ and data_view is self.dv_circ:
                continue
            data_view.draw_nodes()

    def set_node_colors(self):
        if self.display_mode == 'normal':
            self.node_colors = list(self.node_colors_default)
        elif self.display_mode == 'scalar':
            self.node_colors = list(self.node_colors_default)
        elif self.display_mode == 'module_single':
            new_colors = np.tile(0.3, self.nr_labels)
            new_colors[self.get_module()] = 0.8
            self.node_colors = list(self.opts.default_map._pl(new_colors))
        elif self.display_mode == 'module_multi':
            while self.nr_modules > len(self.module_colors):
                i, j = np.random.randint(18, size=(2, ))
                col = (np.array(self.module_colors[i]) + self.module_colors[j]) / 2
                col = np.array(col, dtype=int)
                self.module_colors.append(col.tolist())

            cols = self.module_colors[:self.nr_modules]
            import bct
            ci = bct.ls2ci(self.modules, zeroindexed=True)
            self.node_colors = (np.array(self.module_colors)[ci] / 255).tolist()

    def draw_conns(self, conservative=False, skip_circ=False):
        if conservative:
            new_edges = None
        else:
            new_edges, count_edges = self.select_conns(skip_circ=skip_circ)
        for data_view in (self.dv_3d, self.dv_mat, self.dv_circ):
            if skip_circ and data_view is self.dv_circ:
                continue
            elif data_view is not None:
                data_view.draw_conns(new_edges)

        return

    def select_conns(self, skip_circ=False):
        disable_circle = skip_circ or self.opts.circle_render == 'disabled'
        lo = self.thresval
        hi = np.max(self.adjdat)
        basic_conds = lambda e, a, b: not self.masked[e] and self.curr_node is None or self.curr_node in (a, b)
        if self.display_mode == 'module_single':
            module = self.get_module()
            if self.opts.module_view_style == 'intramodular':
                conds = lambda e, a, b: basic_conds(e, a, b) and a in module and b in module
            elif self.opts.module_view_style == 'intermodular':
                conds = lambda e, a, b: basic_conds(e, a, b) and (a in module) != (b in module)
            elif self.opts.module_view_stlye == 'both':
                conds = lambda e, a, b: basic_conds(e, a, b) and (a in module or b in module)
        else:
            conds = basic_conds
        new_edges = np.zeros((self.nr_edges, 2), dtype=int)
        count_edges = 0
        for e, (a, b) in enumerate(zip(self.edges[:, 0], self.edges[:, 1])):
            if conds(e, a, b):
                new_edges[e] = (
                 a, b)
                if self.dv_circ is not None and not disable_circle:
                    ev = self.adjdat[e]
                    if lo <= ev <= hi:
                        self.dv_circ.circ_data[e].set_visible(True)
                        ec = self.opts.activation_map._pl((ev - lo) / (hi - lo))
                        self.dv_circ.circ_data[e].set_ec(ec)
                        count_edges += 1
                    else:
                        self.dv_circ.circ_data[e].set_visible(False)
            else:
                new_edges[e] = (0, 0)
                if self.dv_circ is not None and not disable_circle:
                    self.dv_circ.circ_data[e].set_visible(False)

        return (
         new_edges, count_edges)

    def center_adjmat(self):
        self.dv_mat.center()

    def _load_parc(self, lab_pos, labnam, srf, labv):
        self.lab_pos = lab_pos
        self.labnam = labnam
        self.srf = srf
        self.labv = labv
        self.nr_labels = len(labnam)
        self.node_scalars = {}
        self.color_legend = ColorLegend()
        self.node_colors_gen()
        self.adj = None
        self.reset_dataviews()
        return

    def _load_adj(self, adj, soft_max_edges, reqrois, suppress_extra_rois):
        self.adj = adj
        self.soft_max_edges = soft_max_edges
        self.pos_helper_gen()
        self.adj_helper_gen()
        self.dv_3d.vectors_clear()
        self.display_mode = 'normal'
        self.dv_3d.supply_adj()
        self.dv_mat.supply_adj()
        if self.opts.circle_render == 'asynchronous':
            self.display_all(skip_circ=True)
            self.dv_3d.zaxis_view()

            def threadsafe_circle_setup():
                self.dv_circ.supply_adj(reqrois=reqrois, suppress_extra_rois=suppress_extra_rois)
                self.select_conns()
                self.dv_circ.draw_conns()

            Thread(target=threadsafe_circle_setup).start()
        else:
            self.dv_circ.supply_adj(reqrois=reqrois, suppress_extra_rois=suppress_extra_rois)
            self.display_all()
            self.dv_3d.zaxis_view()

    def load_tractography(self, params):
        if not params.track_file:
            self.error_dialog('You must specify a valid tractography file')
            return
        if not params.b0_volume:
            self.error_dialog('You must specify a B0 volume from which the registration to the diffusion space can be computed')
            return
        if not params.subjects_dir or not params.subject:
            self.error_dialog('You must specify the freesurfer reconstruction for the individual subject for registration to the surface space.')
            return
        self.dv_3d.tracks_gen(params)

    def load_modules_or_scalars(self, params):
        if not params.mat:
            self.error_dialog('You must specify a valid matrix file')
            return
        if params.whichkind == 'scalars' and not params.measure_name:
            self.error_dialog('Cannot leave scalar name blank.  cvu uses this value as a dictionary index')
            return
        import preprocessing
        try:
            ci = preprocessing.loadmat(params.mat, field=params.field_name, is_adjmat=False)
        except (CVUError, IOError) as e:
            self.error_dialog(str(e))
            return

        if params.mat_order:
            try:
                init_ord, bads = preprocessing.read_ordering_file(params.mat_order)
            except (IndexError, UnicodeDecodeError) as e:
                self.error_dialog(str(e))
                return

            if not params.ignore_deletes:
                ci = np.delete(ci, bads)
            try:
                ci_ord = preprocessing.adj_sort(init_ord, self.labnam)
            except CVUError as e:
                self.error_dialog(str(e))
                return
            except KeyError as e:
                self.error_dialog('Field not found: %s' % str(e))
                return

            ci = ci[ci_ord]
        try:
            ci = np.reshape(ci, (self.nr_labels,))
        except ValueError as e:
            self.error_dialog('The %s file is of size %i after deletions, but the dataset has %i regions' % (
             params.whichkind, len(ci), self.nr_labels))
            return

        if params.whichkind == 'modules':
            import bct
            self.modules = bct.ci2ls(ci)
            self.nr_modules = len(self.modules)
        elif params.whichkind == 'scalars':
            self.save_scalar(params.measure_name, ci)
            params._increment_scalar_count()

    def reset_dataviews(self):
        self.display_mode = 'normal'
        self.dv_3d = DVMayavi(self)
        self.dv_mat = DVMatrix(self)
        self.dv_circ = DVCircle(self)
        self.chg_scalar_colorbar()

    def save_scalar(self, name, scalars, passive=False):
        if np.squeeze(scalars).shape != (self.nr_labels,):
            if passive:
                self.verbose_msg('%s: Only Nx1 vectors can be saved as scalars' % name)
                return
            else:
                self.error_dialog('%s: Only Nx1 vectors can be saved as scalars' % name)
                return

        ci = scalars.ravel().copy()
        self.node_scalars.update({name: ci})

    def snapshot(self, params):

        def save_continuation():
            try:
                if params.whichplot == '3D brain':
                    self.dv_3d.snapshot(params)
                elif params.whichplot == 'connection matrix':
                    self.dv_mat.snapshot(params)
                elif params.whichplot == 'circle plot':
                    self.dv_circ.snapshot(params)
            except IOError as e:
                self.error_dialog(str(e))
            except KeyError as e:
                self.error_dialog('The library making the snapshot supports multiple file types and doesnt know which one you want. Please specify a file extension to disambiguate.')

        return save_continuation

    def make_movie(self, params):

        def save_continuation():
            self.dv_3d.make_movie(params)

        return save_continuation

    def make_movie_finish(self, params):
        self.dv_3d.make_movie_finish(params)

    def display_all(self, skip_circ=False):
        self.display_mode = 'normal'
        self.curr_node = None
        self.cur_module = None
        self.center_adjmat()
        self.draw(skip_circ=skip_circ)
        return

    def display_node(self, n):
        if n < 0 or n >= self.nr_labels:
            return
        self.curr_node = n
        self.draw_conns()

    def display_scalars(self):
        self.display_mode = 'scalar'
        self.draw_surfs()
        self.draw_nodes()

    def display_module(self, module):
        self.display_mode = 'module_single'
        self.curr_node = None
        self.cur_module = module
        self.draw()
        return

    def display_multi_module(self):
        if not self.modules:
            self.error_dialog('No modules defined')
            return
        self.display_mode = 'module_multi'
        self.draw_surfs()
        self.draw_nodes()

    def calculate_modules(self, thres):
        import graph, bct
        thres_adj = self.adj.copy()
        thres_adj[thres_adj < thres] = 0
        self.verbose_msg('Threshold for modularity calculation: %s' % str(thres))
        modvec = graph.calculate_modules(thres_adj)
        self.modules = bct.ci2ls(modvec)
        self.nr_modules = len(self.modules)

    def calculate_graph_stats(self, thres):
        import graph, bct
        thres_adj = self.adj.copy()
        thres_adj[thres_adj < thres] = 0
        self.verbose_msg('Threshold for graph calculations: %s' % str(thres))
        try:
            self.graph_stats = graph.do_summary(thres_adj, bct.ls2ci(self.modules), self.opts.intermediate_graphopts_list)
            for name, arr in self.graph_stats.iteritems():
                self.save_scalar(name, arr, passive=True)

        except CVUError:
            self.error_dialog('Community structure required for some of the calculations specified.  Try calculating modules first.')

    def prop_thresh(self):
        try:
            if int(round(self.opts.pthresh * self.nr_edges - 1)) < 0:
                self.thresval = float(self.adjdat[0])
            else:
                self.thresval = float(self.adjdat[int(round(self.opts.pthresh * self.nr_edges - 1))])
        except TraitError as e:
            if self.opts.pthresh > 1:
                self.warning_dialog('%s\nThreshold set to maximum' % str(e))
            elif self.opts.pthresh < 0:
                self.warning_dialog('%s\nThreshold set to minimum' % str(e))
            else:
                self.error_dialog('Programming error')

    def abs_thresh(self):
        self.thresval = self.opts.athresh
        if self.adjdat[(self.nr_edges - 1)] < self.opts.athresh:
            self.thresval = self.adjdat[(self.nr_edges - 1)]
            self.warning_dialog('Threshold over maximum! Set to maximum.')
        elif self.adjdat[0] > self.opts.athresh:
            self.thresval = self.adjdat[0]
            self.warning_dialog('Threshold under minimum! Set to minimum.')

    @on_trait_change('opts:pthresh')
    def chg_pthresh_val(self):
        if self.opts.thresh_type != 'prop':
            return
        self.reset_thresh()
        self.draw_conns(conservative=True)

    @on_trait_change('opts:athresh')
    def chg_athresh_val(self):
        if self.opts.thresh_type != 'abs':
            return
        self.reset_thresh()
        self.draw_conns(conservative=True)

    @on_trait_change('opts:thresh_type')
    def chg_thresh_type(self):
        self.draw_conns(conservative=True)

    @on_trait_change('opts:interhemi_conns_on')
    def chg_interhemi_connmask(self):
        self.masked[self.interhemi] = not self.opts.interhemi_conns_on

    @on_trait_change('opts:lh_conns_on')
    def chg_lh_connmask(self):
        self.masked[self.left] = not self.opts.lh_conns_on

    @on_trait_change('opts:rh_conns_on')
    def chg_rh_connmask(self):
        self.masked[self.right] = not self.opts.rh_conns_on

    @on_trait_change('opts:tube_conns')
    def chg_tube_conns(self):
        try:
            self.dv_3d.set_tubular_properties()
        except AttributeError:
            pass

    @on_trait_change('opts:circ_size')
    def chg_circ_size(self):
        try:
            self.dv_circ.circ.axes[0].set_ylim(0, self.opts.circ_size)
            self.dv_circ.circ.canvas.draw()
        except AttributeError:
            pass

    @on_trait_change('opts:show_floating_text')
    def chg_float_text(self):
        try:
            self.dv_3d.txt.visible = self.opts.show_floating_text
        except AttributeError:
            pass

    @on_trait_change('opts:scalar_colorbar')
    def chg_scalar_colorbar(self):
        try:
            self.dv_3d.set_colorbar(self.opts.scalar_colorbar, self.dv_3d.syrf_lh, orientation='vertical')
        except AttributeError:
            pass

    @on_trait_change('opts:render_style')
    def chg_render_style(self):
        try:
            self.dv_3d.set_surf_render_style(self.opts.render_style)
        except AttributeError:
            pass

    @on_trait_change('opts:surface_visibility')
    def chg_surf_opacity(self):
        try:
            for syrf in (self.dv_3d.syrf_lh, self.dv_3d.syrf_rh):
                syrf.actor.property.opacity = self.opts.surface_visibility

        except AttributeError:
            pass

    @on_trait_change('opts:lh_nodes_on')
    def chg_lh_nodemask(self):
        try:
            self.dv_3d.nodes_lh.visible = self.opts.lh_nodes_on
        except AttributeError:
            pass

    @on_trait_change('opts:rh_nodes_on')
    def chg_rh_nodemask(self):
        try:
            self.dv_3d.nodes_rh.visible = self.opts.rh_nodes_on
        except AttributeError:
            pass

    @on_trait_change('opts:lh_surfs_on')
    def chg_lh_surfmask(self):
        try:
            self.dv_3d.syrf_lh.visible = self.opts.lh_surfs_on
        except AttributeError:
            pass

    @on_trait_change('opts:rh_surfs_on')
    def chg_rh_surfmask(self):
        try:
            self.dv_3d.syrf_rh.visible = self.opts.rh_surfs_on
        except AttributeError:
            pass

    @on_trait_change('opts:conns_colors_on')
    def chg_conns_colors(self):
        try:
            if self.opts.conns_colors_on:
                self.dv_3d.vectors.glyph.color_mode = 'color_by_scalar'
            else:
                self.dv_3d.vectors.glyph.color_mode = 'no_coloring'
        except AttributeError:
            pass

    @on_trait_change('opts:conns_colorbar')
    def chg_conns_colorbar(self):
        try:
            self.dv_3d.set_colorbar(self.opts.conns_colorbar, self.dv_3d.vectors, orientation='horizontal')
        except AttributeError:
            pass

    @on_trait_change('opts:conns_width')
    def chg_conns_width(self):
        try:
            self.dv_3d.vectors.actor.property.line_width = self.opts.conns_width
        except AttributeError:
            pass

    @on_trait_change('opts:default_map.[cmap,reverse,fname,threshold]')
    def chg_default_map(self):
        try:
            self.draw_nodes()
        except:
            map_def = self.opts.default_map
            if map_def.cmap == 'file' and not map_def.fname:
                pass
            else:
                raise

    @on_trait_change('opts:scalar_map.[cmap,reverse,fname,threshold]')
    def chg_scalar_map(self):
        try:
            self.draw_surfs()
            self.draw_nodes()
        except:
            map_sca = self.opts.scalar_map
            if map_sca.cmap == 'file' and not map_sca.fname:
                pass
            else:
                raise

    @on_trait_change('opts:activation_map.[cmap,reverse,fname,threshold]')
    def chg_activation_map(self):
        try:
            self.dv_3d.draw_conns()
        except:
            map_act = self.opts.activation_map
            if map_act.cmap == 'file' and not map_act.fname:
                pass
            else:
                raise

    @on_trait_change('opts:connmat_map.[cmap,reverse,fname,threshold]')
    def chg_connmat_map(self):
        try:
            self.dv_mat.change_colormap()
        except:
            map_mat = self.opts.connmat_map
            if map_mat.cmap == 'file' and not map_mat.fname:
                pass
            else:
                raise

    def error_dialog(self, str):
        return self.gui.error_dialog(str)

    def warning_dialog(self, str):
        return self.gui.warning_dialog(str)

    def verbose_msg(self, str):
        return self.gui.verbose_msg(str)

    def get_module(self):
        if self.cur_module == 'custom':
            return self.custom_module
        else:
            if isinstance(self.cur_module, int) and self.modules is not None:
                return self.modules[self.cur_module]
            return