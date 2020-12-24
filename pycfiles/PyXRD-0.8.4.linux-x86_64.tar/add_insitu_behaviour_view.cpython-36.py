# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/views/add_insitu_behaviour_view.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 859 bytes
from pkg_resources import resource_filename
from pyxrd.generic.views import DialogView

class AddInSituBehaviourView(DialogView):
    title = 'Add Behaviour'
    subview_builder = resource_filename(__name__, 'glade/add_behaviour.glade')
    subview_toplevel = 'add_behaviour_container'

    def __init__(self, *args, **kwargs):
        (DialogView.__init__)(self, *args, **kwargs)

    def get_behaviour_type(self):
        itr = self.behaviour_combo_box.get_active_iter()
        val = self.behaviour_combo_box.get_model().get_value(itr, 1) if itr else None
        return val

    @property
    def behaviour_combo_box(self):
        return self['cmb_behaviours']