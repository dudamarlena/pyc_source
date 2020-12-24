# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.7.5/x64/lib/python3.7/site-packages/torchani/nn.py
# Compiled at: 2019-11-23 13:53:55
# Size of source mod 2**32: 5303 bytes
import torch
from collections import OrderedDict
from torch import Tensor
from typing import Tuple, NamedTuple, Optional

class SpeciesEnergies(NamedTuple):
    species: Tensor
    energies: Tensor


class SpeciesCoordinates(NamedTuple):
    species: Tensor
    coordinates: Tensor


class ANIModel(torch.nn.ModuleDict):
    __doc__ = 'ANI model that compute energies from species and AEVs.\n\n    Different atom types might have different modules, when computing\n    energies, for each atom, the module for its corresponding atom type will\n    be applied to its AEV, after that, outputs of modules will be reduced along\n    different atoms to obtain molecular energies.\n\n    .. warning::\n\n        The species must be indexed in 0, 1, 2, 3, ..., not the element\n        index in periodic table. Check :class:`torchani.SpeciesConverter`\n        if you want periodic table indexing.\n\n    .. note:: The resulting energies are in Hartree.\n\n    Arguments:\n        modules (:class:`collections.abc.Sequence`): Modules for each atom\n            types. Atom types are distinguished by their order in\n            :attr:`modules`, which means, for example ``modules[i]`` must be\n            the module for atom type ``i``. Different atom types can share a\n            module by putting the same reference in :attr:`modules`.\n    '

    @staticmethod
    def ensureOrderedDict(modules):
        if isinstance(modules, OrderedDict):
            return modules
        od = OrderedDict()
        for i, m in enumerate(modules):
            od[str(i)] = m

        return od

    def __init__(self, modules):
        super(ANIModel, self).__init__(self.ensureOrderedDict(modules))

    def forward(self, species_aev: Tuple[(Tensor, Tensor)], cell: Optional[Tensor]=None, pbc: Optional[Tensor]=None) -> SpeciesEnergies:
        species, aev = species_aev
        species_ = species.flatten()
        aev = aev.flatten(0, 1)
        output = aev.new_zeros(species_.shape)
        for i, (_, m) in enumerate(self.items()):
            mask = species_ == i
            midx = mask.nonzero().flatten()
            if midx.shape[0] > 0:
                input_ = aev.index_select(0, midx)
                output.masked_scatter_(mask, m(input_).flatten())

        output = output.view_as(species)
        return SpeciesEnergies(species, torch.sum(output, dim=1))


class Ensemble(torch.nn.ModuleList):
    __doc__ = 'Compute the average output of an ensemble of modules.'

    def __init__(self, modules):
        super().__init__(modules)
        self.size = len(modules)

    def forward(self, species_input: Tuple[(Tensor, Tensor)], cell: Optional[Tensor]=None, pbc: Optional[Tensor]=None) -> SpeciesEnergies:
        sum_ = 0
        for x in self:
            sum_ += x(species_input)[1]

        species, _ = species_input
        return SpeciesEnergies(species, sum_ / self.size)


class Sequential(torch.nn.ModuleList):
    __doc__ = 'Modified Sequential module that accept Tuple type as input'

    def __init__(self, *modules):
        super(Sequential, self).__init__(modules)

    def forward(self, input_: Tuple[(Tensor, Tensor)], cell: Optional[Tensor]=None, pbc: Optional[Tensor]=None):
        for module in self:
            input_ = module(input_, cell=cell, pbc=pbc)

        return input_


class Gaussian(torch.nn.Module):
    __doc__ = 'Gaussian activation'

    def forward(self, x: Tensor) -> Tensor:
        return torch.exp(-x * x)


class SpeciesConverter(torch.nn.Module):
    __doc__ = 'Convert from element index in the periodic table to 0, 1, 2, 3, ...'
    periodic_table = '\n    H                                                                                                                           He\n    Li  Be                                                                                                  B   C   N   O   F   Ne\n    Na  Mg                                                                                                  Al  Si  P   S   Cl  Ar\n    K   Ca  Sc                                                          Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr\n    Rb  Sr  Y                                                           Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe\n    Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn\n    Fr  Ra  Ac  Th  Pa  U   Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og\n    '.strip().split()

    def __init__(self, species):
        super().__init__()
        rev_idx = {s:k for k, s in enumerate(self.periodic_table, 1)}
        maxidx = max(rev_idx.values())
        self.register_buffer('conv_tensor', torch.full((maxidx + 2,), (-1), dtype=(torch.long)))
        for i, s in enumerate(species):
            self.conv_tensor[rev_idx[s]] = i

    def forward(self, input_: Tuple[(Tensor, Tensor)], cell: Optional[Tensor]=None, pbc: Optional[Tensor]=None):
        """Convert species from periodic table element index to 0, 1, 2, 3, ... indexing"""
        species, coordinates = input_
        return SpeciesCoordinates(self.conv_tensor[species], coordinates)