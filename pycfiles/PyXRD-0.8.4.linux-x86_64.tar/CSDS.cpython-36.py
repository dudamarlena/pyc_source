# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/phases/models/CSDS.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 8225 bytes
from pyxrd.data import settings
from pyxrd.calculations.CSDS import calculate_distribution
from pyxrd.calculations.data_objects import CSDSData
from pyxrd.generic.models import DataModel
from pyxrd.generic.io import storables, Storable
from pyxrd.refinement.refinables.mixins import RefinementGroup, RefinementValue
from pyxrd.refinement.refinables.metaclasses import PyXRDRefinableMeta
from pyxrd.refinement.refinables.properties import DataMixin, RefinableMixin
from mvc.models.properties import GetActionMixin, LabeledProperty, BoolProperty, FloatProperty, ReadOnlyMixin, SetActionMixin
from mvc.models.properties.signal_mixin import SignalMixin

class _AbstractCSDSDistribution(DataModel, Storable, metaclass=PyXRDRefinableMeta):

    class Meta(DataModel.Meta):
        description = 'Abstract CSDS distr.'
        explanation = ''

    phase = property(DataModel.parent.fget, DataModel.parent.fset)
    _data_object = None

    @property
    def data_object(self):
        return self._data_object

    inherited = BoolProperty(default=False,
      text='Inherited',
      visible=False,
      persistent=False,
      signal_name='data_changed',
      mix_with=(SignalMixin,))
    distrib = LabeledProperty(default=None,
      text='CSDS Distribution',
      tabular=True,
      visible=False,
      persistent=False,
      get_action_name='_update_distribution',
      signal_name='data_changed',
      mix_with=(
     SignalMixin, GetActionMixin))
    maximum = FloatProperty(default=0.0,
      text='Maximum CSDS',
      minimum=1,
      maximum=1000,
      tabular=True,
      persistent=False,
      visible=False,
      mix_with=(
     ReadOnlyMixin, DataMixin))
    minimum = FloatProperty(default=0.0,
      text='Maximum CSDS',
      minimum=1,
      maximum=1000,
      tabular=True,
      persistent=False,
      visible=False,
      mix_with=(
     ReadOnlyMixin, DataMixin))
    average = FloatProperty(default=0.0,
      text='Average CSDS',
      minimum=1,
      maximum=200,
      tabular=True,
      persistent=True,
      visible=True,
      refinable=True,
      signal_name='data_changed',
      set_action_name='_update_distribution',
      mix_with=(
     SignalMixin, DataMixin, RefinableMixin, SetActionMixin))
    alpha_scale = FloatProperty(default=0.0,
      text='α scale factor',
      minimum=0.0,
      maximum=10.0,
      tabular=True,
      persistent=True,
      visible=True,
      refinable=True,
      signal_name='data_changed',
      set_action_name='_update_distribution',
      mix_with=(
     SignalMixin, DataMixin, RefinableMixin, SetActionMixin))
    alpha_offset = FloatProperty(default=0.0,
      text='α offset factor',
      minimum=(-5),
      maximum=5,
      tabular=True,
      persistent=True,
      visible=True,
      refinable=True,
      signal_name='data_changed',
      set_action_name='_update_distribution',
      mix_with=(
     SignalMixin, DataMixin, RefinableMixin, SetActionMixin))
    beta_scale = FloatProperty(default=0.0,
      text='β² scale factor',
      minimum=0.0,
      maximum=10.0,
      tabular=True,
      persistent=True,
      visible=True,
      refinable=True,
      signal_name='data_changed',
      set_action_name='_update_distribution',
      mix_with=(
     SignalMixin, DataMixin, RefinableMixin, SetActionMixin))
    beta_offset = FloatProperty(default=0.0,
      text='β² offset factor',
      minimum=(-5),
      maximum=5,
      tabular=True,
      persistent=True,
      visible=True,
      refinable=True,
      signal_name='data_changed',
      set_action_name='_update_distribution',
      mix_with=(
     SignalMixin, DataMixin, RefinableMixin, SetActionMixin))

    def __init__(self, average=10, alpha_scale=0.9485, alpha_offset=-0.0017, beta_scale=0.1032, beta_offset=0.0034, *args, **kwargs):
        (super(_AbstractCSDSDistribution, self).__init__)(*args, **kwargs)
        self._data_object = CSDSData()
        type(self).average._set(self, average)
        type(self).maximum._set(self, int(settings.LOG_NORMAL_MAX_CSDS_FACTOR * average))
        type(self).minimum._set(self, 1)
        type(self).alpha_scale._set(self, alpha_scale)
        type(self).alpha_offset._set(self, alpha_offset)
        type(self).beta_scale._set(self, beta_scale)
        type(self).beta_offset._set(self, beta_offset)
        self._update_distribution()

    def _update_distribution(self):
        type(self).maximum._set(self, int(settings.LOG_NORMAL_MAX_CSDS_FACTOR * self.average))
        self._distrib = calculate_distribution(self.data_object)


@storables.register()
class LogNormalCSDSDistribution(_AbstractCSDSDistribution, RefinementGroup):

    class Meta(_AbstractCSDSDistribution.Meta):
        description = 'Generic log-normal CSDS distr. (Eberl et al. 1990)'
        store_id = 'LogNormalCSDSDistribution'

    @property
    def refine_title(self):
        return 'CSDS Distribution'

    @property
    def refine_descriptor_data(self):
        return dict(phase_name=(self.phase.name),
          component_name='*')


@storables.register()
class DritsCSDSDistribution(_AbstractCSDSDistribution, RefinementValue):

    class Meta(_AbstractCSDSDistribution.Meta):
        description = 'Log-normal CSDS distr. (Drits et. al, 1997)'
        store_id = 'DritsCSDSDistribution'

    alpha_scale = FloatProperty(default=0.9485,
      text='α scale factor',
      minimum=0.0,
      maximum=10.0,
      tabular=True,
      persistent=False,
      visible=False,
      refinable=False,
      mix_with=(
     ReadOnlyMixin, DataMixin, RefinableMixin))
    alpha_offset = FloatProperty(default=0.017,
      text='α offset factor',
      minimum=(-5),
      maximum=5,
      tabular=True,
      persistent=False,
      visible=False,
      refinable=False,
      mix_with=(
     ReadOnlyMixin, DataMixin, RefinableMixin))
    beta_scale = FloatProperty(default=0.1032,
      text='β² scale factor',
      minimum=0.0,
      maximum=10.0,
      tabular=True,
      persistent=False,
      visible=False,
      refinable=False,
      mix_with=(
     ReadOnlyMixin, DataMixin, RefinableMixin))
    beta_offset = FloatProperty(default=0.0034,
      text='β² offset factor',
      minimum=(-5),
      maximum=5,
      tabular=True,
      persistent=False,
      visible=False,
      refinable=False,
      mix_with=(
     ReadOnlyMixin, DataMixin, RefinableMixin))

    @property
    def refine_title(self):
        return 'Average CSDS'

    @property
    def refine_descriptor_data(self):
        return dict(phase_name=(self.phase.name),
          component_name='*',
          property_name=(self.refine_title))

    @property
    def refine_value(self):
        return self.average

    @refine_value.setter
    def refine_value(self, value):
        self.average = value

    @property
    def refine_info(self):
        return self.average_ref_info

    @property
    def is_refinable(self):
        return not self.inherited

    def __init__(self, *args, **kwargs):
        for key in ('alpha_scale', 'alpha_offset', 'beta_scale', 'beta_offset'):
            kwargs.pop(key, None)

        (super(DritsCSDSDistribution, self).__init__)(*args, **kwargs)


CSDS_distribution_types = [
 LogNormalCSDSDistribution,
 DritsCSDSDistribution]