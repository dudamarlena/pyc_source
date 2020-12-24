# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/models/insitu_behaviours/insitu_behaviour.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2477 bytes
from mvc.models.properties import StringProperty
from pyxrd.generic.io.custom_io import storables, Storable
from pyxrd.generic.models.base import DataModel
from pyxrd.refinement.refinables.mixins import RefinementGroup

@storables.register()
class InSituBehaviour(DataModel, RefinementGroup, Storable):
    __doc__ = '\n        Interface class for coding in-situ behaviour scripts.\n        Sub-classes should override or implement the methods below.\n    '

    class Meta(DataModel.Meta):
        store_id = 'InSituBehaviour'
        concrete = False

    mixture = property(DataModel.parent.fget, DataModel.parent.fset)

    @property
    def refine_title(self):
        return 'In-situ behaviour'

    @property
    def refine_descriptor_data(self):
        return dict(phase_name=(self.phase.refine_title),
          component_name='*')

    name = StringProperty(default='New Behaviour',
      text='Name',
      visible=True,
      persistent=True,
      tabular=True)

    def __init__(self, *args, **kwargs):
        my_kwargs = (self.pop_kwargs)(kwargs, *[prop.label for prop in InSituBehaviour.Meta.get_local_persistent_properties()])
        (super(InSituBehaviour, self).__init__)(*args, **kwargs)
        kwargs = my_kwargs
        with self.data_changed.hold():
            self.name = self.get_kwarg(kwargs, self.name, 'name')

    def apply(self, phase):
        if not phase is not None:
            raise AssertionError('Cannot apply on None')
        elif not self.is_compatible_with(phase):
            raise AssertionError('`%r` is not compatible with phase `%r`' % (self, phase))

    def is_compatible_with(self, phase):
        return False