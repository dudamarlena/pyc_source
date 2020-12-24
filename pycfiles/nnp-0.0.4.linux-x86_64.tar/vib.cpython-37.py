# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.7.5/x64/lib/python3.7/site-packages/nnp/vib.py
# Compiled at: 2019-11-24 03:15:15
# Size of source mod 2**32: 5048 bytes
"""
Vibrational Analysis
====================

The module ``nnp.vib`` contains tools to compute analytical hessian
and do vibrational analysis.
"""
import torch
from torch import Tensor
from typing import NamedTuple, Optional

def _get_derivatives_not_none(x: Tensor, y: Tensor, retain_graph: Optional[bool]=None, create_graph: bool=False) -> Tensor:
    ret = torch.autograd.grad([
     y.sum()],
      [x], retain_graph=retain_graph, create_graph=create_graph)[0]
    assert ret is not None
    return ret


def hessian(coordinates: Tensor, energies: Optional[Tensor]=None, forces: Optional[Tensor]=None) -> Tensor:
    """Compute analytical hessian from the energy graph or force graph.

    Arguments:
        coordinates: Tensor of shape `(molecules, atoms, 3)` or `(atoms, 3)`
        energies: Tensor of shape `(molecules,)`, or scalar, if specified,
            then `forces` must be `None`. This energies must be computed
            from `coordinates` in a graph.
        forces: Tensor of shape `(molecules, atoms, 3)` or `(atoms, 3)`,
            if specified, then `energies` must be `None`. This forces must
            be computed from `coordinates` in a graph.

    Returns:
        Tensor of shape `(molecules, 3 * atoms, 3 * atoms)` or `(3 * atoms, 3 * atoms)`
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
    flattened_force = forces.flatten(start_dim=(-2))
    force_components = flattened_force.unbind(dim=(-1))
    return -torch.stack([_get_derivatives_not_none(coordinates, f, retain_graph=True).flatten(start_dim=(-2)) for f in force_components],
      dim=(-1))


class FreqsModes(NamedTuple):
    angular_frequencies: Tensor
    modes: Tensor


def vibrational_analysis(masses: Tensor, hessian: Tensor) -> FreqsModes:
    """Computing the vibrational wavenumbers from hessian.

    Arguments:
        masses: Tensor of shape `(molecules, atoms)` or `(atoms,)`.
        hessian: Tensor of shape `(molecules, 3 * atoms, 3 * atoms)` or
            `(3 * atoms, 3 * atoms)`.

    Returns:
        A namedtuple `(angular_frequencies, modes)` where

        angular_frequencies:
            Tensor of shape `(molecules, 3 * atoms)` or `(3 * atoms,)`
        modes:
            Tensor of shape `(molecules, modes, atoms, 3)` or `(modes, atoms, 3)`
            where `modes = 3 * atoms` is the number of normal modes.
    """
    inv_sqrt_mass = masses.rsqrt().repeat_interleave(3, dim=(-1))
    mass_scaled_hessian = hessian * inv_sqrt_mass.unsqueeze(-2) * inv_sqrt_mass.unsqueeze(-1)
    eigenvalues, eigenvectors = torch.symeig(mass_scaled_hessian, eigenvectors=True)
    angular_frequencies = eigenvalues.sqrt()
    modes = eigenvectors.transpose(-1, -2) * inv_sqrt_mass.unsqueeze(-2)
    new_shape = modes.shape[:-1] + (-1, 3)
    modes = modes.reshape(new_shape)
    return FreqsModes(angular_frequencies, modes)