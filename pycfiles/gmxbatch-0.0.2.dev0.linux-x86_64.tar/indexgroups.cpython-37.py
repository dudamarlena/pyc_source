# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/indexgroups.py
# Compiled at: 2020-03-26 06:17:54
# Size of source mod 2**32: 3790 bytes
from collections import OrderedDict
from typing import Dict, List, Optional
from .conffiles import Coordinates
from .mdengine import MDEngine
from .moleculetype import MoleculeType

class IndexGroups:
    __doc__ = 'Index groups for GROMACS\n    '
    groups: Dict[(str, List[int])]
    filename: str

    def __init__(self, filename: Optional[str]=None):
        if filename is not None:
            self.loadNDX(filename)
        self.groups = OrderedDict()

    def getDefault(self, conf: Coordinates, engine: MDEngine, moleculetypes: List[MoleculeType]):
        """Get the default index groups from GROMACS (using make_ndx)

        In addition to the standard groups (e.g. System, Protein, Ions, Water etc.), the following groups are created
        by looking at the molecule types:

            - Solvent
            - Solute
            - Solvent_and_ions
            - Ions
            - Other

        :param conf: coordinate set
        :type conf: gmxbatch.conffiles.Coordinates
        :param engine: MD engine
        :type engine: gmxbatch.mdengine.MDEngine
        :param moleculetypes: list of molecule types
        :type moleculetypes: gmxbatch.moleculetype.MoleculeType
        """
        engine.generateDefaultIndex(conf.filename, 'index.ndx')
        self.loadNDX('index.ndx')
        solvent = []
        ions = []
        solute = []
        other = []
        lastindex = 1
        for mt in moleculetypes:
            count = mt.count * len(mt.atoms)
            if mt.kind == 'Solvent':
                solvent.extend(list(range(lastindex, lastindex + count)))
            else:
                if mt.kind == 'Solute':
                    solute.extend(list(range(lastindex, lastindex + count)))
                else:
                    if mt.kind == 'Ion':
                        ions.extend(list(range(lastindex, lastindex + count)))
                    else:
                        other.extend(list(range(lastindex, lastindex + count)))
            lastindex = lastindex + count

        self.groups['Solvent'] = solvent
        self.groups['Solute'] = solute
        self.groups['Solvent_and_ions'] = sorted(solvent + ions)
        self.groups['Ions'] = ions
        self.groups['Other'] = other

    def loadNDX(self, filename: Optional[str]):
        """Load an index file

        :param filename: index file name (.ndx)
        :type filename: str
        """
        if filename is None:
            filename = self.filename
        newgroups = OrderedDict()
        with open(filename, 'rt') as (f):
            thisgroup = None
            for line in f:
                l = line.split(';')[0].strip()
                if not l:
                    continue
                elif l.startswith('[') and l.endswith(']'):
                    thisgroup = l[1:-1].strip()
                    newgroups[thisgroup] = []
                elif isinstance(thisgroup, str):
                    newgroups[thisgroup].extend([int(x) for x in l.split()])
                else:
                    raise ValueError('Invalid index file')

        self.groups = newgroups
        self.filename = filename

    def saveNDX(self, filename: Optional[str]=None):
        """Save groups to an index file

        :param filename: index file name (.ndx)
        :type filename: str
        """
        if filename is None:
            filename = self.filename
        with open(filename, 'wt') as (f):
            for group in self.groups:
                f.write('[ {} ]\n'.format(group))
                for i in range(len(self.groups[group]) // 15 + 1):
                    f.write(' '.join(['{:>4d}'.format(n) for n in self.groups[group][i * 15:i * 15 + 15]]) + '\n')

                f.write('\n')