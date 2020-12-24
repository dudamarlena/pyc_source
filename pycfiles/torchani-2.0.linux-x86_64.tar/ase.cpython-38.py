# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/torchani/ase.py
# Compiled at: 2020-04-29 02:37:56
# Size of source mod 2**32: 3905 bytes
"""Tools for interfacing with `ASE`_.

.. _ASE:
    https://wiki.fysik.dtu.dk/ase
"""
import torch
from . import utils
import ase.calculators.calculator, ase.units

class Calculator(ase.calculators.calculator.Calculator):
    __doc__ = 'TorchANI calculator for ASE\n\n    Arguments:\n        species (:class:`collections.abc.Sequence` of :class:`str`):\n            sequence of all supported species, in order.\n        model (:class:`torch.nn.Module`): neural network potential model\n            that convert coordinates into energies.\n        overwrite (bool): After wrapping atoms into central box, whether\n            to replace the original positions stored in :class:`ase.Atoms`\n            object with the wrapped positions.\n    '
    implemented_properties = [
     'energy', 'forces', 'stress', 'free_energy']

    def __init__(self, species, model, overwrite=False):
        super(Calculator, self).__init__()
        self.species_to_tensor = utils.ChemicalSymbolsToInts(species)
        self.model = model
        self.overwrite = overwrite
        a_parameter = next(self.model.parameters())
        self.device = a_parameter.device
        self.dtype = a_parameter.dtype
        try:
            self.periodic_table_index = model.periodic_table_index
        except AttributeError:
            self.periodic_table_index = False

    def calculate(self, atoms=None, properties=['energy'], system_changes=ase.calculators.calculator.all_changes):
        super(Calculator, self).calculate(atoms, properties, system_changes)
        cell = torch.tensor(self.atoms.get_cell(complete=True), dtype=(self.dtype),
          device=(self.device))
        pbc = torch.tensor((self.atoms.get_pbc()), dtype=(torch.bool), device=(self.device))
        pbc_enabled = pbc.any().item()
        if self.periodic_table_index:
            species = torch.tensor((self.atoms.get_atomic_numbers()), dtype=(torch.long), device=(self.device))
        else:
            species = self.species_to_tensor(self.atoms.get_chemical_symbols()).to(self.device)
        species = species.unsqueeze(0)
        coordinates = torch.tensor(self.atoms.get_positions())
        coordinates = coordinates.to(self.device).to(self.dtype).requires_grad_('forces' in properties)
        if pbc_enabled:
            coordinates = utils.map2central(cell, coordinates, pbc)
            if self.overwrite:
                if atoms is not None:
                    atoms.set_positions(coordinates.detach().cpu().reshape(-1, 3).numpy())
        if 'stress' in properties:
            scaling = torch.eye(3, requires_grad=True, dtype=(self.dtype), device=(self.device))
            coordinates = coordinates @ scaling
        else:
            coordinates = coordinates.unsqueeze(0)
            if pbc_enabled:
                if 'stress' in properties:
                    cell = cell @ scaling
                energy = self.model((species, coordinates), cell=cell, pbc=pbc).energies
            else:
                energy = self.model((species, coordinates)).energies
        energy *= ase.units.Hartree
        self.results['energy'] = energy.item()
        self.results['free_energy'] = energy.item()
        if 'forces' in properties:
            forces = -torch.autograd.grad((energy.squeeze()), coordinates, retain_graph=('stress' in properties))[0]
            self.results['forces'] = forces.squeeze(0).to('cpu').numpy()
        if 'stress' in properties:
            volume = self.atoms.get_volume()
            stress = torch.autograd.grad(energy.squeeze(), scaling)[0] / volume
            self.results['stress'] = stress.cpu().numpy()