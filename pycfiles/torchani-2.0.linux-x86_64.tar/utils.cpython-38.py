# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/torchani/utils.py
# Compiled at: 2020-04-29 02:37:56
# Size of source mod 2**32: 18239 bytes
import torch
from torch import Tensor
import torch.utils.data, math
from collections import defaultdict
from typing import Tuple, NamedTuple, Optional
from torchani.units import sqrt_mhessian2invcm, sqrt_mhessian2milliev, mhessian2fconst
from .nn import SpeciesEnergies

def empty_list():
    return []


def stack_with_padding(properties, padding):
    output = defaultdict(empty_list)
    for p in properties:
        for k, v in p.items():
            output[k].append(torch.as_tensor(v))
        else:
            for k, v in output.items():
                if v[0].dim() == 0:
                    output[k] = torch.stack(v)
                else:
                    output[k] = torch.nn.utils.rnn.pad_sequence(v, True, padding[k])
            else:
                return output


def broadcast_first_dim(properties):
    num_molecule = 1
    for k, v in properties.items():
        shape = list(v.shape)
        n = shape[0]
        if num_molecule != 1:
            if not n == 1:
                if not n == num_molecule:
                    raise AssertionError('unable to broadcast')
                else:
                    num_molecule = n
        else:
            for k, v in properties.items():
                shape = list(v.shape)
                shape[0] = num_molecule
                properties[k] = v.expand(shape)
            else:
                return properties


def pad_atomic_properties--- This code section failed: ---

 L.  54         0  LOAD_CLOSURE             'properties'
                2  BUILD_TUPLE_1         1 
                4  LOAD_LISTCOMP            '<code_object <listcomp>>'
                6  LOAD_STR                 'pad_atomic_properties.<locals>.<listcomp>'
                8  MAKE_FUNCTION_8          'closure'
               10  LOAD_DEREF               'properties'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_METHOD              keys
               18  CALL_METHOD_0         0  ''
               20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  STORE_DEREF              'vectors'

 L.  55        26  LOAD_CLOSURE             'properties'
               28  BUILD_TUPLE_1         1 
               30  LOAD_LISTCOMP            '<code_object <listcomp>>'
               32  LOAD_STR                 'pad_atomic_properties.<locals>.<listcomp>'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_DEREF               'properties'
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  LOAD_METHOD              keys
               44  CALL_METHOD_0         0  ''
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'scalars'

 L.  56        52  LOAD_CLOSURE             'properties'
               54  BUILD_TUPLE_1         1 
               56  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               58  LOAD_STR                 'pad_atomic_properties.<locals>.<dictcomp>'
               60  MAKE_FUNCTION_8          'closure'
               62  LOAD_DEREF               'vectors'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'padded_sizes'

 L.  57        70  LOAD_CLOSURE             'vectors'
               72  BUILD_TUPLE_1         1 
               74  LOAD_LISTCOMP            '<code_object <listcomp>>'
               76  LOAD_STR                 'pad_atomic_properties.<locals>.<listcomp>'
               78  MAKE_FUNCTION_8          'closure'
               80  LOAD_DEREF               'properties'
               82  GET_ITER         
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'num_molecules'

 L.  58        88  LOAD_GLOBAL              sum
               90  LOAD_FAST                'num_molecules'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'total_num_molecules'

 L.  59        96  BUILD_MAP_0           0 
               98  STORE_FAST               'output'

 L.  60       100  LOAD_FAST                'scalars'
              102  GET_ITER         
              104  FOR_ITER            138  'to 138'
              106  STORE_DEREF              'k'

 L.  61       108  LOAD_GLOBAL              torch
              110  LOAD_METHOD              stack
              112  LOAD_CLOSURE             'k'
              114  BUILD_TUPLE_1         1 
              116  LOAD_LISTCOMP            '<code_object <listcomp>>'
              118  LOAD_STR                 'pad_atomic_properties.<locals>.<listcomp>'
              120  MAKE_FUNCTION_8          'closure'
              122  LOAD_DEREF               'properties'
              124  GET_ITER         
              126  CALL_FUNCTION_1       1  ''
              128  CALL_METHOD_1         1  ''
              130  LOAD_FAST                'output'
              132  LOAD_DEREF               'k'
              134  STORE_SUBSCR     
              136  JUMP_BACK           104  'to 104'

 L.  62       138  LOAD_DEREF               'vectors'
              140  GET_ITER         
              142  FOR_ITER            308  'to 308'
              144  STORE_DEREF              'k'

 L.  63       146  LOAD_DEREF               'properties'
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  LOAD_DEREF               'k'
              154  BINARY_SUBSCR    
              156  STORE_FAST               'tensor'

 L.  64       158  LOAD_GLOBAL              list
              160  LOAD_FAST                'tensor'
              162  LOAD_ATTR                shape
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'shape'

 L.  65       168  LOAD_FAST                'tensor'
              170  LOAD_ATTR                device
              172  STORE_FAST               'device'

 L.  66       174  LOAD_FAST                'tensor'
              176  LOAD_ATTR                dtype
              178  STORE_FAST               'dtype'

 L.  67       180  LOAD_FAST                'total_num_molecules'
              182  LOAD_FAST                'shape'
              184  LOAD_CONST               0
              186  STORE_SUBSCR     

 L.  68       188  LOAD_FAST                'padded_sizes'
              190  LOAD_DEREF               'k'
              192  BINARY_SUBSCR    
              194  LOAD_FAST                'shape'
              196  LOAD_CONST               1
              198  STORE_SUBSCR     

 L.  69       200  LOAD_GLOBAL              torch
              202  LOAD_ATTR                full
              204  LOAD_FAST                'shape'
              206  LOAD_FAST                'padding_values'
              208  LOAD_DEREF               'k'
              210  BINARY_SUBSCR    
              212  LOAD_FAST                'device'
              214  LOAD_FAST                'dtype'
              216  LOAD_CONST               ('device', 'dtype')
              218  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              220  LOAD_FAST                'output'
              222  LOAD_DEREF               'k'
              224  STORE_SUBSCR     

 L.  70       226  LOAD_CONST               0
              228  STORE_FAST               'index0'

 L.  71       230  LOAD_GLOBAL              zip
              232  LOAD_FAST                'num_molecules'
              234  LOAD_DEREF               'properties'
              236  CALL_FUNCTION_2       2  ''
              238  GET_ITER         
              240  FOR_ITER            306  'to 306'
              242  UNPACK_SEQUENCE_2     2 
              244  STORE_FAST               'n'
              246  STORE_FAST               'x'

 L.  72       248  LOAD_FAST                'x'
              250  LOAD_DEREF               'k'
              252  BINARY_SUBSCR    
              254  LOAD_ATTR                shape
              256  LOAD_CONST               1
              258  BINARY_SUBSCR    
              260  STORE_FAST               'original_size'

 L.  73       262  LOAD_FAST                'x'
              264  LOAD_DEREF               'k'
              266  BINARY_SUBSCR    
              268  LOAD_FAST                'output'
              270  LOAD_DEREF               'k'
              272  BINARY_SUBSCR    
              274  LOAD_FAST                'index0'
              276  LOAD_FAST                'index0'
              278  LOAD_FAST                'n'
              280  BINARY_ADD       
              282  BUILD_SLICE_2         2 
              284  LOAD_CONST               0
              286  LOAD_FAST                'original_size'
              288  BUILD_SLICE_2         2 
              290  LOAD_CONST               Ellipsis
              292  BUILD_TUPLE_3         3 
              294  STORE_SUBSCR     

 L.  74       296  LOAD_FAST                'index0'
              298  LOAD_FAST                'n'
              300  INPLACE_ADD      
              302  STORE_FAST               'index0'
              304  JUMP_BACK           240  'to 240'
              306  JUMP_BACK           142  'to 142'

 L.  75       308  LOAD_FAST                'output'
              310  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 56


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
    else:
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
    coordinates_cell -= coordinates_cell.floor() * pbc
    return torch.matmul(coordinates_cell, cell)


class EnergyShifter(torch.nn.Module):
    __doc__ = 'Helper class for adding and subtracting self atomic energies\n\n    This is a subclass of :class:`torch.nn.Module`, so it can be used directly\n    in a pipeline as ``[input->AEVComputer->ANIModel->EnergyShifter->output]``.\n\n    Arguments:\n        self_energies (:class:`collections.abc.Sequence`): Sequence of floating\n            numbers for the self energy of each atom type. The numbers should\n            be in order, i.e. ``self_energies[i]`` should be atom type ``i``.\n        fit_intercept (bool): Whether to calculate the intercept during the LSTSQ\n            fit. The intercept will also be taken into account to shift energies.\n    '

    def __init__(self, self_energies, fit_intercept=False):
        super(EnergyShifter, self).__init__()
        self.fit_intercept = fit_intercept
        if self_energies is not None:
            self_energies = torch.tensor(self_energies, dtype=(torch.double))
        self.register_buffer('self_energies', self_energies)

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

    def forward(self, species_energies: Tuple[(Tensor, Tensor)], cell: Optional[Tensor]=None, pbc: Optional[Tensor]=None) -> SpeciesEnergies:
        """(species, molecular energies)->(species, molecular energies + sae)
        """
        species, energies = species_energies
        sae = self.sae(species)
        return SpeciesEnergies(species, energies + sae)


class ChemicalSymbolsToInts:
    __doc__ = "Helper that can be called to convert chemical symbol string to integers\n\n    On initialization the class should be supplied with a :class:`list` (or in\n    general :class:`collections.abc.Sequence`) of :class:`str`. The returned\n    instance is a callable object, which can be called with an arbitrary list\n    of the supported species that is converted into a tensor of dtype\n    :class:`torch.long`. Usage example:\n\n    .. code-block:: python\n\n       from torchani.utils import ChemicalSymbolsToInts\n\n\n       # We initialize ChemicalSymbolsToInts with the supported species\n       species_to_tensor = ChemicalSymbolsToInts(['H', 'C', 'Fe', 'Cl'])\n\n       # We have a species list which we want to convert to an index tensor\n       index_tensor = species_to_tensor(['H', 'C', 'H', 'H', 'C', 'Cl', 'Fe'])\n\n       # index_tensor is now [0 1 0 0 1 3 2]\n\n\n    .. warning::\n\n        If the input is a string python will iterate over\n        characters, this means that a string such as 'CHClFe' will be\n        intepreted as 'C' 'H' 'C' 'l' 'F' 'e'. It is recommended that you\n        input either a :class:`list` or a :class:`numpy.ndarray` ['C', 'H', 'Cl', 'Fe'],\n        and not a string. The output of a call does NOT correspond to a\n        tensor of atomic numbers.\n\n    Arguments:\n        all_species (:class:`collections.abc.Sequence` of :class:`str`):\n            sequence of all supported species, in order.\n    "

    def __init__(self, all_species):
        self.rev_species = {i:s for i, s in enumerate(all_species)}

    def __call__(self, species):
        """Convert species from sequence of strings to 1D tensor"""
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


class VibAnalysis(NamedTuple):
    freqs: Tensor
    modes: Tensor
    fconstants: Tensor
    rmasses: Tensor


def vibrational_analysis(masses, hessian, mode_type='MDU', unit='cm^-1'):
    """Computing the vibrational wavenumbers from hessian.

    Note that normal modes in many popular software packages such as
    Gaussian and ORCA are output as mass deweighted normalized (MDN).
    Normal modes in ASE are output as mass deweighted unnormalized (MDU).
    Some packages such as Psi4 let ychoose different normalizations.
    Force constants and reduced masses are calculated as in Gaussian.

    mode_type should be one of:
    - MWN (mass weighted normalized)
    - MDU (mass deweighted unnormalized)
    - MDN (mass deweighted normalized)

    MDU modes are not orthogonal, and not normalized,
    MDN modes are not orthogonal, and normalized.
    MWN modes are orthonormal, but they correspond
    to mass weighted cartesian coordinates (x' = sqrt(m)x).
    """
    if unit == 'meV':
        unit_converter = sqrt_mhessian2milliev
    else:
        if unit == 'cm^-1':
            unit_converter = sqrt_mhessian2invcm
        else:
            raise ValueError('Only meV and cm^-1 are supported right now')
    assert hessian.shape[0] == 1, 'Currently only supporting computing one molecule a time'
    inv_sqrt_mass = (1 / masses.sqrt()).repeat_interleave(3, dim=1)
    mass_scaled_hessian = hessian * inv_sqrt_mass.unsqueeze(1) * inv_sqrt_mass.unsqueeze(2)
    if mass_scaled_hessian.shape[0] != 1:
        raise ValueError('The input should contain only one molecule')
    mass_scaled_hessian = mass_scaled_hessian.squeeze(0)
    eigenvalues, eigenvectors = torch.symeig(mass_scaled_hessian, eigenvectors=True)
    angular_frequencies = eigenvalues.sqrt()
    frequencies = angular_frequencies / (2 * math.pi)
    wavenumbers = unit_converter(frequencies)
    mw_normalized = eigenvectors.t()
    md_unnormalized = mw_normalized * inv_sqrt_mass
    norm_factors = 1 / torch.norm(md_unnormalized, dim=1)
    md_normalized = md_unnormalized * norm_factors.unsqueeze(1)
    rmasses = norm_factors ** 2
    fconstants = mhessian2fconst(eigenvalues) * rmasses
    if mode_type == 'MDN':
        modes = md_normalized.reshape(frequencies.numel(), -1, 3)
    else:
        if mode_type == 'MDU':
            modes = md_unnormalized.reshape(frequencies.numel(), -1, 3)
        else:
            if mode_type == 'MWN':
                modes = mw_normalized.reshape(frequencies.numel(), -1, 3)
            return VibAnalysis(wavenumbers, modes, fconstants, rmasses)


def get_atomic_masses(species):
    """Convert a tensor of znumbers into a tensor of atomic masses

    Atomic masses supported are the first 119 elements, and are taken from:

    Atomic weights of the elements 2013 (IUPAC Technical Report). Meija, J.,
    Coplen, T., Berglund, M., et al. (2016). Pure and Applied Chemistry, 88(3), pp.
    265-291. Retrieved 30 Nov. 2016, from doi:10.1515/pac-2015-0305

    They are all consistent with those used in ASE

    Arguments:
        species (:class:`torch.Tensor`): tensor with atomic numbers

    Returns:
        :class:`torch.Tensor`: Tensor of dtype :class:`torch.double`, with
        atomic masses, with the same shape as the input.
    """
    assert len((species == 0).nonzero()) == 0
    default_atomic_masses = torch.tensor([
     0.0, 1.008, 4.002602, 6.94,
     9.0121831, 10.81, 12.011, 14.007,
     15.999, 18.99840316, 20.1797, 22.98976928,
     24.305, 26.9815385, 28.085, 30.973762,
     32.06, 35.45, 39.948, 39.0983,
     40.078, 44.955908, 47.867, 50.9415,
     51.9961, 54.938044, 55.845, 58.933194,
     58.6934, 63.546, 65.38, 69.723,
     72.63, 74.921595, 78.971, 79.904,
     83.798, 85.4678, 87.62, 88.90584,
     91.224, 92.90637, 95.95, 97.90721,
     101.07, 102.9055, 106.42, 107.8682,
     112.414, 114.818, 118.71, 121.76,
     127.6, 126.90447, 131.293, 132.90545196,
     137.327, 138.90547, 140.116, 140.90766,
     144.242, 144.91276, 150.36, 151.964,
     157.25, 158.92535, 162.5, 164.93033,
     167.259, 168.93422, 173.054, 174.9668,
     178.49, 180.94788, 183.84, 186.207,
     190.23, 192.217, 195.084, 196.966569,
     200.592, 204.38, 207.2, 208.9804,
     208.98243, 209.98715, 222.01758, 223.01974,
     226.02541, 227.02775, 232.0377, 231.03588,
     238.02891, 237.04817, 244.06421, 243.06138,
     247.07035, 247.07031, 251.07959, 252.083,
     257.09511, 258.09843, 259.101, 262.11,
     267.122, 268.126, 271.134, 270.133,
     269.1338, 278.156, 281.165, 281.166,
     285.177, 286.182, 289.19, 289.194,
     293.204, 293.208, 294.214],
      dtype=(torch.double),
      device=(species.device))
    masses = default_atomic_masses[species]
    return masses


PERIODIC_TABLE = '\n    H                                                                                                                           He\n    Li  Be                                                                                                  B   C   N   O   F   Ne\n    Na  Mg                                                                                                  Al  Si  P   S   Cl  Ar\n    K   Ca  Sc                                                          Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr\n    Rb  Sr  Y                                                           Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe\n    Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn\n    Fr  Ra  Ac  Th  Pa  U   Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og\n    '.strip().split()
__all__ = [
 'pad_atomic_properties', 'present_species', 'hessian',
 'vibrational_analysis', 'strip_redundant_padding',
 'ChemicalSymbolsToInts', 'get_atomic_masses']