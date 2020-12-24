# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/models/insitu_mixture.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 9931 bytes
raise NotImplemented('This module is not yet implemented')
import sys, imp
from contextlib import contextmanager
import numpy as np
from pyxrd.generic.io.custom_io import storables
from pyxrd.mixture.models.mixture import Mixture
from copy import deepcopy

@storables.register()
class InSituMixture(Mixture):
    __doc__ = '\n        Advanced model for optimizing and refining of calculated in-situ XRD data.\n        Is a sub-class of the basic Mixture class.\n        \n        Each phase is linked with an additional Behaviour instance - these are created at the\n        project level.\n    '

    class Meta(Mixture.Meta):
        store_id = 'InSituMixture'

    _data_object = None

    @property
    def data_object(self):
        self._data_object = Mixture.data_object.fget(self)
        return self._data_object

    def get_phase_data_object(self, specimen_index, z_index, phase_index):
        behav = self.behaviour_matrix[(specimen_index, ...)].flatten()[phase_index] if self.behaviour_matrix is not None else None
        phase = self.phase_matrix[(specimen_index, ...)].flatten()[phase_index] if self.phase_matrix is not None else None
        if behav is not None:
            if phase is not None:
                behav.apply(phase, self.specimens[specimen_index].get_z_list()[z_index])
        if phase is not None:
            return deepcopy(phase.data_object)

    behaviour_matrix = None

    def __init__(self, *args, **kwargs):
        my_kwargs = (self.pop_kwargs)(kwargs, 'behaviour_uuids', *[prop.label for prop in InSituMixture.Meta.get_local_persistent_properties()])
        (super(InSituMixture, self).__init__)(*args, **kwargs)
        kwargs = my_kwargs
        with self.data_changed.hold():
            behaviour_uuids = self.get_kwarg(kwargs, None, 'behaviour_uuids')
            if behaviour_uuids is not None:
                self.behaviour_matrix = np.array([[type(type(self)).object_pool.get_object(uuid) if uuid else None for uuid in row] for row in behaviour_uuids], dtype=(np.object_))
            else:
                self.behaviour_matrix = np.empty(shape=(0, 0), dtype=(np.object_))
            print(behaviour_uuids, self.behaviour_matrix)

    def json_properties(self):
        retval = super(InSituMixture, self).json_properties()
        retval['behaviour_uuids'] = [[item.uuid if item else None for item in row] for row in map(list, self.behaviour_matrix)]
        return retval

    @staticmethod
    def from_json(**kwargs):
        if 'refinables' in kwargs:
            del kwargs['refinables']
        return InSituMixture(**kwargs)

    def get_behaviour(self, specimen_slot, phase_slot):
        """Returns the behaviour at the given slot positions or None if not set"""
        return self.behaviour_matrix[(specimen_slot, phase_slot)]

    def set_behaviour(self, specimen_slot, phase_slot, behaviour):
        """Sets the behaviour at the given slot positions"""
        if self.parent is not None:
            with self.needs_update.hold_and_emit():
                with self.data_changed.hold():
                    if behaviour is None:
                        raise RuntimeError('Behaviour can not be set to None, use unset_behaviour to clear!')
                    self.behaviour_matrix[(specimen_slot, phase_slot)] = behaviour
                    self.refinement.update_refinement_treestore()

    def unset_behaviour(self, behaviour):
        """ Clears a behaviour slot in the phase matrix """
        with self.needs_update.hold_and_emit():
            with self.data_changed.hold():
                shape = self.behaviour_matrix.shape
                for i in range(shape[0]):
                    for j in range(shape[1]):
                        if self.behaviour_matrix[(i, j)] == behaviour:
                            self.behaviour_matrix[(i, j)] = None

                self.refinement.update_refinement_treestore()

    @contextmanager
    def _relieve_and_observe_behaviours(self):
        self._relieve_behaviours()
        yield
        self._observe_behaviours()

    def _observe_behaviours(self):
        """ Starts observing behaviour in the behaviour matrix"""
        for behaviour in self.behaviour_matrix.flat:
            if behaviour is not None:
                self.observe_model(behaviour)

    def _relieve_behaviours(self):
        """ Relieves behaviour observer calls """
        for behaviour in self.behaviour_matrix.flat:
            if behaviour is not None:
                self.relieve_model(behaviour)

    def add_phase_slot(self, phase_name, fraction):
        with self.needs_update.hold_and_emit():
            with self.data_changed.hold():
                n, m = self.behaviour_matrix.shape if self.behaviour_matrix.ndim == 2 else (0,
                                                                                            0)
                if self.behaviour_matrix.size == 0:
                    self.behaviour_matrix = np.resize(self.behaviour_matrix.copy(), (n, m + 1))
                    self.behaviour_matrix[:] = None
                else:
                    self.behaviour_matrix = np.concatenate([self.behaviour_matrix.copy(), [[None]] * n], axis=1)
                    self.behaviour_matrix[:, m] = None
                return super(InSituMixture, self).add_phase_slot(phase_name, fraction)

    def del_phase_slot(self, phase_slot):
        with self.needs_update.hold_and_emit():
            with self.data_changed.hold():
                with self._relieve_and_observe_behaviours():
                    self.behaviour_matrix = np.delete((self.behaviour_matrix), phase_slot, axis=1)
                return super(InSituMixture, self).del_phase_slot(phase_slot)

    def add_specimen_slot(self, specimen, scale, bgs):
        with self.needs_update.hold_and_emit():
            with self.data_changed.hold():
                n, m = self.behaviour_matrix.shape if self.behaviour_matrix.ndim == 2 else (0,
                                                                                            0)
                if self.behaviour_matrix.size == 0:
                    self.behaviour_matrix = np.resize(self.behaviour_matrix.copy(), (n + 1, m))
                    self.behaviour_matrix[:] = None
                else:
                    self.behaviour_matrix = np.concatenate([self.behaviour_matrix.copy(), [[None] * m]], axis=0)
                    self.behaviour_matrix[n, :] = None
                return super(InSituMixture, self).add_specimen_slot(specimen, scale, bgs)

    def del_specimen_slot(self, specimen_slot):
        with self.needs_update.hold_and_emit():
            with self.data_changed.hold():
                self.behaviour_matrix = np.delete((self.behaviour_matrix), specimen_slot, axis=0)
                return super(InSituMixture, self).del_specimen_slot(specimen_slot)

    def set_data_object(self, mixture, calculate=False):
        """
            Sets the fractions, scales and bgshifts of this mixture.
        """
        if mixture is not None:
            with self.needs_update.ignore():
                with self.data_changed.hold_and_emit():
                    self.fractions[:] = list(mixture.fractions)
                    self.scales[:] = list(mixture.scales)
                    self.bgshifts[:] = list(mixture.bgshifts)
                    if calculate:
                        mixture = self.optimizer.calculate(mixture)
                    for i, (specimen_data, specimen) in enumerate(zip(mixture.specimens, self.specimens)):
                        if specimen is not None:
                            with specimen.data_changed.ignore():
                                specimen.update_pattern(specimen_data.total_intensity, specimen_data.phase_intensities * self.fractions[:, np.newaxis] * self.scales[i], self.phase_matrix[i, :])

    def load_behaviour_from_module(self, path):
        """Loads the behaviour class from the given filepath"""
        mod = imp.load_source('Behaviour', path)
        del sys.modules['Behaviour']
        sys.modules[mod.BEHAVIOUR_CLASS] = mod
        klass = mod[mod.BEHAVIOUR_CLASS]
        behaviour = klass()
        behaviour._InSituMixture__path = path
        return behaviour