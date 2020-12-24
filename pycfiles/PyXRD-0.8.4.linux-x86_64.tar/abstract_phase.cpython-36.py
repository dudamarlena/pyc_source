# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/phases/models/abstract_phase.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 4417 bytes
import zipfile
from random import choice
from mvc.models.properties import StringProperty, SignalMixin, IntegerProperty, ReadOnlyMixin
from pyxrd.generic.io import storables, Storable, COMPRESSION
from pyxrd.generic.models import DataModel
from pyxrd.calculations.data_objects import PhaseData
from pyxrd.calculations.phases import get_diffracted_intensity
from pyxrd.file_parsers.json_parser import JSONParser

@storables.register()
class AbstractPhase(DataModel, Storable):

    class Meta(DataModel.Meta):
        store_id = 'AbstractPhase'

    _data_object = None

    @property
    def data_object(self):
        return self._data_object

    project = property(DataModel.parent.fget, DataModel.parent.fset)
    name = StringProperty(default='New Phase',
      text='Name',
      visible=True,
      persistent=True,
      tabular=True)

    @IntegerProperty(default=0,
      text='# of components',
      visible=True,
      persistent=True,
      tabular=True,
      widget_type='entry',
      mix_with=(
     ReadOnlyMixin,))
    def G(self):
        return 0

    @IntegerProperty(default=0,
      text='Reichweite',
      visible=True,
      persistent=False,
      tabular=True,
      widget_type='entry',
      mix_with=(
     ReadOnlyMixin,))
    def R(self):
        return 0

    display_color = StringProperty(default='#FFB600',
      text='Display color',
      visible=True,
      persistent=True,
      tabular=True,
      widget_type='color',
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    line_colors = [
     '#004488',
     '#FF4400',
     '#559911',
     '#770022',
     '#AACC00',
     '#441177']

    def __init__(self, *args, **kwargs):
        my_kwargs = (self.pop_kwargs)(kwargs, 'data_name', 'data_G', 'data_R', *[prop.label for prop in AbstractPhase.Meta.get_local_persistent_properties()])
        (super(AbstractPhase, self).__init__)(*args, **kwargs)
        kwargs = my_kwargs
        with self.data_changed.hold():
            self._data_object = PhaseData()
            self.name = self.get_kwarg(kwargs, self.name, 'name', 'data_name')
            self.display_color = self.get_kwarg(kwargs, choice(self.line_colors), 'display_color')

    def __repr__(self):
        return "AbstractPhase(name='%s')" % self.name

    def resolve_json_references(self):
        pass

    def _pre_multi_save(self, phases, ordered_phases):
        pass

    def _post_multi_save(self):
        pass

    @classmethod
    def save_phases(cls, phases, filename):
        """
            Saves multiple phases to a single file.
        """
        ordered_phases = list(phases)
        for phase in phases:
            phase._pre_multi_save(phases, ordered_phases)

        with zipfile.ZipFile(filename, 'w', compression=COMPRESSION) as (zfile):
            for i, phase in enumerate(ordered_phases):
                zfile.writestr('%d###%s' % (i, phase.uuid), phase.dump_object())

        for phase in ordered_phases:
            phase._post_multi_save()

        type(cls).object_pool.change_all_uuids()

    def get_diffracted_intensity(self, range_theta, range_stl, *args):
        return get_diffracted_intensity(range_theta, range_stl, self.data_object)