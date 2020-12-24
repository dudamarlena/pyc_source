# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/views/edit_insitu_behaviour_view.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1394 bytes
from pkg_resources import resource_filename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pyxrd.generic.views import BaseView

class EditInSituBehaviourView(BaseView):
    builder = resource_filename(__name__, 'glade/edit_insitu_behaviour.glade')
    top = 'edit_insitu_behaviour'
    widget_format = 'behaviour_%s'
    parameter_table = 'edit_insitu_behaviour'

    def __init__(self, meta, **kwargs):
        assert meta is not None, "EditInSituBehaviourView needs a model's Meta class!"
        (BaseView.__init__)(self, **kwargs)
        self.props = [prop for prop in meta.all_properties if getattr(prop, 'visible', False)]

        def create_label(prop):
            new_lbl = Gtk.Label(label=(prop.text))
            new_lbl.set_use_markup(True)
            return new_lbl

        def create_input(prop):
            new_inp = self.add_widget(prop)
            new_inp.set_name(self.widget_format % prop.label)
            return new_inp

        self.create_input_table((self[self.parameter_table]),
          (self.props), num_columns=1,
          widget_callbacks=[
         create_label,
         create_input])