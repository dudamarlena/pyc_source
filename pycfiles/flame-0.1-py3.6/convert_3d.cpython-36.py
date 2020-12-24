# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/chem/convert_3d.py
# Compiled at: 2018-05-22 12:10:29
# Size of source mod 2**32: 1664 bytes
import os, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

def _ETKDG(ifile):
    """ Assigns 3D structures to the molecular structures provided as input.
    """
    try:
        suppl = Chem.SDMolSupplier(ifile)
    except:
        return (False, 'unable to compute 3D structures')
    else:
        filename, fileext = os.path.splitext(ifile)
        ofile = filename + '_3d' + fileext
        num_obj = 0
        with open(ofile, 'w') as (fo):
            for mol in suppl:
                if mol is None:
                    print('ERROR: (@_ETKDG) Unable to obtain 3D structure for molecule #', str(num_obj + 1), 'in file ' + ifile)
                else:
                    mol3 = Chem.AddHs(mol)
                    AllChem.EmbedMolecule(mol3, AllChem.ETKDG())
                    fo.write(Chem.MolToMolBlock(mol3))
                    fo.write('\n$$$$\n')
                    num_obj += 1

        return (
         True, ofile)