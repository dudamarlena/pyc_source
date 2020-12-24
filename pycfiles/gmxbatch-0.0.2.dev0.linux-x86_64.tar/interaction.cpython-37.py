# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/intermolecularinteractions/interaction.py
# Compiled at: 2020-03-15 09:00:45
# Size of source mod 2**32: 888 bytes
from typing import Sequence, Tuple

class Interaction:
    atoms: Tuple[(int, ...)]
    func: int
    parameters: Tuple[(float, ...)]
    type: str

    def __init__(self, type: str, atoms: Sequence[int], functype: int, parameters: Sequence[float]):
        self.type = type
        if type == 'bond' and len(atoms) != 2:
            raise ValueError('Bonds need two atoms.')
        else:
            if type == 'angle' and len(atoms) != 3:
                raise ValueError('Angles need three atoms.')
            else:
                if type == 'dihedral':
                    if len(atoms) != 4:
                        raise ValueError('Dihedrals need four atoms.')
        self.atoms = tuple(atoms)
        self.func = functype
        self.parameters = tuple(parameters)

    def __str__(self) -> str:
        return ' '.join(['{:>7d}'.format(a) for a in self.atoms]) + f" {self.func:>5d}  " + '   '.join([str(p) for p in self.parameters]) + '\n'