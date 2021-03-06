# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.7.5/x64/lib/python3.7/site-packages/torchani/utils.py
# Compiled at: 2019-11-23 13:53:56
# Size of source mod 2**32: 12631 bytes
import torch
from torch import Tensor
import torch.utils.data, math, numpy as np
from collections import defaultdict
from typing import Tuple, NamedTuple, Optional
from .nn import SpeciesEnergies

def pad(species):
    """Put different species together into single tensor.

    If the species are from molecules of different number of total atoms, then
    ghost atoms with atom type -1 will be added to make it fit into the same
    shape.

    Arguments:
        species (:class:`collections.abc.Sequence`): sequence of species.
            Species must be of shape ``(N, A)``, where ``N`` is the number of
            3D structures, ``A`` is the number of atoms.

    Returns:
        :class:`torch.Tensor`: species batched together.
    """
    max_atoms = max([s.shape[1] for s in species])
    padded_species = []
    for s in species:
        natoms = s.shape[1]
        if natoms < max_atoms:
            padding = torch.full((s.shape[0], max_atoms - natoms), (-1), dtype=(torch.long),
              device=(s.device))
            s = torch.cat([s, padding], dim=1)
        padded_species.append(s)

    return torch.cat(padded_species)


def pad_atomic_properties(atomic_properties, padding_values=defaultdict((lambda : 0.0), species=(-1))):
    """Put a sequence of atomic properties together into single tensor.

    Inputs are `[{'species': ..., ...}, {'species': ..., ...}, ...]` and the outputs
    are `{'species': padded_tensor, ...}`

    Arguments:
        species_coordinates (:class:`collections.abc.Sequence`): sequence of
             atomic properties.
        padding_values (dict): the value to fill to pad tensors to same size
    """
    keys = list(atomic_properties[0])
    anykey = keys[0]
    max_atoms = max((x[anykey].shape[1] for x in atomic_properties))
    padded = {k:[] for k in keys}
    for p in atomic_properties:
        num_molecules = 1
        for v in p.values():
            assert num_molecules in {1, v.shape[0]}, 'Number of molecules in different atomic properties mismatch'
            if v.shape[0] != 1:
                num_molecules = v.shape[0]

        for k, v in p.items():
            shape = list(v.shape)
            padatoms = max_atoms - shape[1]
            shape[1] = padatoms
            padding = v.new_full(shape, padding_values[k])
            v = torch.cat([v, padding], dim=1)
            shape = list(v.shape)
            shape[0] = num_molecules
            v = (v.expand)(*shape)
            padded[k].append(v)

    return {k:torch.cat(v) for k, v in padded.items()}


def present_species(species):
    """Given a vector of species of atoms, compute the unique species present.

    Arguments:
        species (:class:`torch.Tensor`): 1D vector of shape ``(atoms,)``

    Returns:
        :class:`torch.Tensor`: 1D vector storing present atom types sorted.
    """
    present_species = species.flatten().unique(sorted=True)
    if present_species[0].item() == -1:
        present_species = present_species[1:]
    return present_species


def strip_redundant_padding(atomic_properties):
    """Strip trailing padding atoms.

    Arguments:
        atomic_properties (dict): properties to strip

    Returns:
        dict: same set of properties with redundant padding atoms stripped.
    """
    species = atomic_properties['species']
    non_padding = (species >= 0).any(dim=0).nonzero().squeeze()
    for k in atomic_properties:
        atomic_properties[k] = atomic_properties[k].index_select(1, non_padding)

    return atomic_properties


def map2central(cell, coordinates, pbc):
    """Map atoms outside the unit cell into the cell using PBC.

    Arguments:
        cell (:class:`torch.Tensor`): tensor of shape (3, 3) of the three
            vectors defining unit cell:

            .. code-block:: python

                tensor([[x1, y1, z1],
                        [x2, y2, z2],
                        [x3, y3, z3]])

        coordinates (:class:`torch.Tensor`): Tensor of shape
            ``(molecules, atoms, 3)``.

        pbc (:class:`torch.Tensor`): boolean vector of size 3 storing
            if pbc is enabled for that direction.

    Returns:
        :class:`torch.Tensor`: coordinates of atoms mapped back to unit cell.
    """
    inv_cell = torch.inverse(cell)
    coordinates_cell = torch.matmul(coordinates, inv_cell)
    coordinates_cell -= coordinates_cell.floor() * pbc.to(coordinates_cell.dtype)
    return torch.matmul(coordinates_cell, cell)


class EnergyShifter(torch.nn.Module):
    __doc__ = 'Helper class for adding and subtracting self atomic energies\n\n    This is a subclass of :class:`torch.nn.Module`, so it can be used directly\n    in a pipeline as ``[input->AEVComputer->ANIModel->EnergyShifter->output]``.\n\n    Arguments:\n        self_energies (:class:`collections.abc.Sequence`): Sequence of floating\n            numbers for the self energy of each atom type. The numbers should\n            be in order, i.e. ``self_energies[i]`` should be atom type ``i``.\n        fit_intercept (bool): Whether to calculate the intercept during the LSTSQ\n            fit. The intercept will also be taken into account to shift energies.\n    '

    def __init__(self, self_energies, fit_intercept=False):
        super(EnergyShifter, self).__init__()
        self.fit_intercept = fit_intercept
        if self_energies is not None:
            self_energies = torch.tensor(self_energies, dtype=(torch.double))
        self.register_buffer('self_energies', self_energies)

    def sae_from_dataset(self, atomic_properties, properties):
        """Compute atomic self energies from dataset.

        Least-squares solution to a linear equation is calculated to output
        ``self_energies`` when ``self_energies = None`` is passed to
        :class:`torchani.EnergyShifter`
        """
        species = atomic_properties['species']
        energies = properties['energies']
        present_species_ = present_species(species)
        X = (species.unsqueeze(-1) == present_species_).sum(dim=1).to(torch.double)
        if self.fit_intercept:
            X = torch.cat((X, torch.ones(X.shape[0], 1).to(torch.double)), dim=(-1))
        y = energies.unsqueeze(dim=(-1))
        coeff_, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        return coeff_.squeeze(-1)

    def sae(self, species):
        """Compute self energies for molecules.

        Padding atoms will be automatically excluded.

        Arguments:
            species (:class:`torch.Tensor`): Long tensor in shape
                ``(conformations, atoms)``.

        Returns:
            :class:`torch.Tensor`: 1D vector in shape ``(conformations,)``
            for molecular self energies.
        """
        intercept = 0.0
        if self.fit_intercept:
            intercept = self.self_energies[(-1)]
        self_energies = self.self_energies[species]
        self_energies[species == torch.tensor((-1), device=(species.device))] = torch.tensor(0, device=(species.device), dtype=(torch.double))
        return self_energies.sum(dim=1) + intercept

    def subtract_from_dataset(self, atomic_properties, properties):
        """Transformer for :class:`torchani.data.BatchedANIDataset` that
        subtract self energies.
        """
        if self.self_energies is None:
            self_energies = self.sae_from_dataset(atomic_properties, properties)
            self.self_energies = torch.tensor(self_energies, dtype=(torch.double))
        species = atomic_properties['species']
        energies = properties['energies']
        device = energies.device
        energies = energies.to(torch.double) - self.sae(species).to(device)
        properties['energies'] = energies
        return (atomic_properties, properties)

    def forward(self, species_energies: Tuple[(Tensor, Tensor)], cell: Optional[Tensor]=None, pbc: Optional[Tensor]=None) -> SpeciesEnergies:
        """(species, molecular energies)->(species, molecular energies + sae)
        """
        species, energies = species_energies
        sae = self.sae(species).to(energies.device)
        return SpeciesEnergies(species, energies.to(sae.dtype) + sae)


class ChemicalSymbolsToInts:
    __doc__ = 'Helper that can be called to convert chemical symbol string to integers\n\n    Arguments:\n        all_species (:class:`collections.abc.Sequence` of :class:`str`):\n            sequence of all supported species, in order.\n    '

    def __init__(self, all_species):
        self.rev_species = {s:i for i, s in enumerate(all_species)}

    def __call__(self, species):
        """Convert species from squence of strings to 1D tensor"""
        rev = [self.rev_species[s] for s in species]
        return torch.tensor(rev, dtype=(torch.long))

    def __len__(self):
        return len(self.rev_species)


def _get_derivatives_not_none(x: Tensor, y: Tensor, retain_graph: Optional[bool]=None, create_graph: bool=False) -> Tensor:
    ret = torch.autograd.grad([y.sum()], [x], retain_graph=retain_graph, create_graph=create_graph)[0]
    assert ret is not None
    return ret


def hessian(coordinates: Tensor, energies: Optional[Tensor]=None, forces: Optional[Tensor]=None) -> Tensor:
    """Compute analytical hessian from the energy graph or force graph.

    Arguments:
        coordinates (:class:`torch.Tensor`): Tensor of shape `(molecules, atoms, 3)`
        energies (:class:`torch.Tensor`): Tensor of shape `(molecules,)`, if specified,
            then `forces` must be `None`. This energies must be computed from
            `coordinates` in a graph.
        forces (:class:`torch.Tensor`): Tensor of shape `(molecules, atoms, 3)`, if specified,
            then `energies` must be `None`. This forces must be computed from
            `coordinates` in a graph.

    Returns:
        :class:`torch.Tensor`: Tensor of shape `(molecules, 3A, 3A)` where A is the number of
        atoms in each molecule
    """
    if energies is None:
        if forces is None:
            raise ValueError('Energies or forces must be specified')
    if energies is not None:
        if forces is not None:
            raise ValueError('Energies or forces can not be specified at the same time')
    if forces is None:
        assert energies is not None
        forces = -_get_derivatives_not_none(coordinates, energies, create_graph=True)
    flattened_force = forces.flatten(start_dim=1)
    force_components = flattened_force.unbind(dim=1)
    return -torch.stack([_get_derivatives_not_none(coordinates, f, retain_graph=True).flatten(start_dim=1) for f in force_components],
      dim=1)


class FreqsModes(NamedTuple):
    freqs: Tensor
    modes: Tensor


def vibrational_analysis(masses, hessian, unit='cm^-1'):
    """Computing the vibrational wavenumbers from hessian."""
    if unit != 'cm^-1':
        raise ValueError('Only cm^-1 are supported right now')
    assert hessian.shape[0] == 1, 'Currently only supporting computing one molecule a time'
    inv_sqrt_mass = (1 / masses.sqrt()).repeat_interleave(3, dim=1)
    mass_scaled_hessian = hessian * inv_sqrt_mass.unsqueeze(1) * inv_sqrt_mass.unsqueeze(2)
    if mass_scaled_hessian.shape[0] != 1:
        raise ValueError('The input should contain only one molecule')
    mass_scaled_hessian = mass_scaled_hessian.squeeze(0)
    eigenvalues, eigenvectors = torch.symeig(mass_scaled_hessian, eigenvectors=True)
    angular_frequencies = eigenvalues.sqrt()
    frequencies = angular_frequencies / (2 * math.pi)
    wavenumbers = frequencies * 17092
    modes = (eigenvectors.t() * inv_sqrt_mass).reshape(frequencies.numel(), -1, 3)
    return FreqsModes(wavenumbers, modes)


__all__ = [
 'pad', 'pad_atomic_properties', 'present_species', 'hessian',
 'vibrational_analysis', 'strip_redundant_padding',
 'ChemicalSymbolsToInts']