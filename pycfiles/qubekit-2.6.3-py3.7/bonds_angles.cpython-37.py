# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/VEHICLe/bonds_angles.py
# Compiled at: 2019-09-18 10:44:24
# Size of source mod 2**32: 6415 bytes
"""
Get the hessians from the VEHICLe dataset

Get the json dict from qcportal
From this, initialise a Ligand object, add in the qm-optimised coords and hessian
Generate a

"""
from QUBEKit.engines import RDKit
from QUBEKit.ligand import Ligand
from QUBEKit.mod_seminario import ModSeminario
from QUBEKit.parametrisation.base_parametrisation import Parametrisation
from QUBEKit.utils import constants
from QUBEKit.utils.helpers import check_symmetry
import os
from pathlib import Path
import pickle, numpy as np, pandas as pd, qcportal as ptl
from rdkit import DataStructs
from rdkit.Chem import AllChem

class BondsAndAngles:

    def __init__(self):
        self.client, self.ds, self.records = (None, None, None)
        self.get_records()
        self.bond_data = []
        self.bond_labels = []
        self.angle_data = []
        self.angle_labels = []

    def get_records(self):
        if os.path.exists('records.pkl'):
            with open('records.pkl', 'rb') as (rec_file):
                self.client, self.ds, self.records = pickle.load(rec_file)
        else:
            self.client = ptl.FractalClient()
            self.client.list_collections('OptimizationDataset')
            self.ds = self.client.get_collection('OptimizationDataset', 'OpenFF VEHICLe Set 1')
            self.ds.df.head()
            self.ds.list_specifications()
            self.records = self.ds.data.records
            pickle_data = (self.client, self.ds, self.records)
            with open('records.pkl', 'wb') as (rec_file):
                pickle.dump(pickle_data, rec_file)

    def loop_over_mols(self):
        for i, item in enumerate(self.records):
            try:
                ptl_name = item.strip('\n')
                smiles = self.records[ptl_name].attributes['canonical_smiles']
                print(f"iter: {str(i).zfill(5)}; smiles: {smiles}")
                try:
                    opt_record = self.ds.get_entry(ptl_name).object_map['default']
                except KeyError:
                    continue

                optimisation = self.client.query_procedures(id=opt_record)[0]
                try:
                    hessian = self.client.query_results(molecule=(optimisation.final_molecule), driver='hessian')[0].return_result
                except IndexError:
                    continue

                conversion = constants.HA_TO_KCAL_P_MOL / constants.BOHR_TO_ANGS ** 2
                hessian = np.array(hessian).flatten()
                hessian = hessian.reshape(int(len(hessian) ** 0.5), -1) * conversion
                opt_struct = self.client.query_procedures(id=opt_record)[0].get_final_molecule()
                mol = self.calc_mod_sem(smiles, hessian, opt_struct)
                finger_prints = self.calc_fingerprint()
                self.format_data(mol, finger_prints)
            except BaseException as exc:
                try:
                    self.bond_data = np.array(self.bond_data)
                    np.save('test_data', self.bond_data)
                    self.bond_labels = np.array(self.bond_labels)
                    np.save('test_labels', self.bond_labels)
                    raise exc
                finally:
                    exc = None
                    del exc

    @staticmethod
    def calc_mod_sem(smiles, hessian, opt_struct):
        mol = Ligand(opt_struct, name='initial_test')
        mol.coords['qm'] = mol.coords['input']
        mol.hessian = hessian
        mol.parameter_engine = 'none'
        Parametrisation(mol).gather_parameters()
        with open('Modified_Seminario_Bonds.txt', 'a+') as (bonds_file):
            with open('Modified_Seminario_Angles.txt', 'a+') as (angles_file):
                bonds_file.write(f"\n\n{smiles}\n\n")
                angles_file.write(f"\n\n{smiles}\n\n")
        ModSeminario(mol).modified_seminario_method()
        mol.write_pdb(name='test')
        return mol

    @staticmethod
    def calc_fingerprint():
        rdkit_mol = RDKit().read_file(Path('test.pdb'))
        finger_prints = {}
        for atom in rdkit_mol.GetAtoms():
            atom_index = atom.GetIdx()
            fp = AllChem.GetHashedAtomPairFingerprintAsBitVect(rdkit_mol, maxLength=4, fromAtoms=[atom_index])
            arr = np.zeros(1)
            DataStructs.ConvertToNumpyArray(fp, arr)
            finger_prints[atom_index] = arr

        os.system('rm test.pdb')
        return finger_prints

    def format_data(self, mol, finger_prints):
        for bond, val in mol.HarmonicBondForce.items():
            self.bond_data.append(np.concatenate((finger_prints[bond[0]], finger_prints[bond[1]])))
            self.bond_labels.append(val)


if __name__ == '__main__':
    BondsAndAngles().loop_over_mols()