# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/options_struct.py
# Compiled at: 2015-07-03 22:24:23
from traits.api import HasTraits, Instance, Int, Range, Bool, Float, Property, Enum, Str, List, Either, Directory, Any, File, on_trait_change, cached_property
from color_map import CustomColormap
from color_legend import ColorLegend
from graph import StatisticsDisplay
import os, numpy as np

class OptionsDatabase(HasTraits):

    def __init__(self, ds_orig, **kwargs):
        super(OptionsDatabase, self).__init__(**kwargs)
        self.parcellation_chooser_parameters = ParcellationChooserParameters(ds_orig)
        self.adjmat_chooser_parameters = AdjmatChooserParameters(ds_orig)
        self.tractography_chooser_parameters = TractographyChooserParameters(ds_orig)
        self.general_matrix_chooser_parameters = GeneralMatrixChooserParameters(ds_orig)
        self.node_chooser_parameters = NodeChooserParameters(ds_orig)
        self.calculate_parameters = CalculateParameters(ds_orig)
        self.module_chooser_parameters = ModuleChooserParameters(ds_orig)
        self.module_customizer_parameters = ModuleCustomizerParameters(ds_orig)
        self.color_legend_parameters = ColorLegendParameters(ds_orig)
        self.snapshot_parameters = SnapshotParameters(ds_orig)
        self.make_movie_parameters = MakeMovieParameters(ds_orig)
        self.graph_theory_parameters = GraphTheoryParameters(ds_orig)


class DatasetReferenceOptionsStructure(HasTraits):
    ds_ref = Any

    def __init__(self, ds_ref, **kwargs):
        super(DatasetReferenceOptionsStructure, self).__init__(**kwargs)
        self.ds_ref = ds_ref


class DisplayOptions(DatasetReferenceOptionsStructure):
    surface_visibility = Range(0.0, 1.0, 0.15)
    circ_size = Range(7, 20, 10, mode='spinner')
    circ_symmetry = Enum('bilateral', 'radial')
    circ_bilateral_symmetry = Property(depends_on='circ_symmetry')

    def _get_circ_bilateral_symmetry(self):
        return self.circ_symmetry == 'bilateral'

    conns_colorbar = Bool(False)
    scalar_colorbar = Bool(False)
    pthresh = Range(0.0, 1.0, 0.95)
    athresh = Float
    thresh_type = Enum('prop', 'abs')
    prune_modules = Bool(True)
    show_floating_text = Bool(True)
    module_view_style = Enum('intramodular', 'intermodular', 'both')
    modules_on_surface = Bool(False)
    render_style = Enum('glass', 'cracked_glass', 'contours', 'wireframe', 'speckled')
    interhemi_conns_on = Bool(True)
    lh_conns_on = Bool(True)
    rh_conns_on = Bool(True)
    lh_nodes_on = Bool(True)
    rh_nodes_on = Bool(True)
    lh_surfs_on = Bool(True)
    rh_surfs_on = Bool(True)
    conns_width = Float(2.0)
    tube_conns = Bool(False)
    circle_render = Enum('singlethreaded', 'asynchronous', 'disabled')
    conns_colors_on = Bool(True)
    default_map = Instance(CustomColormap)

    def _default_map_default(self):
        return CustomColormap('default')

    scalar_map = Instance(CustomColormap)

    def _scalar_map_default(self):
        return CustomColormap('scalar')

    activation_map = Instance(CustomColormap)

    def _activation_map_default(self):
        return CustomColormap('activation')

    connmat_map = Instance(CustomColormap)

    def _connmat_map_default(self):
        return CustomColormap('connmat')

    intermediate_graphopts_list = List(Str)

    def _intermediate_graphopts_list_default(self):
        return [
         'global efficiency', 'clustering coefficient',
         'average strength', 'eigenvector centrality', 'binary kcore']


class ScalarDisplaySettings(DatasetReferenceOptionsStructure):
    node_color = Either(Str, None)
    surf_color = Either(Str, None)
    node_size = Either(Str, None)
    circle = Either(Str, None)
    connmat = Either(Str, None)
    scalar_sets = Property(List(Either(Str, None)))

    def _get_scalar_sets(self):
        return [
         None] + self.ds_ref.node_scalars.keys()

    def reset_configuration(self):
        self.node_color = ''
        self.surf_color = ''
        self.node_size = ''
        self.circle = ''
        self.connmat = ''


class ParcellationChooserParameters(DatasetReferenceOptionsStructure):
    new_dataset = Bool(False)
    new_dataset_name = Str
    subjects_dir = Directory('./')
    subject = Str('fsavg5')
    ordering_file = File
    surface_type = Str('pial')
    parcellation_type = Enum('surface', 'volume file', 'coordinates file')
    parcellation_name = Str
    parcellation_volume = File
    volume_ordering = File
    parcellation_coords = File
    registration_matrix = File


class AdjmatChooserParameters(DatasetReferenceOptionsStructure):
    adjmat = Either(File, np.ndarray, np.matrix)
    adjmat_order = Either(File, None, list)
    max_edges = Int
    field_name = Either(Str, None)
    ignore_deletes = Bool
    require_ls = List(Str)
    suppress_extra_rois = Bool

    def _adjmat_default(self):
        return ''

    def _adjmat_order_default(self):
        return ''


class TractographyChooserParameters(DatasetReferenceOptionsStructure):
    track_file = File
    b0_volume = File
    subjects_dir = Directory
    subject = Str
    fs_setup = File('/usr/local/freesurfer/nmr-stable53-env')


class GeneralMatrixChooserParameters(DatasetReferenceOptionsStructure):
    mat = File
    mat_order = File
    field_name = Str
    ignore_deletes = Bool
    whichkind = Enum('modules', 'scalars')
    measure_nr = Int(1)
    measure_name = Property(Str)
    measure_has_custom_name = Bool(False)
    measure_custom_name = Str

    def _get_measure_name(self):
        if self.measure_has_custom_name:
            return self.measure_custom_name
        return 'scalars%i' % self.measure_nr

    def _set_measure_name(self, new_val):
        self.measure_has_custom_name = True
        self.measure_custom_name = new_val

    def _increment_scalar_count(self):
        self.measure_nr += 1
        self.measure_has_custom_name = False


class NodeChooserParameters(DatasetReferenceOptionsStructure):
    cur_node = Int(-1)
    node_list = Property(List(Str))

    def _get_node_list(self):
        return self.ds_ref.labnam


class CalculateParameters(DatasetReferenceOptionsStructure):
    calculation_type = Enum('modules', 'statistics')
    athresh = Float
    pthresh = Range(0.0, 1.0, 0.8)
    thresh_type = Enum('prop', 'abs')


class ModuleChooserParameters(DatasetReferenceOptionsStructure):
    cur_mod = Int(-1)
    module_list = Property(List(Str), depends_on='ds_ref.modules')

    @cached_property
    def _get_module_list(self):
        return [ 'Module %i' % i for i, m in enumerate(self.ds_ref.modules) ]


class ModuleCustomizerParameters(DatasetReferenceOptionsStructure):
    initial_node_list = Property(List(Str))

    def _get_initial_node_list(self):
        return self.ds_ref.labnam

    intermediate_node_list = List(Str)
    return_module = List(Int)

    def _index_convert(self):
        self.return_module = [ self.initial_node_list.index(i) for i in self.intermediate_node_list
                             ]


class ColorLegendParameters(DatasetReferenceOptionsStructure):
    skaabbl = Str('skaabll')
    legend = Property(Instance(ColorLegend))

    def _get_legend(self):
        return self.ds_ref.color_legend


class SnapshotParameters(DatasetReferenceOptionsStructure):
    savefile = Str(os.path.expanduser('~'))
    whichplot = Enum('3D brain', 'connection matrix', 'circle plot')
    dpi = Int(300)


class MakeMovieParameters(DatasetReferenceOptionsStructure):
    savefile = Str(os.path.expanduser('~'))
    framerate = Int(20)
    bitrate = Int(4000)
    samplerate = Int(8)
    anim_style = Bool(True)
    anim_rate = Int(8)
    rotate_deg = Int(10)
    debug = Bool(False)


class GraphTheoryParameters(DatasetReferenceOptionsStructure):
    from traitsui.api import View, Item, ListEditor
    graph_stats = Property(List(StatisticsDisplay), depends_on='ds_ref:graph_stats')
    current_stat = Instance(StatisticsDisplay)
    scalar_savename = File

    @cached_property
    def _get_graph_stats(self):
        return list(StatisticsDisplay(k, v, self.ds_ref.labnam) for k, v in self.ds_ref.graph_stats.iteritems())

    def _current_stat_changed(self):
        self.scalar_savename = self.current_stat.name

    def _proc_export_to_scalar(self):
        from traitsui.file_dialog import save_file
        filename = save_file()
        if filename.endswith('.mat'):
            from scipy import io
            io.savemat(filename, mdict={self.current_stat.name: self.current_stat.stat})
        elif filename.endswith('.npy'):
            np.save(filename, self.current_stat.stat)
        else:
            np.savetxt(filename, self.current_stat.stat)

    def _proc_save_to_scalar(self):
        self.ds_ref.save_scalar(self.scalar_savename, self.current_stat.stat)

    def _proc_recalculate(self):
        self.ds_ref.calculate_graph_stats()

    old_traitsui_view = View(Item(name='graph_stats', style='custom', editor=ListEditor(use_notebook=True, page_name='.name', selected='current_stat'), show_label=False))