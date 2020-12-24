# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.7.5/x64/lib/python3.7/site-packages/nnp/md.py
# Compiled at: 2019-11-24 03:15:15
# Size of source mod 2**32: 2291 bytes
"""
Molecular Dynamics
==================

The module ``nnp.md`` provide tools to run molecular dynamics with a potential
defined by PyTorch.
"""
import torch
from torch import Tensor
from nnp import pbc
from typing import Callable, Sequence
import ase.calculators.calculator

class Calculator(ase.calculators.calculator.Calculator):
    __doc__ = 'ASE Calculator that wraps a neural network potential\n\n    Arguments:\n        func (callable): A fucntion that .\n        overwrite (bool): After wrapping atoms into central box, whether\n            to replace the original positions stored in :class:`ase.Atoms`\n            object with the wrapped positions.\n    '
    implemented_properties = [
     'energy', 'forces', 'stress', 'free_energy']

    def __init__(self, func, overwrite=False):
        super(Calculator, self).__init__()
        self.func = func
        self.overwrite = overwrite

    def calculate(self, atoms=None, properties=['energy'], system_changes=ase.calculators.calculator.all_changes):
        super(Calculator, self).calculate(atoms, properties, system_changes)
        coordinates = torch.from_numpy(self.atoms.get_positions()).requires_grad_('forces' in properties)
        cell = coordinates.new_tensor(self.atoms.get_cell(complete=True).array)
        pbc_ = torch.tensor((self.atoms.get_pbc()), dtype=(torch.bool))
        pbc_enabled = pbc_.any().item()
        if pbc_enabled:
            coordinates = pbc.map2central(cell, coordinates, pbc_)
        if 'stress' in properties:
            scaling = torch.eye(3, requires_grad=True)
            coordinates = coordinates @ scaling
            cell = cell @ scaling
        energy = self.func(atoms.get_chemical_symbols(), coordinates, cell, pbc_)
        self.results['energy'] = energy.item()
        self.results['free_energy'] = energy.item()
        if 'forces' in properties:
            forces = -torch.autograd.grad(energy, coordinates)[0]
            self.results['forces'] = forces.cpu().numpy()
        if 'stress' in properties:
            volume = self.atoms.get_volume()
            stress = torch.autograd.grad(energy, scaling)[0] / volume
            self.results['stress'] = stress.cpu().numpy()