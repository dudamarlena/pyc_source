# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/_population.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 3012 bytes
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
    day = 0
    day: int
    date = None
    date: _date

    @property
    def population(self) -> int:
        """The total population in all wards"""
        return self.susceptibles + self.total + self.recovereds

    @property
    def infecteds(self) -> int:
        """The number who are infected across all wards"""
        return self.total + self.latent

    def __str__(self):
        s = f"DAY: {self.day} S: {self.susceptibles}    E: {self.latent}    I: {self.total}    R: {self.recovereds}    IW: {self.n_inf_wards}   TOTAL POPULATION {self.population}"
        if self.date:
            return f"{self.date.isoformat()}: {s}"
        return s


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