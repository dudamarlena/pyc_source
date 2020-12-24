# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/rdkit/rdkit.py
# Compiled at: 2017-03-01 21:14:20
# Size of source mod 2**32: 2234 bytes
"""
This package contains classes responsible for loading rdkit objects
"""
from __future__ import print_function, absolute_import
from parmed.formats import PDBFile
from parmed.utils.six.moves import StringIO

class RDKit(object):

    @staticmethod
    def load(rmol):
        """
        Load a :class:`Mol` object and return a populated :class:`Structure`
        instance

        Parameters
        ----------
        rmol: :class:`Mol`
            RDKit :class:`Mol` object to convert

        Examples
        --------
        >>> from rdkit import Chem
        >>> import parmed as pmd
        >>> mol = Chem.MolFromSmiles('Cc1ccccc1')
        >>> struct = pmd.load_rdkit(mol)
        """
        from rdkit import Chem
        fh = StringIO(Chem.MolToPDBBlock(rmol))
        return PDBFile.parse(fh)

    @staticmethod
    def from_smiles(smiles, coordinates=True):
        """
        Load smiles string to :class:`Structure`

        Parameters
        ----------
        smiles : str, smiles
        coordinates : bool, default True
            if True, use `rdkit.Chem.AllChem.EmbedMultipleConfs to assign coordinates

        Returns
        -------
        parm : :class:`Structure`
        """
        from rdkit import Chem
        from rdkit.Chem import AllChem
        mol = Chem.MolFromSmiles(smiles)
        if coordinates:
            AllChem.EmbedMultipleConfs(mol, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
        parm = RDKit.load(mol)
        if not coordinates:
            parm.coordinates = None
            parm._coordinates = None
        return parm

    @staticmethod
    def from_sdf(filename, structure=False):
        """
        Load SDF file to :class:`Structure`

        Parameters
        ----------
        filename: str
        structure : bool, default False
            if True, return a :class:`Structure`
            if False, return a list of :class:`Structure`
        """
        from rdkit import Chem
        sdf_collection = Chem.SDMolSupplier(filename, removeHs=False)
        if structure:
            mol = next(sdf_collection)
            return RDKit.load(mol)
        else:
            return [RDKit.load(mol) for mol in sdf_collection]