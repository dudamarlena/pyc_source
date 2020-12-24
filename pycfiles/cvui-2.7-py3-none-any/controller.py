# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/controller.py
# Compiled at: 2015-05-05 12:37:20
from traits.api import HasTraits, Any, List, Str, Enum, Dict, Instance, Either, Property, Button, on_trait_change
from traitsui.api import Item, Handler, View, ButtonEditor, InstanceEditor, TextEditor
from options_struct import OptionsDatabase
from utils import DatasetMetadataElement, CVUError, DisplayMetadata
from viewport import ViewPanel

class ViewportManagerEntry(HasTraits):
    window_name = Str
    window_group = Enum('1', '2')
    all_datasets = List


class ViewportManager(Handler):
    from traitsui.api import Item, View, ObjectColumn, TableEditor, RangeEditor, CheckListEditor, OKButton
    ctl = Any
    selected_col = Any

    def __init__(self, ctl, **kwargs):
        super(Handler, self).__init__(**kwargs)
        self.ctl = ctl

    traits_view = View(Item(name='metadata_list', object='object.ctl', editor=TableEditor(columns=[
     ObjectColumn(label='Window', name='panel_scratch', editor=TextEditor(enter_set=True, auto_set=False)),
     ObjectColumn(label='Dataset', name='ds_name_scratch', editor=TextEditor(enter_set=True, auto_set=False))], edit_view='tabular_view'), show_label=False, height=200, width=700), kind='nonmodal', buttons=[OKButton], title='If it were up to me it would all be in Swahili')


class DatasetUIMetadata(DatasetMetadataElement):
    controller = Any
    panel, panel_scratch = 2 * (Str,)
    ds_name, ds_name_scratch = 2 * (Str,)
    display_metadata = Instance(DisplayMetadata)
    rebuild_button = Button
    rebuild_label = Property(Str)

    def _get_rebuild_label(self):
        return 'Rebuild %s' % self.panel

    delete_button = Button
    delete_label = Property(Str)

    def _get_delete_label(self):
        return 'Delete %s' % self.ds_name

    def __init__(self, controller, panel, name, display_metadata, **kwargs):
        self.panel = self.panel_scratch = panel
        self.ds_name = self.ds_name_scratch = name
        super(DatasetUIMetadata, self).__init__(controller, **kwargs)
        self.controller = controller
        self.display_metadata = display_metadata

    def _rebuild_button_fired(self):
        if self.panel == 'base_gui':
            self.controller.error_dialog('Rebuilding the base GUI is not allowed')
            return
        self.controller.rebuild_panel(self.panel)

    def _delete_button_fired(self):
        if self.controller.ds_instances[self.ds_name] is self.controller.ds_orig:
            self.controller.error_dialog('Removal of the sample data is not allowed')
            return
        self.controller.remove_dataset(self.ds_name)

    @on_trait_change('panel_scratch')
    def _rename_panel(self):
        if self.panel == 'base_gui':
            self.controller.warning_dialog('Renaming the base gui window is not allowed')
            return
        old_name = self.controller.panel_instances[self.panel].panel_name
        new_name = self.panel_scratch
        self.controller.rename_panel(old_name, new_name)
        self.panel = self.panel_scratch

    @on_trait_change('ds_name_scratch')
    def _rename_ds(self):
        old_name = self.controller.ds_instances[self.ds_name].name
        new_name = self.ds_name_scratch
        self.controller.rename_dataset(old_name, new_name)
        self.ds_name = self.ds_name_scratch

    tabular_view = View(Item(name='rebuild_button', editor=ButtonEditor(label_value='rebuild_label'), show_label=False), Item(name='delete_button', editor=ButtonEditor(label_value='delete_label'), show_label=False), Item(name='display_metadata', style='custom', show_label=False, editor=InstanceEditor()))


class Controller(HasTraits):
    gui = Any
    options_db = Instance(OptionsDatabase)
    ds_orig = Any
    ds_instances = Dict
    ds_metadatae = Dict
    panel_instances = Dict
    panel_metadatae = Dict
    metadata_list = Property(List)

    def _get_metadata_list(self):
        return self.ds_metadatae.values()

    viewport_manager = Instance(ViewportManager)

    def __init__(self, gui, sample_data, sample_metadata):
        super(Controller, self).__init__()
        self.gui = gui
        self.ds_orig = sample_data
        ds_meta = DatasetUIMetadata(self, 'base_gui', sample_data.name, sample_metadata)
        self.ds_instances = {sample_data.name: sample_data}
        self.panel_instances = {'base_gui': self.gui}
        self.ds_metadatae = {sample_data.name: ds_meta}
        self.panel_metadatae = {'base_gui': ds_meta}
        self.options_db = OptionsDatabase(sample_data)
        self.viewport_manager = ViewportManager(self)

    @on_trait_change('gui:options_window:current_dataset')
    def options_window_ctl_listener(self):
        self.gui.options_window.ctl = self.gui.options_window.current_dataset.opts

    @on_trait_change('gui:configure_scalars_window:current_dataset')
    def configure_scalars_window_ctl_listener(self):
        csw = self.gui.configure_scalars_window
        csw.ctl = csw.current_dataset.scalar_display_settings

    def add_dataset(self, ds, display_metadata, panel=None, group=None):
        """Given a dataset, add it to the controller.  If panel and group
           are specified, add it to that panel, otherwise any panel will do"""
        if ds.name in self.ds_instances:
            raise CVUError('A dataset with this name already exists')
        if panel is None and group is None:
            panel_ref = self._create_new_panel(ds.name)
            panel = panel_ref.panel_name
            group = 2 if panel_ref.is_full(group=1) else 1
        elif group is not None:
            raise CVUError('Cannot specify group without panel')
        elif panel is not None:
            panel_ref = self.get_named_panel(panel)
            if panel_ref.is_full():
                raise CVUError('That panel is full')
            group = 2 if panel_ref.is_full(group=1) else 1
        else:
            panel_ref = self.get_named_panel(panel)
        panel_ref.populate(ds, group=group)
        ds_meta = DatasetUIMetadata(self, panel, ds.name, display_metadata)
        self.ds_instances.update({ds.name: ds})
        self.ds_metadatae.update({ds.name: ds_meta})
        self.panel_instances.update({panel_ref.panel_name: panel_ref})
        self.panel_metadatae.update({panel_ref.panel_name: ds_meta})
        self.show_panel(panel_ref)
        return

    def show_panel(self, panel):
        panel.edit_traits(panel.produce_view())

    def rebuild_panel(self, panel_name):
        """we havent actually destroyed the editor here.
            have to destroy the panel and create a new one.
            otherwise the panel still refers to the wrong editor"""
        panel = self.panel_instances[panel_name]
        panel.conditionally_dispose()
        ds = self._get_dataset_from_panel(panel)
        ds.reset_dataviews()
        panel.populate(ds, force=True)
        self.show_panel(panel)

    def rename_panel(self, old_name, new_name):
        try:
            panel = self.panel_instances[old_name]
            ds_meta = self.panel_metadatae[old_name]
        except KeyError:
            raise CVUError('No such panel')

        del self.panel_instances[old_name]
        del self.panel_metadatae[old_name]
        self.panel_instances.update({new_name: panel})
        self.panel_metadatae.update({new_name: ds_meta})
        panel.panel_name = new_name

    def rename_dataset(self, old_name, new_name):
        try:
            ds = self.ds_instances[old_name]
            ds_meta = self.ds_metadatae[old_name]
        except KeyError:
            raise CVUError('No such dataset')

        del self.ds_instances[old_name]
        del self.ds_metadatae[old_name]
        self.ds_instances.update({new_name: ds})
        self.ds_metadatae.update({new_name: ds_meta})
        ds.name = new_name

    def find_dataset_views(self, ds):
        """Given a dataset, return the three viewports that refer to it"""
        ds_meta = self.ds_metadatae[ds.name]
        panel = self.panel_instances[ds_meta.panel]
        from viewport import DatasetViewportInterface
        if isinstance(panel, DatasetViewportInterface):
            layout_obj = panel
        else:
            layout_obj = panel.group_1
        return layout_obj

    def update_display_metadata(self, ds_name, subject_name=None, parc_name=None, adj_filename=None):
        ds_meta = self.ds_metadatae[ds_name]
        if subject_name is not None:
            ds_meta.display_metadata.subject_name = subject_name
        if parc_name is not None:
            ds_meta.display_metadata.parc_name = parc_name
        if adj_filename is not None:
            ds_meta.display_metadata.adj_filename = adj_filename
        return

    def remove_dataset(self, ds_name):
        ds_meta = self.ds_metadatae[ds_name]
        panel_name = ds_meta.panel
        panel = self.panel_instances[panel_name]
        panel.conditionally_dispose()
        ds = self.ds_instances[ds_name]
        self.gui.reset_controls(ds)
        try:
            del self.ds_instances[ds_name]
            del self.ds_metadatae[ds_name]
            del self.panel_instances[panel_name]
            del self.panel_metadatae[panel_name]
        except KeyError as e:
            raise CVUError('Inconsistent metadata')

    def _get_named_panel(self, panel_name):
        try:
            return self.panel_instances[panel_name]
        except KeyError as e:
            raise CVUError('No such panel')

    def _get_dataset_from_panel(self, panel):
        ds_meta = self.panel_metadatae[panel.panel_name]
        return self._get_named_dataset(ds_meta.ds_name)

    def _get_named_dataset(self, ds_name):
        try:
            return self.ds_instances[ds_name]
        except KeyError as e:
            raise CVUError('No such dataset')

    def __ctr_generate():
        i = 0
        while True:
            i += 1
            yield i

    __ctr_generator = Any(__ctr_generate())

    def _panel_counter(self):
        return self.__ctr_generator.next()

    def _create_new_panel(self, ds_name):
        panel_name = 'Extra View %i' % self._panel_counter()
        panel = ViewPanel(panel_name=ds_name)
        self.panel_instances[ds_name] = panel
        return panel

    def _destroy_panel(self, name):
        del self.panel_instances[name]

    def error_dialog(self, message):
        return self.gui.error_dialog(message)

    def warning_dialog(self, message):
        return self.gui.warning_dialog(message)

    def verbose_msg(self, message):
        return self.gui.verbose_msg(message)