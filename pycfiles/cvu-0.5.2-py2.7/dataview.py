# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/dataview.py
# Compiled at: 2015-11-10 11:18:54
from __future__ import division
import numpy as np
from traits.api import HasTraits, Str, Any, List, Instance, Bool, Property, on_trait_change
from utils import CVUError
import shell_utils
from color_map import set_lut, set_color_range
from mayavi import mlab
from mayavi.core.ui.api import MlabSceneModel
from chaco.api import Plot, ArrayPlotData, ColorMapper, PlotGraphicsContext
from chaco.tools.api import ZoomTool, PanTool
from color_axis import ColorfulAxis
import circle_plot

class DataView(HasTraits):
    ds = Any
    current_subject = Str
    current_parcellation = Str
    current_matrix_file = Str

    def __init__(self, ds, **kwargs):
        super(DataView, self).__init__(**kwargs)
        self.ds = ds

    def supply_adj(self):
        raise NotImplementedError()

    def error_dialog(self, str):
        return self.ds.error_dialog(str)

    def warning_dialog(self, str):
        return self.ds.warning_dialog(str)

    def verbose_msg(self, str):
        return self.ds.verbose_msg(str)

    def draw_surfs(self):
        raise NotImplementedError()

    def draw_nodes(self):
        raise NotImplementedError()

    def draw_conns(self, new_edges=None):
        raise NotImplementedError()

    def snapshot(self):
        raise NotImplementedError()


class DVMayavi(DataView):
    scene = Instance(MlabSceneModel)
    syrf_lh = Any
    syrf_rh = Any
    nodes_lh = Any
    nodes_rh = Any
    vectors = Any
    tracks = Any
    txt = Any
    thres = Any
    surfs_cracked = Bool(False)

    def __init__(self, ds, engine=None, **kwargs):
        super(DVMayavi, self).__init__(ds, **kwargs)
        if engine is not None:
            self.scene = MlabSceneModel(engine=engine)
        else:
            self.scene = MlabSceneModel()
        return

    @on_trait_change('scene:activated')
    def setup(self):
        try:
            mlab.figure(bgcolor=(0.34, 0.34, 0.34), figure=self.scene.mayavi_scene)
        except Exception as e:
            print str(e)
            return

        self.surfs_gen()
        self.nodes_gen()
        from pyface.api import GUI
        gui = GUI()
        gui.invoke_later(self.zaxis_view)
        if self.ds.adj is not None:
            self.supply_adj()
            self.ds.display_all()
        return

    def supply_adj(self):
        self.vectors_gen()
        pck = self.scene.mayavi_scene.on_mouse_pick(self.leftpick_callback)
        pck.tolerance = 0.02
        self.scene.mayavi_scene.on_mouse_pick(self.rightpick_callback, button='Right')

    def zaxis_view(self):
        mlab.view(distance=350, figure=self.scene.mayavi_scene)

    def surfs_clear(self):
        try:
            self.syrf_lh.parent.parent.parent.remove()
            self.syrf_rh.parent.parent.parent.remove()
        except (ValueError, AttributeError):
            self.ds.verbose_msg('failed to remove old surfaces')

    def surfs_gen(self):
        self.syrf_lh = mlab.triangular_mesh(self.ds.srf.lh_verts[:, 0], self.ds.srf.lh_verts[:, 1], self.ds.srf.lh_verts[:, 2], self.ds.srf.lh_tris, opacity=self.ds.opts.surface_visibility, color=self.ds.default_glass_brain_color)
        self.syrf_rh = mlab.triangular_mesh(self.ds.srf.rh_verts[:, 0], self.ds.srf.rh_verts[:, 1], self.ds.srf.rh_verts[:, 2], self.ds.srf.rh_tris, opacity=self.ds.opts.surface_visibility, color=self.ds.default_glass_brain_color)
        self.surfs_cracked = False
        for syrf in (self.syrf_lh, self.syrf_rh):
            syrf.actor.actor.pickable = 0
            set_lut(syrf, self.ds.opts.scalar_map)

        self.ds.chg_lh_surfmask()
        self.ds.chg_rh_surfmask()

    def cracked_surfs_gen(self):
        from parsing_utils import demangle_hemi
        tri_inds_l, tri_inds_r = [], []
        for l in self.ds.labnam:
            if l[0] == 'l':
                tris = self.ds.srf.lh_tris
                tri_inds = tri_inds_l
            elif l[0] == 'r':
                tris = self.ds.srf.rh_tris
                tri_inds = tri_inds_r
            else:
                self.error_dialog('Bad label name %s' % l)
                return
            v_as_set = set(self.ds.labv[demangle_hemi(l)])
            ts, = np.where([ v_as_set.issuperset(tri) for tri in tris ])
            tri_inds.extend(ts)

        self.syrf_lh = mlab.triangular_mesh(self.ds.srf.lh_verts[:, 0], self.ds.srf.lh_verts[:, 1], self.ds.srf.lh_verts[:, 2], self.ds.srf.lh_tris[tri_inds_l], opacity=self.ds.opts.surface_visibility, color=self.ds.default_glass_brain_color, figure=self.scene.mayavi_scene)
        self.syrf_rh = mlab.triangular_mesh(self.ds.srf.rh_verts[:, 0], self.ds.srf.rh_verts[:, 1], self.ds.srf.rh_verts[:, 2], self.ds.srf.rh_tris[tri_inds_r], opacity=self.ds.opts.surface_visibility, color=self.ds.default_glass_brain_color, figure=self.scene.mayavi_scene)
        self.surfs_cracked = True
        for syrf in (self.syrf_lh, self.syrf_rh):
            syrf.actor.actor.pickable = 0
            set_lut(syrf, self.ds.opts.scalar_map)

        self.ds.chg_lh_surfmask()
        self.ds.chg_rh_surfmask()

    def nodes_clear(self):
        try:
            self.nodes_lh.parent.parent.remove()
            self.nodes_rh.parent.parent.remove()
            self.txt.remove()
        except (ValueError, AttributeError):
            pass

    def nodes_gen(self):
        nodesource_lh = mlab.pipeline.scalar_scatter(self.ds.lab_pos[(self.ds.lhnodes, 0)], self.ds.lab_pos[(self.ds.lhnodes, 1)], self.ds.lab_pos[(self.ds.lhnodes, 2)], figure=self.scene.mayavi_scene)
        self.nodes_lh = mlab.pipeline.glyph(nodesource_lh, scale_mode='none', scale_factor=3.0, mode='sphere', figure=self.scene.mayavi_scene)
        nodesource_rh = mlab.pipeline.scalar_scatter(self.ds.lab_pos[(self.ds.rhnodes, 0)], self.ds.lab_pos[(self.ds.rhnodes, 1)], self.ds.lab_pos[(self.ds.rhnodes, 2)], figure=self.scene.mayavi_scene)
        self.nodes_rh = mlab.pipeline.glyph(nodesource_rh, scale_mode='none', scale_factor=3.0, mode='sphere', figure=self.scene.mayavi_scene)
        self.txt = mlab.text3d(0, 0, 83, '', scale=4.0, color=(0.8, 0.6, 0.98), figure=self.scene.mayavi_scene)
        self.txt.actor.actor.pickable = 0
        for nodes in (self.nodes_lh, self.nodes_rh):
            nodes.glyph.color_mode = 'color_by_scalar'

        self.ds.chg_lh_nodemask()
        self.ds.chg_rh_nodemask()
        self.ds.chg_scalar_colorbar()
        self.draw_nodes()

    def vectors_clear(self):
        try:
            self.vectors.parent.parent.parent.remove()
        except (ValueError, AttributeError):
            pass

    def vectors_gen(self):
        vectorsrc = mlab.pipeline.vector_scatter(self.ds.starts[:, 0], self.ds.starts[:, 1], self.ds.starts[:, 2], self.ds.vecs[:, 0], self.ds.vecs[:, 1], self.ds.vecs[:, 2], figure=self.scene.mayavi_scene)
        vectorsrc.mlab_source.dataset.point_data.scalars = self.ds.adjdat
        self.ds.reset_thresh()
        self.thres = mlab.pipeline.threshold(vectorsrc, name='threshold', low=self.ds.thresval, up=np.max(self.ds.adjdat), figure=self.scene.mayavi_scene)
        self.thres.auto_reset_lower = False
        self.thres.auto_reset_upper = False
        self.vectors = mlab.pipeline.vectors(self.thres, colormap='black-white', line_width=self.ds.opts.conns_width, scale_mode='vector', figure=self.scene.mayavi_scene)
        set_lut(self.vectors, self.ds.opts.activation_map)
        self.vectors.glyph.glyph.clamping = False
        self.vectors.actor.property.opacity = 0.3
        self.vectors.actor.actor.pickable = False
        self.set_tubular_properties()
        set_lut(self.vectors, self.ds.opts.activation_map)
        self.ds.chg_conns_colors()
        self.ds.chg_lh_connmask()
        self.ds.chg_rh_connmask()
        self.ds.chg_interhemi_connmask()
        self.ds.chg_conns_colorbar()
        self.txt.set(text='')

    def tracks_clear(self):
        try:
            self.tracks.parent.parent.parent.remove()
        except (ValueError, AttributeError):
            pass

    def tracks_gen(self, params):
        import tractography
        self.tracks = tractography.plot_fancily(params.track_file, figure=self.scene.mayavi_scene)
        tractography.apply_affines_carefully(self.tracks, params.b0_volume, params.track_file, params.subject, params.subjects_dir, fsenvsrc=params.fs_setup)
        tractography.fix_skewing(self.tracks, use_fsavg5=False, lhsurf=self.syrf_lh, rhsurf=self.syrf_rh)

    def draw_surfs(self):
        from parsing_utils import demangle_hemi
        srf_scalar = self.ds.scalar_display_settings.surf_color
        nc = self.ds.scalar_display_settings.node_color
        if self.ds.display_mode == 'scalar' and srf_scalar:
            scalars = self.ds.node_scalars[srf_scalar]
            colors_lh = np.zeros(len(self.ds.srf.lh_verts))
            colors_rh = np.zeros(len(self.ds.srf.rh_verts))
            for i, l in enumerate(self.ds.labnam):
                vertices = self.ds.labv[demangle_hemi(l)]
                if l[0] == 'l':
                    colors_lh[vertices] = scalars[i]
                elif l[0] == 'r':
                    colors_rh[vertices] = scalars[i]

            self.syrf_lh.mlab_source.scalars = colors_lh
            self.syrf_rh.mlab_source.scalars = colors_rh
            for syrf in (self.syrf_lh, self.syrf_rh):
                set_lut(syrf, self.ds.opts.scalar_map)
                set_color_range(syrf, scalars)
                syrf.actor.mapper.scalar_visibility = True

        elif self.ds.display_mode == 'scalar' and nc:
            scalars = self.ds.node_scalars[nc]
            min_scale, max_scale = np.min(scalars), np.max(scalars)
            colors = np.tile(min_scale, (len(self.ds.srf.lh_verts),))
            colors[0] = max_scale
            self.syrf_lh.mlab_source.scalars = colors
            for syrf in (self.syrf_lh, self.syrf_rh):
                syrf.actor.mapper.scalar_visibility = False

        elif self.ds.display_mode == 'module_multi' and self.ds.opts.modules_on_surface:
            new_colors = np.array(self.ds.module_colors[:self.ds.nr_modules + 1])
            for syrf, nodes, letter, verts in (
             (
              self.syrf_lh, self.ds.lhnodes, 'l', self.ds.srf.lh_verts),
             (
              self.syrf_rh, self.ds.rhnodes, 'r', self.ds.srf.rh_verts)):
                colors = np.zeros(len(verts))
                manager = syrf.module_manager.scalar_lut_manager
                manager.lut_mode = 'black-white'
                manager.number_of_colors = self.ds.nr_modules
                manager.lut.table = new_colors
                import bct
                ci = bct.ls2ci(self.ds.modules, zeroindexed=True)[nodes]
                i = 0
                for l in self.ds.labnam:
                    if not l[0] == letter:
                        continue
                    vertices = self.ds.labv[demangle_hemi(l)]
                    colors[vertices] = ci[i] + 1
                    i += 1

                syrf.mlab_source.scalars = colors
                set_color_range(syrf, (0.0, self.ds.nr_modules + 1))
                syrf.actor.mapper.scalar_visibility = True

        else:
            for syrf in (self.syrf_lh, self.syrf_rh):
                syrf.actor.mapper.scalar_visibility = False

    def draw_nodes(self):
        nc = self.ds.scalar_display_settings.node_color
        ns = self.ds.scalar_display_settings.node_size
        lhn = self.nodes_lh
        lhn_ix = self.ds.lhnodes
        rhn = self.nodes_rh
        rhn_ix = self.ds.rhnodes
        for nodes, ixes in ((lhn, lhn_ix), (rhn, rhn_ix)):
            nr = len(ixes)
            if self.ds.display_mode == 'scalar' and ns:
                scalars = self.ds.node_scalars[ns]
                scalars = (scalars - np.min(scalars)) / (np.max(scalars) - np.min(scalars))
                scalars = (np.exp(scalars * np.log(2)) - 1) / (np.e - 1)
                nodes.glyph.scale_mode = 'scale_by_vector'
                nodes.glyph.glyph.scale_factor = 12
                nodes.mlab_source.dataset.point_data.vectors = np.tile(scalars[ixes], (3,
                                                                                       1)).T
            else:
                nodes.glyph.scale_mode = 'data_scaling_off'
                nodes.glyph.glyph.scale_factor = 3
            if self.ds.display_mode == 'normal' or self.ds.display_mode == 'scalar' and not nc or self.ds.display_mode in ('module_single',
                                                                                                                           'module_multi') and self.ds.opts.modules_on_surface:
                scalars = np.tile(0.3, nr)
                set_lut(nodes, self.ds.opts.default_map)
                set_color_range(nodes, (0.0, 1.0))
                nodes.mlab_source.dataset.point_data.scalars = scalars
            elif self.ds.display_mode == 'scalar':
                scalars = self.ds.node_scalars[nc]
                set_lut(nodes, self.ds.opts.scalar_map)
                set_color_range(nodes, scalars)
                nodes.mlab_source.dataset.point_data.scalars = scalars[ixes]
            elif self.ds.display_mode == 'module_single':
                scalars = np.tile(0.3, self.ds.nr_labels)
                scalars[self.ds.get_module()] = 0.8
                set_lut(nodes, self.ds.opts.default_map)
                set_color_range(nodes, (0.0, 1.0))
                nodes.mlab_source.dataset.point_data.scalars = scalars[ixes]
            elif self.ds.display_mode == 'module_multi':
                new_colors = np.array(self.ds.module_colors[:self.ds.nr_modules + 1])
                manager = nodes.module_manager.scalar_lut_manager
                manager.lut_mode = 'black-white'
                manager.number_of_colors = self.ds.nr_modules
                manager.lut.table = new_colors
                import bct
                nodes.mlab_source.dataset.point_data.scalars = bct.ls2ci(self.ds.modules, zeroindexed=True)[ixes] + 1
                set_color_range(nodes, (0.0, self.ds.nr_modules + 1))

        mlab.draw()

    def draw_conns(self, new_edges=None):
        try:
            self.thres.set(lower_threshold=self.ds.thresval)
            lo = self.thres.lower_threshold
            hi = self.thres.upper_threshold
            set_lut(self.vectors, self.ds.opts.activation_map)
            if new_edges is not None:
                new_starts = self.ds.lab_pos[new_edges[:, 0]]
                new_vecs = self.ds.lab_pos[new_edges[:, 1]] - new_starts
                self.vectors.mlab_source.reset(x=new_starts[:, 0], y=new_starts[:, 1], z=new_starts[:, 2], u=new_vecs[:, 0], v=new_vecs[:, 1], w=new_vecs[:, 2])
            if self.ds.curr_node is not None:
                self.vectors.actor.property.opacity = 0.75
                self.txt.set(text='  %s' % self.ds.labnam[self.ds.curr_node])
            else:
                self.vectors.actor.property.opacity = 0.5 if self.ds.opts.tube_conns else 0.3
                self.txt.set(text='')
            mlab.draw()
        except AttributeError:
            pass

        return

    def cleanup(self):
        self.surfs_clear()
        self.nodes_clear()
        self.vectors_clear()
        self.tracks_clear()

    def set_colorbar(self, on, mayavi_obj, orientation='vertical'):
        if on:
            mlab.colorbar(object=mayavi_obj, orientation=orientation, title='')
        else:
            mayavi_obj.module_manager.scalar_lut_manager.show_scalar_bar = False

    def set_surf_render_style(self, style):
        self.ds.opts.lh_surfs_on = True
        self.ds.opts.rh_surfs_on = True
        if self.surfs_cracked:
            if style == 'cracked glass':
                return
            self.surfs_clear()
            self.surfs_gen()
            self.draw_surfs()
        if style == 'cracked_glass':
            self.surfs_clear()
            self.cracked_surfs_gen()
            self.draw_surfs()
        else:
            for syrf in [self.syrf_lh, self.syrf_rh]:
                if style == 'contours':
                    syrf.actor.property.representation = 'surface'
                    syrf.enable_contours = True
                    syrf.contour.number_of_contours = 250
                    continue
                else:
                    syrf.enable_contours = False
                if style == 'glass':
                    syrf.actor.property.representation = 'surface'
                elif style == 'wireframe':
                    syrf.actor.property.representation = 'wireframe'
                elif style == 'speckled':
                    syrf.actor.property.representation = 'points'

    def set_tubular_properties(self):
        if self.ds.opts.tube_conns:
            self.vectors.glyph.glyph_source.glyph_source = self.vectors.glyph.glyph_source.glyph_dict['cylinder_source']
            self.vectors.glyph.glyph_source.glyph_source.radius = 0.007 * self.ds.opts.conns_width
            self.vectors.actor.property.opacity = 0.5
        else:
            self.vectors.glyph.glyph_source.glyph_source = self.vectors.glyph.glyph_source.glyph_dict['glyph_source2d']
            self.vectors.glyph.glyph_source.glyph_source.glyph_type = 'dash'
            self.vectors.actor.property.opacity = 0.3

    def leftpick_callback(self, picker):
        for nodes in (self.nodes_lh, self.nodes_rh):
            if picker.actor in nodes.actor.actors:
                ptid = int(picker.point_id / nodes.glyph.glyph_source.glyph_source.output.points.to_array().shape[0])
                if ptid != -1 and nodes is self.nodes_lh:
                    self.ds.display_node(self.ds.lhnodes[ptid])
                elif ptid != -1 and nodes is self.nodes_rh:
                    self.ds.display_node(self.ds.rhnodes[ptid])

    def rightpick_callback(self, picker):
        self.ds.display_all()

    def snapshot(self, params):
        res = np.ceil(500 * params.dpi / 8000 * 111)
        from mayavi import __version__ as mayavi_version
        if float(mayavi_version[:3]) >= 4.3:
            mlab.savefig(params.savefile, figure=self.scene.mayavi_scene, size=(
             res, res))
        else:
            self.hack_mlabsavefig(params.savefile, size=(res, res))

    def hack_mlabsavefig(self, fname, size):
        oldx, oldy = self.scene.scene_editor.get_size()
        curx, cury = self.scene.scene_editor.control.Parent.Parent.Size
        cury -= 32
        self.scene.scene_editor.set_size((curx, cury))
        self.txt.visible = False
        magnif_desired = max(size[0] // curx, size[1] // cury) + 1
        newsize = (int(size[0] / magnif_desired), int(size[1] / magnif_desired))
        self.scene.scene_editor.set_size(newsize)
        from tvtk.api import tvtk
        filter = tvtk.WindowToImageFilter(read_front_buffer=True)
        filter.magnification = int(magnif_desired)
        self.scene.scene_editor._lift()
        filter.input = self.scene.scene_editor._renwin
        ex = tvtk.PNGWriter()
        ex.file_name = fname
        ex.input = filter.output
        self.scene.scene_editor._exporter_write(ex)
        self.scene.scene_editor.set_size((oldx, oldy))
        self.txt.visible = self.ds.opts.show_floating_text

    def make_movie(self, params):
        self.animator = None
        xs, ys = self.scene.scene_editor.control.GetScreenPositionTuple()
        ys += 32
        xe, ye = tuple(self.scene.scene_editor.get_size())
        cmd = 'ffmpeg -loglevel error -y -f x11grab -s %ix%i -r %i -b %i -i :0.0+%i,%i %s' % (
         xe, ye, params.framerate, params.bitrate * 1024, xs, ys, params.savefile)
        try:
            self.ffmpeg_process = shell_utils.sh_cmd_retproc(cmd, params.debug)
            self.make_movie_animate(params.samplerate, params.anim_style, params.rotate_deg)
        except CVUError as e:
            self.error_dialog(str(e))

        return

    def make_movie_animate(self, samplerate, rotate_on, rotate_deg):
        if not rotate_on:
            return
        from mayavi.tools.animator import Animator

        def anim():
            i = 0
            while True:
                if rotate_on:
                    self.scene.camera.azimuth(rotate_deg)
                    self.scene.render()
                yield

        animation = anim()
        fps_in = 1000 // samplerate
        self.animator = Animator(fps_in, animation.next)

    def make_movie_finish(self, params):
        if self.animator:
            self.animator.timer.Stop()
            del self.animator
        self.ffmpeg_process.communicate('q')
        if self.ffmpeg_process.returncode:
            self.error_dialog('ffmpeg failed with error code %s' % self.ffmpeg_process.returncode)
            return
        del self.ffmpeg_process
        self.verbose_msg('Movie saved successfully to %s' % params.savefile)


class DVMatrix(DataView):
    conn_mat = Any
    xa = Instance(ColorfulAxis)
    ya = Instance(ColorfulAxis)

    def __init__(self, ds, **kwargs):
        super(DVMatrix, self).__init__(ds, **kwargs)
        if self.ds.adj is not None:
            self.chaco_gen()
        else:
            self.empty_gen()
        return

    def supply_adj(self):
        self.conn_mat.data.set_data('imagedata', self.ds.adj_thresdiag)

    def chaco_gen(self):
        self.conn_mat = Plot(ArrayPlotData(imagedata=self.ds.adj_thresdiag))
        cm = ColorMapper.from_palette_array(self.ds.opts.connmat_map._pl(xrange(256)))
        self.conn_mat.img_plot('imagedata', name='connmatplot', colormap=cm)
        self.conn_mat.tools.append(ZoomTool(self.conn_mat))
        self.conn_mat.tools.append(PanTool(self.conn_mat))
        self.xa = ColorfulAxis(self.conn_mat, self.ds.node_colors, 'x')
        self.ya = ColorfulAxis(self.conn_mat, self.ds.node_colors, 'y')
        self.conn_mat.underlays = [self.xa, self.ya]

    def empty_gen(self):
        from chaco.api import Greys
        img = np.zeros((self.ds.nr_labels, self.ds.nr_labels))
        self.conn_mat = Plot(ArrayPlotData(imagedata=img))
        cm = ColorMapper.from_palette_array(self.ds.opts.connmat_map._pl(xrange(256)))
        self.conn_mat.img_plot('imagedata', name='connmatplot', colormap=cm)
        self.conn_mat.tools.append(ZoomTool(self.conn_mat))
        self.conn_mat.tools.append(PanTool(self.conn_mat))
        self.xa = ColorfulAxis(self.conn_mat, self.ds.node_colors, 'x')
        self.ya = ColorfulAxis(self.conn_mat, self.ds.node_colors, 'y')
        self.conn_mat.underlays = [self.xa, self.ya]

    def draw_surfs(self):
        NotImplemented

    def draw_nodes(self):
        mat = self.ds.scalar_display_settings.connmat
        if self.ds.display_mode == 'scalar' and mat:
            scalars = self.ds.node_scalars[mat]
            scalars = (scalars - np.min(scalars)) / (np.max(scalars) - np.min(scalars))
            colors = list(self.ds.opts.scalar_map._pl(scalars))
        else:
            colors = self.ds.node_colors
        self.xa.colors = colors
        self.ya.colors = colors
        self.conn_mat.request_redraw()

    def draw_conns(self, new_edges=None):
        NotImplemented

    def center(self):
        for ax in (self.xa, self.ya):
            ax.mapper.range.high_setting = self.ds.nr_labels
            ax.mapper.range.low_setting = 0

    def change_colormap(self):
        self.conn_mat.color_mapper = ColorMapper.from_palette_array(self.ds.opts.connmat_map._pl(xrange(256)))
        self.conn_mat.request_redraw()

    def snapshot(self, params):
        gc = PlotGraphicsContext(self.conn_mat.outer_bounds, dpi=params.dpi)
        gc.render_component(self.conn_mat)
        gc.save(params.savefile)


class DVCircle(DataView):
    circ = Any
    circ_data = List
    node_angles = Any
    tooltip_labnam = Property

    def _get_tooltip_labnam(self):
        if self.ds.opts.circ_bilateral_symmetry:
            if self.ds.labnam[0][0] == 'l':
                hemi_pivot = self.ds.lhnodes.size
                return self.ds.labnam[:hemi_pivot] + self.ds.labnam[:hemi_pivot - 1:-1]
            else:
                hemi_pivot = self.ds.rhnodes.size
                return self.ds.labnam[hemi_pivot:] + self.ds.labnam[hemi_pivot - 1::-1]

        else:
            if starthemi == 'l':
                return self.ds.labnam
            else:
                hemi_pivot = self.ds.rhnodes.size
                return self.ds.labnam[hemi_pivot:] + self.ds.labnam[:hemi_pivot]

    def __init__(self, ds, **kwargs):
        super(DVCircle, self).__init__(ds, **kwargs)
        if self.ds.adj is None:
            self.empty_gen()
        elif self.ds.opts.circle_render == 'disabled':
            self.empty_gen()
        else:
            self.circ_gen()
        return

    def supply_adj(self, **kwargs):
        if not self.ds.opts.circle_render == 'disabled':
            self.circ_gen(figure=self.circ, **kwargs)

    def circ_gen(self, reqrois=(), figure=None, suppress_extra_rois=False):
        if figure is not None:
            figure.clf()
        try:
            self.circ, self.node_angles = circle_plot.plot_connectivity_circle_cvu(np.reshape(self.ds.adjdat, (self.ds.nr_edges,)), self.ds.node_labels_numberless, indices=self.ds.edges.T, colormap=self.ds.opts.activation_map, fig=figure, n_lines=self.ds.nr_edges, node_colors=self.ds.node_colors, reqrois=reqrois, suppress_extra_rois=suppress_extra_rois, bilateral_symmetry=self.ds.opts.circ_bilateral_symmetry)
        except CVUError as e:
            self.ds.error_dialog(str(e))

        self.circ_data = self.circ.get_axes()[0].patches
        self.draw_nodes()
        return

    def empty_gen(self, figure=None):
        self.circ, self.node_angles = circle_plot.plot_connectivity_circle_cvu(np.array(()), self.ds.node_labels_numberless, indices=np.array(((), ())), colormap=self.ds.opts.activation_map, fig=figure, n_lines=None, node_colors=self.ds.node_colors, reqrois=(), bilateral_symmetry=self.ds.opts.circ_bilateral_symmetry)
        self.circ_data = self.circ.get_axes()[0].patches
        return

    def draw_surfs(self):
        NotImplemented

    def draw_nodes(self):
        circ = self.ds.scalar_display_settings.circle
        if self.ds.display_mode == 'scalar' and circ:
            scalars = self.ds.node_scalars[circ]
            scalars = (scalars - np.min(scalars)) / (np.max(scalars) - np.min(scalars))
            colors = list(self.ds.opts.scalar_map._pl(scalars))
        else:
            colors = self.ds.node_colors
        if self.ds.opts.circ_bilateral_symmetry:
            starthemi = self.ds.labnam[0][0]
            hemi_pivot = self.ds.lhnodes.size if starthemi == 'l' else self.ds.rhnodes.size
            colors = colors[:hemi_pivot] + colors[:hemi_pivot - 1:-1]
        if len(self.circ_data) == self.ds.nr_labels:
            circ_path_offset = 0
        else:
            circ_path_offset = len(self.ds.adjdat)
        for n in xrange(self.ds.nr_labels):
            self.circ_data[(circ_path_offset + n)].set_fc(colors[n])

        self.circ.canvas.draw()

    def draw_conns(self, new_edges=None):
        self.circ.canvas.draw()

    def circle_click(self, event):
        if event.button == 3:
            self.ds.display_all()
        elif event.button == 1 and 7 <= event.ydata <= 8:
            n = np.argmin(np.abs(event.xdata - self.node_angles % (np.pi * 2)))
            real_labelnr = self.ds.labnam.index(self.tooltip_labnam[n])
            self.ds.display_node(real_labelnr)

    def circle_mouseover(self, event, update_tooltip):
        if 7 <= event.ydata <= 8:
            n = np.argmin(np.abs(event.xdata - self.node_angles % (np.pi * 2)))
            update_tooltip(True, text=self.tooltip_labnam[int(np.floor(n))])
        else:
            update_tooltip(False)

    def snapshot(self, params):
        self.circ.savefig(params.savefile, dpi=params.dpi, facecolor=self.circ.get_facecolor())