# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/friisj/Private/prosjekter/EMMC-CSA/EMMO-python/demo/horizontal/step2_define_atoms.py
# Compiled at: 2019-06-08 08:26:18
# Size of source mod 2**32: 1209 bytes
"""
Step 2 - define metadata for the ASE Atoms class
------------------------------------------------
In this step we define metadata for the Atoms class in the Atomistic
Simulation Environment (ASE).  This metadata is defined in the file
atoms.json.

We use the dlite.classfactory() to create a subclass of ASE Atoms that
also exposes the attributes as dlite properties. The subclass DLiteAtoms
adds some methods for handling some special attributes.
"""
import ase
from ase.spacegroup import Spacegroup
import dlite
BaseAtoms = dlite.classfactory((ase.Atoms), url='json://atoms.json?mode=r#')

class DLiteAtoms(BaseAtoms):
    __doc__ = 'ASE Atoms class extended as a dlite entity.'

    def _dlite_get_info(self):
        d = self.info.copy()
        sg = Spacegroup(d.get('spacegroup', 'P 1'))
        d['spacegroup'] = sg.symbol
        return [(k, str(v)) for k, v in d.items()]

    def _dlite_set_info(value):
        self.info.update(value)
        self.info['spacegroup'] = Spacegroup(self.info['spacegroup'])

    def _dlite_get_celldisp(self):
        return self.get_celldisp()[:, 0]