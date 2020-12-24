# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/gui.py
# Compiled at: 2015-07-04 00:19:35
import os, sys, numpy as np
from traits.api import HasTraits, List, Instance, Dict, Button, Str, Bool, Property, on_trait_change
from traitsui.api import ButtonEditor, ShellEditor, View, Item, Spring, HSplit, VSplit, Group, InstanceEditor
from dataset import Dataset
from controller import Controller
from utils import DisplayMetadata
import dialogs
from threading import Thread
from viewport import Viewport, DatasetViewportInterface
from traits.api import Event

class ErrorHandler(HasTraits):
    quiet = Bool

    def __init__(self, quiet=False, **kwargs):
        super(ErrorHandler, self).__init__(**kwargs)
        self.quiet = quiet

    def error_dialog(self, message, collect_stacktrace=False):
        sys.stderr.write('%s\n' % message)

    def warning_dialog(self, message):
        sys.stderr.write('%s\n' % message)

    def verbose_msg(self, message):
        if not self.quiet:
            print message


class CvuGUI(ErrorHandler, DatasetViewportInterface):
    controller = Instance(Controller)

    def _mayavi_port_default(self):
        return Viewport(self.controller.ds_orig, view_type='3D Brain')

    def _matrix_port_default(self):
        return Viewport(self.controller.ds_orig, view_type='Connection Matrix')

    def _circle_port_default(self):
        return Viewport(self.controller.ds_orig, view_type='Circular plot')

    options_window = Instance(dialogs.InteractiveSubwindow)
    adjmat_chooser_window = Instance(dialogs.InteractiveSubwindow)
    parcellation_chooser_window = Instance(dialogs.InteractiveSubwindow)
    tractography_chooser_window = Instance(dialogs.InteractiveSubwindow)
    node_chooser_window = Instance(dialogs.InteractiveSubwindow)
    module_chooser_window = Instance(dialogs.InteractiveSubwindow)
    module_customizer_window = Instance(dialogs.InteractiveSubwindow)
    graph_theory_window = Instance(dialogs.InteractiveSubwindow)
    configure_scalars_window = Instance(dialogs.InteractiveSubwindow)
    save_snapshot_window = Instance(dialogs.InteractiveSubwindow)
    make_movie_window = Instance(dialogs.InteractiveSubwindow)
    really_overwrite_file_window = Instance(dialogs.InteractiveSubwindow)
    calculate_window = Instance(dialogs.InteractiveSubwindow)
    color_legend_window = Instance(dialogs.InteractiveSubwindow)
    load_standalone_matrix_window = Instance(dialogs.InteractiveSubwindow)
    select_node_button = Button('Choose node')
    display_all_button = Button('Reset Displays')
    graph_theory_button = Button('Show statistics')
    calculate_button = Button('Calculate stats')
    select_module_button = Button('View module')
    custom_module_button = Button('Custom subset')
    display_scalars_button = Button('Show scalars')
    load_standalone_button = Button('Load stats')
    load_adjmat_button = Button('Load an adjacency matrix')
    color_legend_button = Button('Color legend')
    load_parcellation_button = Button('Load a parcellation')
    options_button = Button('Options')
    controller_button = Button('Manage views')
    load_tractography_button = Button('Load tractography')
    save_snapshot_button = Button('Take snapshot')
    make_movie_button = Button
    currently_making_movie = Bool(False)
    mk_movie_lbl = Property(depends_on='currently_making_movie')

    def _get_mk_movie_lbl(self):
        if self.currently_making_movie:
            return 'Stop movie'
        return 'Make movie'

    about_button = Button('About')
    manage_views_button = Button('Manage views')
    python_shell = Dict
    traits_view = View(VSplit(HSplit(Item(name='mayavi_port', height=500, width=500, editor=InstanceEditor(view='mayavi_view'), show_label=False, style='custom', resizable=True), Item(name='matrix_port', height=500, width=500, editor=InstanceEditor(view='matrix_view'), show_label=False, style='custom', resizable=True), Group(Spring(), Item(name='select_node_button'), Item(name='display_all_button'), Item(name='color_legend_button'), Spring(), Item(name='calculate_button'), Item(name='load_standalone_button'), Item(name='graph_theory_button'), Item(name='display_scalars_button'), Item(name='select_module_button'), Item(name='custom_module_button'), Spring(), show_labels=False)), HSplit(Item(name='circle_port', height=500, width=500, editor=InstanceEditor(view='circle_view'), show_label=False, style='custom', resizable=True), Group(HSplit(Item(name='load_parcellation_button'), Item(name='load_adjmat_button'), Item(name='load_tractography_button'), show_labels=False), HSplit(Item(name='save_snapshot_button'), Item(name='make_movie_button', editor=ButtonEditor(label_value='mk_movie_lbl')), Item(name='options_button'), Item(name='controller_button'), Item(name='about_button'), show_labels=False), HSplit(Item(name='python_shell', editor=ShellEditor(), height=450, show_label=False))))), resizable=True, title='Connectome Visualization Utility')

    def __init__(self, sample_data, sample_metadata, quiet=False, **kwargs):
        super(HasTraits, self).__init__(quiet=quiet, **kwargs)
        ctrl = self.controller = Controller(self, sample_data, sample_metadata)
        ds_orig = self.controller.ds_orig
        self.error_dialog_window = dialogs.ErrorDialogWindow()
        self.warning_dialog_window = dialogs.WarningDialogWindow()
        self.about_window = dialogs.AboutWindow()
        self.really_overwrite_file_window = dialogs.ReallyOverwriteFileWindow()
        self.options_window = dialogs.OptionsWindow(ds_orig.opts, ctrl)
        self.configure_scalars_window = dialogs.ConfigureScalarsWindow(ds_orig.scalar_display_settings, ctrl)
        self.calculate_window = dialogs.CalculateWindow(ctrl.options_db.calculate_parameters, ctrl)
        self.adjmat_chooser_window = dialogs.AdjmatChooserWindow(ctrl.options_db.adjmat_chooser_parameters, ctrl)
        self.parcellation_chooser_window = dialogs.ParcellationChooserWindow(ctrl.options_db.parcellation_chooser_parameters, ctrl)
        self.tractography_chooser_window = dialogs.TractographyChooserWindow(ctrl.options_db.tractography_chooser_parameters, ctrl)
        self.load_standalone_matrix_window = dialogs.LoadGeneralMatrixWindow(ctrl.options_db.general_matrix_chooser_parameters, ctrl)
        self.node_chooser_window = dialogs.NodeChooserWindow(ctrl.options_db.node_chooser_parameters, ctrl)
        self.module_chooser_window = dialogs.ModuleChooserWindow(ctrl.options_db.module_chooser_parameters, ctrl)
        self.module_customizer_window = dialogs.ModuleCustomizerWindow(ctrl.options_db.module_customizer_parameters, ctrl)
        self.graph_theory_window = dialogs.GraphTheoryWindow(ctrl.options_db.graph_theory_parameters, ctrl)
        self.color_legend_window = dialogs.ColorLegendWindow(ctrl.options_db.color_legend_parameters, ctrl)
        self.save_snapshot_window = dialogs.SaveSnapshotWindow(ctrl.options_db.snapshot_parameters, ctrl)
        self.make_movie_window = dialogs.MakeMovieWindow(ctrl.options_db.make_movie_parameters, ctrl)
        self.panel_name = 'base_gui'

    def error_dialog(self, message):
        self.error_dialog_window.stacktrace = None
        _, _, tb = sys.exc_info()
        if tb is not None:
            self.error_dialog_window.stacktrace = tb
        self.error_dialog_window.error = message
        self.error_dialog_window.edit_traits()
        return

    def warning_dialog(self, message):
        self.warning_dialog_window.warning = message
        self.warning_dialog_window.edit_traits()

    def reset_controls(self, ds_match):
        for window in (self.load_standalone_matrix_window,
         self.adjmat_chooser_window, self.node_chooser_window,
         self.parcellation_chooser_window, self.module_chooser_window,
         self.module_customizer_window, self.graph_theory_window,
         self.save_snapshot_window, self.make_movie_window,
         self.calculate_window, self.color_legend_window,
         self.configure_scalars_window, self.options_window):
            if window.ctl.ds_ref is ds_match or window.ctl.ds_ref is None:
                window._current_dataset_list = [
                 self.controller.ds_orig]

        return

    def _display_all_button_fired(self):
        for ds in self.controller.ds_instances.values():
            ds.display_all()

    def _options_button_fired(self):
        self.options_window.finished = False
        self.options_window.edit_traits()

    def _load_parcellation_button_fired(self):
        self.parcellation_chooser_window.finished = False
        self.parcellation_chooser_window.edit_traits()

    @on_trait_change('parcellation_chooser_window:notify')
    def _load_parcellation_check(self):
        pcw = self.parcellation_chooser_window
        if not pcw.finished:
            return
        if pcw.ctl.new_dataset:
            if pcw.ctl.new_dataset_name == '':
                self.error_dialog('Must specify a dataset name!')
                return
            if pcw.ctl.new_dataset_name in self.controller.ds_instances:
                self.error_dialog('Dataset name is not unique')
                return
            ds_name = pcw.ctl.new_dataset_name
            import preprocessing
            parc_struct = preprocessing.process_parc(pcw.ctl, self)
            if parc_struct is None:
                return
            lab_pos, labnam, srf, labv, subject_name, parc_name = parc_struct
            display_metadata = DisplayMetadata(subject_name=subject_name, parc_name=parc_name, adj_filename='')
            ds = Dataset(ds_name, lab_pos, labnam, srf, labv, gui=self)
            self.controller.add_dataset(ds, display_metadata)
        else:
            import preprocessing
            parc_struct = preprocessing.process_parc(pcw.ctl, self)
            if parc_struct is None:
                return
            lab_pos, labnam, srf, labv, subject_name, parc_name = parc_struct
            pcw.ctl.ds_ref._load_parc(lab_pos, labnam, srf, labv)
            self.controller.update_display_metadata(pcw.ctl.ds_ref.name, subject_name=subject_name, parc_name=parc_name)
            ds_interface = self.controller.find_dataset_views(pcw.ctl.ds_ref)
            ds_interface.mayavi_port = Viewport(pcw.ctl.ds_ref)
            ds_interface.matrix_port = Viewport(pcw.ctl.ds_ref)
            ds_interface.circle_port = Viewport(pcw.ctl.ds_ref)
        return

    def _load_adjmat_button_fired(self):
        self.adjmat_chooser_window.finished = False
        self.adjmat_chooser_window.edit_traits()

    @on_trait_change('adjmat_chooser_window:notify')
    def _load_adjmat_check(self):
        acw = self.adjmat_chooser_window
        if not acw.finished:
            return
        else:
            import preprocessing as pp
            adj_struct = pp.process_adj(acw.ctl, self)
            if adj_struct is None:
                return
            adj, soft_max_edges, adj_filename = adj_struct
            acw.ctl.ds_ref._load_adj(adj, soft_max_edges, acw.ctl.require_ls, acw.ctl.suppress_extra_rois)
            self.controller.update_display_metadata(acw.ctl.ds_ref.name, adj_filename=adj_filename)
            return

    def _load_tractography_button_fired(self):
        self.tractography_chooser_window.finished = False
        self.tractography_chooser_window.edit_traits()

    @on_trait_change('tractography_chooser_window:notify')
    def _load_tractography_check(self):
        tcw = self.tractography_chooser_window
        if not tcw.finished:
            return
        tcw.ctl.ds_ref.load_tractography(tcw.ctl)

    def _load_standalone_button_fired(self):
        self.load_standalone_matrix_window.finished = False
        self.load_standalone_matrix_window.edit_traits()

    @on_trait_change('load_standalone_matrix_window:notify')
    def _load_standalone_check(self):
        lsmw = self.load_standalone_matrix_window
        if not lsmw.finished:
            return
        lsmw.ctl.ds_ref.load_modules_or_scalars(lsmw.ctl)

    def _display_scalars_button_fired(self):
        csw = self.configure_scalars_window
        csw.finished = False
        self.configure_scalars_window.edit_traits()

    @on_trait_change('configure_scalars_window:notify')
    def _display_scalars_check(self):
        csw = self.configure_scalars_window
        if not csw.finished or not any((csw.ctl.node_color, csw.ctl.surf_color,
         csw.ctl.node_size, csw.ctl.circle, csw.ctl.connmat)):
            return
        csw.ctl.ds_ref.display_scalars()

    def _select_node_button_fired(self):
        self.node_chooser_window.finished = False
        self.node_chooser_window.edit_traits()

    @on_trait_change('node_chooser_window:notify')
    def _select_node_check(self):
        ncw = self.node_chooser_window
        if not ncw.finished:
            return
        ncw.ctl.ds_ref.display_node(ncw.ctl.cur_node)

    def _calculate_button_fired(self):
        cw = self.calculate_window
        cw.finished = False
        cw.edit_traits()

    @on_trait_change('calculate_window:notify')
    def _calculation_check(self):
        cw = self.calculate_window
        if not cw.finished:
            return
        else:
            if cw.ctl.ds_ref.adj is None:
                self.error_dialog('There is no adjacency matrix loaded')
                return
            if cw.ctl.thresh_type == 'abs':
                thres = cw.ctl.athresh
            elif cw.ctl.thresh_type == 'prop':
                if cw.ctl.pthresh == 0.0:
                    thres = -np.inf
                else:
                    thres = cw.ctl.ds_ref.adjdat[int(round(cw.ctl.pthresh * cw.ctl.ds_ref.nr_edges - 1))]
            if cw.ctl.calculation_type == 'modules':
                cw.ctl.ds_ref.calculate_modules(thres)
                cw.ctl.ds_ref.display_multi_module()
            elif cw.ctl.calculation_type == 'statistics':
                Thread(target=cw.ctl.ds_ref.calculate_graph_stats, args=(thres,)).start()
            return

    def _select_module_button_fired(self):
        self.module_chooser_window.finished = False
        self.module_chooser_window.edit_traits()

    @on_trait_change('module_chooser_window:notify')
    def _select_module_check(self):
        mcw = self.module_chooser_window
        if not mcw.finished or mcw.ctl.cur_mod == -1:
            return
        mcw.ctl.ds_ref.display_module(mcw.ctl.cur_mod)

    def _custom_module_button_fired(self):
        self.module_customizer_window.finished = False
        self.module_customizer_window.edit_traits()

    @on_trait_change('module_customizer_window:notify')
    def _module_customizer_check(self):
        mcw = self.module_customizer_window
        if not mcw.finished:
            return
        try:
            mcw.ctl._index_convert()
        except ValueError:
            self.error_dialog('Internal error: bad index conversion')
            return

        mcw.ctl.ds_ref.custom_module = mcw.ctl.return_module
        mcw.ctl.ds_ref.display_module('custom')

    def _graph_theory_button_fired(self):
        self.graph_theory_window.finished = False
        self.graph_theory_window.edit_traits()

    def _color_legend_button_fired(self):
        self.color_legend_window.edit_traits()

    def _save_snapshot_button_fired(self):
        self.save_snapshot_window.finished = False
        self.save_snapshot_window.edit_traits()

    @on_trait_change('save_snapshot_window:notify')
    def _save_snapshot_check(self):
        ssw = self.save_snapshot_window
        if not ssw.finished:
            return
        save_continuation = ssw.ctl.ds_ref.snapshot(ssw.ctl)
        self.process_save_continuation(ssw.ctl.savefile, save_continuation)

    def _make_movie_button_fired(self):
        if not self.currently_making_movie:
            self.make_movie_window.finished = False
            self.make_movie_window.edit_traits()
        else:
            self.currently_making_movie = False
            mmw = self.make_movie_window
            mmw.ctl.ds_ref.make_movie_finish(mmw.ctl)

    @on_trait_change('make_movie_window:notify')
    def make_movie_check(self):
        mmw = self.make_movie_window
        if not mmw.finished:
            return
        movie_continuation = mmw.ctl.ds_ref.make_movie(mmw.ctl)

        def save_continuation():
            self.currently_making_movie = True
            movie_continuation()

        self.process_save_continuation(mmw.ctl.savefile, save_continuation)

    @on_trait_change('really_overwrite_file_window:notify')
    def _really_overwrite_file_check(self):
        rofw = self.really_overwrite_file_window
        if rofw.finished:
            rofw.save_continuation()

    def process_save_continuation(self, filename, save_continuation):
        if not filename:
            self.error_dialog('No save file specified')
            return
        if not os.path.exists(os.path.dirname(filename)):
            self.error_dialog('Bad save file specified. Check for typos.')
            return
        if not os.path.exists(filename):
            save_continuation()
        else:
            rofw = self.really_overwrite_file_window
            rofw.save_continuation = save_continuation
            rofw.finished = False
            rofw.edit_traits()

    def _controller_button_fired(self):
        self.controller.viewport_manager.edit_traits()

    def _about_button_fired(self):
        self.about_window.edit_traits()