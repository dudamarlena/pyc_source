# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/controllers/mixtures_controller.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2439 bytes
from contextlib import contextmanager
from mvc.models.base import Model
from pyxrd.generic.controllers import ObjectListStoreController
from pyxrd.mixture.models import Mixture
from pyxrd.mixture.views import EditMixtureView, AddMixtureView
from .edit_mixture_controller import EditMixtureController
from .add_mixture_controller import AddMixtureController

class MixturesController(ObjectListStoreController):
    treemodel_property_name = 'mixtures'
    treemodel_class_type = Mixture
    columns = [('Mixture name', 'c_name')]
    delete_msg = 'Deleting a mixture is irreverisble!\nAre You sure you want to continue?'
    obj_type_map = [
     (
      Mixture, EditMixtureView, EditMixtureController)]

    def get_mixtures_tree_model(self, *args):
        return self.treemodel

    def on_load_object_clicked(self, event):
        pass

    def on_save_object_clicked(self, event):
        pass

    def create_new_object_proxy(self):
        """def on_accept(mixture_type):
            if mixture_type == "mixture":
                self.add_object(Mixture(parent=self.model))
            #elif mixture_type == "insitu":
            #    self.add_object(InSituMixture(parent=self.model))
                
        # TODO re-use this and reset the COMBO etc.
        self.add_model = Model()
        self.add_view = AddMixtureView(types_dict={
            'mixture': "Create a regular mixture", 
            #'insitu': "Create an in-situ mixture"
        }, parent=self.view)
        self.add_ctrl = AddMixtureController(
            model=self.add_model, view=self.add_view, parent=self.parent,
            callback=on_accept
        )

        self.add_view.present()"""
        return Mixture(parent=(self.model))

    @contextmanager
    def _multi_operation_context(self):
        with self.model.data_changed.hold():
            yield