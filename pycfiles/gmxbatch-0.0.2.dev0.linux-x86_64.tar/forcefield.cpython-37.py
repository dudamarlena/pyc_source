# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/forcefields/forcefield.py
# Compiled at: 2020-02-28 04:24:12
# Size of source mod 2**32: 4288 bytes
import copy, os
from typing import List, Union, Optional
from ..mdp import MDP
from ..moleculetype import MoleculeType

class ForceField:
    __doc__ = "Representation of a MD force field. This is a general superclass, actual force field implementations should have\n    a corresponding subclass.\n\n    Information incorporated in attributes:\n\n    1) MDP options (`mdp`):\n        The GROMACS preprocessor needs a file (.mdp) with various parameters describing the interactions, engine\n        options, algorithm choices etc. Part of these are force field dependent (e.g. cut-off distances), others change\n        from run to run (e.g. thermostat reference temperature or algorithm, step count, output frequency etc.).\n\n    2) Force field name (`name`)\n\n    3) Force field include topology file name (`itp`)\n\n    4) Molecule types:\n        GROMACS users typically employ 'pdb2gmx' to construct a topology from the coordinate set. 'gmxbatch' does not\n        wrap pdb2gmx, instead requires .itp files containing [ moleculetype ] entries. Upon writing the final topology\n        files (.top), these will be #include-d. Molecule types are loaded from a set of directories (`moltypespath`\n        attribute, a list of strings) upon force field initialization. Since molecule types contain information on\n        atom types, partial charges, etc, they typically cannot be shared between force fields.\n    "
    mdp: MDP
    name: str
    itp: str
    moltypespath: List[str]
    _moleculetypes: List[MoleculeType]

    def __init__(self, itp: str, moltypespath: Union[(str, List[str])]):
        """Create a new force field instance

        :param itp: include topology file name (e.g. charmm36m.ff/forcefield.itp)
        :type itp: str
        :param moltypespath: molecule types lookup directories
        :type moltypespath: list of strings (or a single string)
        """
        self.itp = itp
        self._moleculetypes = []
        self.moltypespath = [moltypespath] if isinstance(moltypespath, str) else moltypespath[:]
        self.reloadMoleculetypes()

    def reloadMoleculetypes(self):
        """Reload molecule types from the path."""
        self._moleculetypes = []
        for path in self.moltypespath:
            for filename in os.listdir(path):
                if filename.lower().endswith('.itp'):
                    print('Trying to load molecule type from {}'.format(filename))
                    try:
                        mtypes = list(MoleculeType.loadITP(os.path.join(path, filename)))
                    except (RuntimeError, ValueError, OSError, FileNotFoundError):
                        raise
                    else:
                        self._moleculetypes.extend(mtypes)

    def moleculetypes(self) -> List[MoleculeType]:
        return sorted([copy.deepcopy(mt) for mt in self._moleculetypes], key=(lambda mt: (mt.name, mt.itpfile)))

    def moleculetype(self, name: str, count: int=1, itpfilenamepart: Optional[str]=None) -> MoleculeType:
        """Get a molecule type instance.

        The instance is a deep copy, i.e. subsequent calls to this method give physically different objects.

        :param name: moleculetype name
        :type name: str
        :param count: the number of this molecule in your system
        :type count: int
        :param itpfilenamepart: part of the itp file name if needed for disambiguating molecule types with the same name
        :type itpfilenamepart: str or None
        :return: a molecule type instance
        :rtype: MoleculeType
        """
        mtypes = [mt for mt in self._moleculetypes if mt.name == name and (itpfilenamepart is None or itpfilenamepart in mt.itpfile)]
        if len(mtypes) > 1:
            raise ValueError('Ambiguous molecule type name. Please supply a (more specific) itp file name part.')
        else:
            if not mtypes:
                raise ValueError('Unknown molecule type')
        mt = copy.deepcopy(mtypes[0])
        mt.count = count
        return mt