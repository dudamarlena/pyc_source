# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ielu/utils.py
# Compiled at: 2016-03-02 14:09:44
import numpy as np, os
from traits.api import HasTraits, Str, Color, List, Instance, Int, Method, on_trait_change, Color, Any, Enum, Button, Float, File, Bool, Range, Event
from traitsui.api import View, Item, HGroup, Handler, CSVListEditor, InstanceEditor, Group, OKCancelButtons, TableEditor, ObjectColumn, TextEditor, OKButton, CheckListEditor, OKCancelButtons, Label, Action, VSplit, HSplit, VGroup
from traitsui.message import error as error_dialog
from functools import partial
from mayavi import mlab

class SortingLabelingError(Exception):
    pass


def virtual_points3d(coords, figure=None, scale_factor=None, color=None, name=None):
    c = np.array(coords)
    source = mlab.pipeline.scalar_scatter(c[:, 0], c[:, 1], c[:, 2], figure=figure)
    return mlab.pipeline.glyph(source, scale_mode='none', scale_factor=scale_factor, mode='sphere', figure=figure, color=color, name=name)


def intize(tuple_of_floats):
    return tuple(map(int, map(lambda x: x * 10000.0, map(partial(round, ndigits=4), tuple_of_floats))))


def clear_scene(scene):
    pass


def get_subjects_dir(subjects_dir=None, subject=None):
    if subjects_dir is None or subjects_dir == '':
        subjects_dir = os.environ['SUBJECTS_DIR']
    if subject is None or subject == '':
        subject = os.environ['SUBJECT']
    return os.path.join(subjects_dir, subject)


def _count():
    i = 0
    while True:
        yield i
        i += 1


_counter = _count()

def gensym():
    global _counter
    return _counter.next()


def crash_if_freesurfer_is_not_sourced():
    import os, subprocess
    with open(os.devnull, 'w') as (nil):
        p = subprocess.call(['which', 'mri_info'], stdout=nil)
    if p != 0:
        print 'Freesurfer is not sourced or not in the subshell path'
        import sys
        print os.environ['PATH']
        sys.exit(1)


def ask_user_for_savefile(title=None):
    from pyface.api import FileDialog, OK
    dialog = FileDialog(action='save as')
    if title is not None:
        dialog.title = title
    dialog.open()
    if dialog.return_code != OK:
        return
    else:
        return os.path.join(dialog.directory, dialog.filename)


def ask_user_for_loadfile(title=None):
    from pyface.api import FileDialog, OK
    dialog = FileDialog(action='open')
    if title is not None:
        dialog.title = title
    dialog.open()
    if dialog.return_code != OK:
        return
    else:
        return os.path.join(dialog.directory, dialog.filename)


def get_default_color_scheme():
    predefined_colors = [(0.2, 0.5, 0.8),
     (0.6, 0.3, 0.9),
     (0.8, 0.5, 0.9),
     (1, 0.2, 0.5),
     (0.7, 0.7, 0.9),
     (0.36, 0.58, 0.04),
     (0.22, 0.94, 0.64),
     (1, 0.6, 0.2),
     (0.5, 0.9, 0.4),
     (0, 0.6, 0.8)]
    for color in predefined_colors:
        yield color

    while True:
        yield tuple(np.random.random(3))


class AddLabelsWindow(Handler):
    model = Any
    annotation = Str
    label = File
    add_annot_button = Button('Add annotation')
    add_label_button = Button('Add label file')
    annot_borders = Bool
    annot_opacity = Range(0.0, 1.0, 1.0)
    annot_hemi = Enum('both', 'lh', 'rh')
    label_borders = Bool
    label_opacity = Range(0.0, 1.0, 1.0)
    label_color = Color('blue')
    remove_labels_action = Action(name='Remove all labels', action='do_remove')

    def _add_annot_button_fired(self):
        self.model.add_annotation(self.annotation, border=self.annot_borders, hemi=self.annot_hemi, opacity=self.annot_opacity)

    def _add_label_button_fired(self):
        self.model.add_label(self.label, border=self.label_borders, opacity=self.label_opacity, color=self.label_color)

    def do_remove(self, info):
        self.model.remove_labels()

    traits_view = View(HSplit(VGroup(Item('annotation'), Item('annot_borders', label='show border only'), Item('annot_opacity', label='opacity'), Item('annot_hemi', label='hemi'), Item('add_annot_button', show_label=False)), VGroup(Item('label'), Item('label_borders', label='show_border_only'), Item('label_opacity', label='opacity'), Item('label_color', label='color'), Item('add_label_button', show_label=False))), buttons=[
     remove_labels_action, OKButton], kind='livemodal', title='Dial 1-800-COLLECT and save a buck or two')