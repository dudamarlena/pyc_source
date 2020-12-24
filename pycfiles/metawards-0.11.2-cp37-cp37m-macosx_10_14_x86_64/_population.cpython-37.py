# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_population.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 6703 bytes
from dataclasses import dataclass as _dataclass
from typing import List as _List
from copy import deepcopy as _deepcopy
from datetime import date as _date
__all__ = [
 'Population', 'Populations']

@_dataclass
class Population:
    __doc__ = 'This class holds information about the progress of the\n       disease through the population\n    '
    initial = 0
    initial: int
    susceptibles = 0
    susceptibles: int
    latent = 0
    latent: int
    total = 0
    total: int
    recovereds = 0
    recovereds: int
    n_inf_wards = 0
    n_inf_wards: int
    scale_uv = 1.0
    scale_uv: float
    day = 0
    day: int
    date = None
    date: _date
    subpops = None

    @property
    def population(self) -> int:
        """The total population in all wards"""
        return self.susceptibles + self.latent + self.total + self.recovereds

    @property
    def infecteds(self) -> int:
        """The number who are infected across all wards"""
        return self.total + self.latent

    def specialise(self, network):
        """Specialise this population for the passed Networks"""
        subpops = []
        from copy import deepcopy
        self.subpops = None
        for i in range(0, len(network.subnets)):
            subpops.append(deepcopy(self))

        self.subpops = subpops

    def __str__(self):
        s = f"DAY: {self.day} S: {self.susceptibles}    E: {self.latent}    I: {self.total}    R: {self.recovereds}    IW: {self.n_inf_wards}   UV: {self.scale_uv}   TOTAL POPULATION {self.population}"
        if self.date:
            return f"{self.date.isoformat()}: {s}"
        return s

    def assert_sane(self):
        """Assert that this population is sane, i.e. the totals within
           this population and with the sub-populations all add up to
           the correct values
        """
        errors = []
        t = self.susceptibles + self.latent + self.total + self.recovereds
        if t != self.population:
            errors.append(f"Disagreement in total overall population: {t} versus {self.population}")
        if self.subpops is not None:
            if len(self.subpops) > 0:
                S = 0
                E = 0
                I = 0
                R = 0
                P = 0
                for subpop in self.subpops:
                    S += subpop.susceptibles
                    E += subpop.latent
                    I += subpop.infecteds
                    R += subpop.recovereds
                    P += subpop.population

                if S != self.susceptibles:
                    errors.append(f"Disagreement in S: {S} versus {self.susceptibles}")
                if E != self.latent:
                    errors.append(f"Disagreement in E: {E} versus {self.latent}")
                if I != self.infecteds:
                    errors.append(f"Disagreement in I: {I} versus {self.infecteds}")
                if R != self.recovereds:
                    errors.append(f"Disagreement in R: {R} versus {self.recovereds}")
                if P != self.population:
                    errors.append(f"Disagreement in Population: {P} versus {self.population}")
        if len(errors) > 0:
            errors = '\nERROR: '.join(errors)
            print(f"ERROR: {errors}")
            raise AssertionError('Disagreement in population sums!')

    def summary(self, demographics=None):
        """Return a short summary string that is suitable to be printed
           out during a model run

           Returns
           -------
           summary: str
             The short summary string
        """
        summary = f"S: {self.susceptibles}  E: {self.latent}  I: {self.total}  R: {self.recovereds}  IW: {self.n_inf_wards}  POPULATION: {self.population}"
        if self.subpops is None or len(self.subpops) == 0:
            return summary
        subs = []
        for i, subpop in enumerate(self.subpops):
            if demographics is not None:
                name = demographics.get_name(i)
                subs.append(f"{name}  {subpop.summary()}")
            else:
                subs.append(f"{i}  {subpop.summary()}")

        from utils._align_strings import align_strings
        subs = align_strings(subs, ':')
        return f"{summary}\n  " + '\n  '.join(subs)


@_dataclass
class Populations:
    __doc__ = 'This class holds the trajectory of Population objects recorded\n       for every step (day) of a model outbreak\n    '
    _trajectory = None
    _trajectory: _List[Population]

    def __str__(self):
        if len(self) == 0:
            return 'Populations:empty'
        return f"Latest: {self._trajectory[(-1)]}"

    def __getitem__(self, i: int):
        """Return the ith Population in the trajectory"""
        if self._trajectory is None:
            raise IndexError('No trajectory data collected')
        else:
            return self._trajectory[i]

    def __len__(self):
        if self._trajectory is None:
            return 0
        return len(self._trajectory)

    def strip_demographics(self):
        """Remove the demographics information from this trajectory. This
           makes it much smaller and easier to transmit over a network
        """
        for value in self._trajectory:
            value._subpops = None

        return self

    def append(self, population: Population):
        """Append the next step in the trajectory.

           Parameters
           ----------
           population: Population
             The population to append to this list
        """
        if not isinstance(population, Population):
            raise TypeError('Only Population objects should be recorded!')
        if self._trajectory is None:
            self._trajectory = []
        self._trajectory.append(_deepcopy(population))