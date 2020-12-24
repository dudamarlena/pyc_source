# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/utils.py
# Compiled at: 2014-06-11 17:08:50
from traits.api import HasTraits, Any, Property, List, Str
from traitsui.api import View, Item

class CVUError(Exception):
    pass


class DisplayMetadata(HasTraits):
    subject_name = Str
    parc_name = Str
    adj_filename = Str
    traits_view = View(Item('subject_name', style='readonly'), Item('parc_name', style='readonly'), Item('adj_filename', style='readonly', width=250, height=5))


class DatasetMetadataElement(HasTraits):
    _controller = Any
    all_datasets = Property(depends_on='_controller:datasets')

    def _get_all_datasets(self):
        return self._controller.ds_instances.values()

    _current_dataset_list = List
    current_dataset = Property(depends_on='_current_dataset_list')

    def _get_current_dataset(self):
        try:
            return self._current_dataset_list[0]
        except IndexError:
            return

        return

    def __init__(self, controller, dataset=None, **kwargs):
        super(DatasetMetadataElement, self).__init__(**kwargs)
        self._controller = controller
        if dataset == None:
            self._current_dataset_list = [
             controller.ds_orig]
        else:
            self._current_dataset_list = [
             dataset]
        return


def file_chooser(**kwargs):
    from Tkinter import Tk
    Tk().withdraw()
    from tkFileDialog import askopenfilename
    return askopenfilename(**kwargs)


def fancy_file_chooser(main_window):
    from traits.api import HasPrivateTraits, File, Str, on_trait_change
    from traitsui.api import View, Item, FileEditor, OKCancelButtons

    class FileChooserWindow(HasPrivateTraits):
        f = File
        _fn = Str
        traits_view = View(Item(name='_fn', show_label=False), Item(name='f', editor=FileEditor(), style='custom', height=500, width=500, show_label=False), buttons=OKCancelButtons, kind='nonmodal', title='This should be extremely inconvenient')

        @on_trait_change('_fn')
        def f_chg(self):
            self.f = self._fn

    main_window.file_chooser_window = FileChooserWindow()
    main_window.file_chooser_window.edit_traits()