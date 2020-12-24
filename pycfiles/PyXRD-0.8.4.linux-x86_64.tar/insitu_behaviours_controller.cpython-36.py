# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/controllers/insitu_behaviours_controller.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2854 bytes
from contextlib import contextmanager
from mvc.models.base import Model
from pyxrd.generic.controllers import ObjectListStoreController
from pyxrd.mixture.models import InSituBehaviour, insitu_behaviours
from pyxrd.mixture.views import EditInSituBehaviourView
from pyxrd.mixture.views.add_insitu_behaviour_view import AddInSituBehaviourView
from .edit_insitu_behaviour_controller import EditInSituBehaviourController
from .add_insitu_behaviour_controller import AddInSituBehaviourController

class InSituBehavioursController(ObjectListStoreController):
    treemodel_property_name = 'behaviours'
    treemodel_class_type = InSituBehaviour
    columns = [('Mixture name', 'c_name')]
    delete_msg = 'Deleting a mixture is irreverisble!\nAre You sure you want to continue?'
    obj_type_map = [(cls, EditInSituBehaviourView, EditInSituBehaviourController) for name, cls in list(insitu_behaviours.__dict__.items()) if hasattr(cls, 'Meta') if cls.Meta.concrete]

    def get_behaviours_tree_model(self, *args):
        return self.treemodel

    def on_load_object_clicked(self, event):
        pass

    def on_save_object_clicked(self, event):
        pass

    def get_new_edit_view(self, obj):
        """
            Gets a new 'edit object' view for the given obj, view and parent
            view.
        """
        if obj == None:
            return self.view.none_view
        for obj_tp, view_tp, ctrl_tp in self.obj_type_map:
            if isinstance(obj, obj_tp):
                return view_tp((obj.Meta), parent=(self.view))

        raise NotImplementedError('Unsupported object type; subclasses of TreeControllerMixin need to define an obj_type_map attribute!')

    def create_new_object_proxy(self):

        def on_accept(behaviour_type):
            if behaviour_type is not None:
                self.add_object(behaviour_type(parent=(self.model)))

        self.add_model = Model()
        self.add_view = AddInSituBehaviourView(parent=(self.view))
        self.add_ctrl = AddInSituBehaviourController(model=(self.add_model),
          view=(self.add_view),
          parent=self,
          callback=on_accept)
        self.add_view.present()

    @contextmanager
    def _multi_operation_context(self):
        with self.model.data_changed.hold():
            yield