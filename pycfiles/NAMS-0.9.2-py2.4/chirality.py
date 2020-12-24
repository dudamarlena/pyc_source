# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nams/chirality.py
# Compiled at: 2013-09-26 10:32:38
"""
The NAMS python package calculates the similarity between molecules based on the 
structural/topological relationships of each atom towards all the others 
within a molecule.

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published on the official site of Open Source Initiative
and attached above.

Copyright (C) 2013, Andre Falcao and Ana Teixeira, University of Lisbon - LaSIGE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Please cite the authors in any work or product based on this material:

AL Teixeira, AO Falcao. 2013. A non-contiguous atom matching structural similarity function. J. Chem. Inf. Model. DOI: 10.1021/ci400324u.

"""
import openbabel, pybel

class Chirality:
    """
    This class determinates the chirality of a molecule according to the R-S convention based
    on linear notations to represent the molecular structure: SMILES or InCHI.
    It requires Python 2.6 or above and Openbabel 2.3.1.
    """
    __module__ = __name__

    def __init__(self, line_notation, input_type, isotopes=False):
        self.obmol = None
        self.n_atoms = 0
        self.all_bonds = {}
        self.chiral_atoms = []
        self.chiralities = []
        obConversion = openbabel.OBConversion()
        mol_can = openbabel.OBMol()
        obConversion.SetInAndOutFormats(input_type, 'can')
        obConversion.ReadString(mol_can, line_notation)
        can_smi = obConversion.WriteString(mol_can)
        self.can_smi = can_smi
        obConversion.SetInFormat('can')
        mol = openbabel.OBMol()
        obConversion.ReadString(mol, can_smi)
        mol.AddHydrogens()
        self.obmol = mol
        chir = False
        for c in can_smi:
            if c == '@':
                if chir == True:
                    self.chiral_atoms.append(1)
                    chir = False
                else:
                    chir = True
            elif chir == True:
                self.chiral_atoms.append(-1)
                chir = False

        self.n_atoms = self.obmol.NumAtoms()
        self.n_bonds = self.obmol.NumBonds()
        self.all_bonds = {}
        self.auto_chirs = 0
        for atom_id in range(self.n_atoms):
            at = self.obmol.GetAtom(atom_id + 1)
            if at.IsChiral():
                self.auto_chirs += 1
            bonds = self.get_bonds(self.obmol, atom_id)
            for b in bonds:
                self.all_bonds.setdefault(b[0], {})[b[1]] = 1
                self.all_bonds.setdefault(b[1], {})[b[0]] = 1

        if len(self.chiral_atoms) == self.auto_chirs:
            self.calc_chiralities(isotopes)
        else:
            self.chiralities = [
             0] * self.n_atoms
        return

    def get_chirality(self, atom_id):
        return self.chiralities[atom_id]

    def calc_chiralities(self, isotopes):
        chir_atom = 0
        for atom_id in range(self.n_atoms):
            at = self.obmol.GetAtom(atom_id + 1)
            if at.IsChiral():
                chiral_levels = []
                level0 = []
                for n_atom in openbabel.OBAtomAtomIter(at):
                    id2 = n_atom.GetIndex()
                    elliminated = []
                    elliminated.append((atom_id, id2))
                    elliminated.append((id2, atom_id))
                    lvl_bonds = [[]]
                    lvl = 0
                    start_set = [id2]
                    self.process_bonds(start_set, elliminated, lvl_bonds)
                    lvl_bonds = lvl_bonds[:-1]
                    at2 = self.obmol.GetAtom(id2 + 1)
                    levels = []
                    if isotopes:
                        levels.append(at2.GetExactMass())
                    else:
                        levels.append(at2.GetAtomicNum())
                    for lvl in lvl_bonds:
                        levels.append(lvl)

                    chiral_levels.append(levels)

                chiral = self.is_chiral(chiral_levels, chir_atom)
                self.chiralities.append(chiral)
                chir_atom += 1
            else:
                self.chiralities.append(0)

    def process_bonds(self, start_set, elliminated, lvl_bonds):
        to_follow = {}
        for at1 in start_set:
            for at2 in self.all_bonds[at1]:
                if (
                 at1, at2) not in elliminated:
                    my_bond = (
                     at1, at2)
                    b = self.obmol.GetBond(at1 + 1, at2 + 1)
                    bo = b.GetBO()
                    for i in range(0, bo):
                        lvl_bonds[(-1)].append(my_bond)

                    if at2 < self.n_atoms:
                        to_follow.setdefault(at2, 1)
                    elliminated.append((at1, at2))
                    elliminated.append((at2, at1))

        new_starts = to_follow.keys()
        if len(new_starts) > 0:
            lvl_bonds.append([])
            self.process_bonds(new_starts, elliminated, lvl_bonds)

    def get_bonds(self, mol, atom_id):
        natoms = mol.NumAtoms()
        bonds = []
        obatom = mol.GetAtom(atom_id + 1)
        id1 = obatom.GetIndex()
        for n_atom in openbabel.OBAtomAtomIter(obatom):
            id2 = n_atom.GetIndex()
            bonds.append((id1, id2))

        return bonds

    def is_chiral(self, chiral_levels, chir_atom):
        irotation = self.chiral_atoms[chir_atom]
        magic_list = []
        i = 0
        for lig in chiral_levels:
            lig_id = [
             [
              lig[0]]]
            for lvl in lig[1:]:
                nlvl = []
                for bnd in lvl:
                    at = self.obmol.GetAtom(bnd[1] + 1)
                    nlvl.append(at.GetAtomicNum())

                nlvl.sort()
                nlvl.reverse()
                lig_id.append(nlvl)

            magic_list.append((lig_id, i))
            i += 1

        magic_list.sort()
        permutations = []
        duplicate_ligs = {}
        aux = [ x[0] for x in magic_list ]
        for lig in magic_list:
            if aux.count(lig[0]) > 1:
                duplicate_ligs[lig[1]] = chiral_levels[lig[1]]
            permutations.append(lig[1])

        permutations.reverse()
        if duplicate_ligs:
            return 0
        return self.parity(permutations, irotation)

    def priority_e_z(self, duplicate_ligs, permutations):
        import doubleb_e_z
        ez = doubleb_e_z.Stereodoubleb(self.can_smi)
        e_z_lig = {}
        print duplicate_ligs
        for k in duplicate_ligs:
            for x in duplicate_ligs[k][1:len(duplicate_ligs[k])]:
                for (at1, at2) in x:
                    at_1 = self.obmol.GetAtom(at1 + 1)
                    at_2 = self.obmol.GetAtom(at2 + 1)
                    bond = at_2.GetBond(at_1)
                    if bond.IsDouble():
                        b_idx = bond.GetIdx()
                        if ez.get_e_z(at_1, at_2) != 0:
                            if k in e_z_lig.keys():
                                e_z_lig[k].append(ez.get_e_z(at_1, at_2))
                            else:
                                e_z_lig[k] = [
                                 ez.get_e_z(at_1, at_2)]

        keys = e_z_lig.keys()
        import operator
        sorted_x = sorted(e_z_lig.iteritems(), key=operator.itemgetter(1))
        x = 0
        permutations_old = permutations[:]
        for ezlig in sorted_x:
            idx = permutations_old.index(keys[x])
            permutations[idx] = ezlig[0]
            x = x + 1

        return permutations

    def priority_chiral(self, duplicate_ligs, permutations):
        chir_lig = {}
        import chiraux
        for k in duplicate_ligs:
            unique_atoms = []
            for x in duplicate_ligs[k][1:len(duplicate_ligs[k])]:
                for (at1, at2) in x:
                    if at1 not in unique_atoms:
                        unique_atoms.append(at1)
                        at_1 = self.obmol.GetAtom(at1 + 1)
                        if at_1.IsChiral():
                            if k in chir_lig.keys():
                                chir_lig[k].append(ch.get_chirality(at1))
                            else:
                                chir_lig[k] = [
                                 ch.get_chirality(at1)]
                    if at2 not in unique_atoms:
                        unique_atoms.append(at2)
                        at_2 = self.obmol.GetAtom(at2 + 1)
                        if at_2.IsChiral():
                            if k in chir_lig.keys():
                                chir_lig[k].append(ch.get_chirality(at2))
                            else:
                                chir_lig[k] = [
                                 ch.get_chirality(at2)]

        keys = chir_lig.keys()
        import operator
        sorted_x = sorted(chir_lig.iteritems(), key=operator.itemgetter(1))
        x = 0
        permutations_old = permutations[:]
        for chirlig in sorted_x:
            idx = permutations_old.index(keys[x])
            permutations[idx] = chirlig[0]
            x = x + 1

        return permutations

    def parity(self, permutation, irotation):
        i = 1
        e = permutation[0]
        while e != 0:
            e = permutation[e]
            i += 1

        if i == 2:
            aux = permutation[0]
            zero = permutation[aux]
            for i in range(0, 3):
                if permutation[i] != aux and permutation[i] != zero:
                    if permutation[i] == i and irotation == 1:
                        return -1
                    elif permutation[i] == i and irotation == -1:
                        return 1
                    elif permutation[i] != i and irotation == 1:
                        return 1
                    elif permutation[i] != i and irotation == -1:
                        return -1

        if i == 3:
            if irotation == 1:
                return 1
            elif irotation == -1:
                return -1
        if i == 4:
            if irotation == 1:
                return -1
            elif irotation == -1:
                return 1
        i = 1
        e = permutation[1]
        while e != 1:
            e = permutation[e]
            i += 1

        if i == 2:
            if irotation == 1:
                return -1
            elif irotation == -1:
                return 1
        if i == 3:
            if irotation == 1:
                return 1
            elif irotation == -1:
                return -1
        if permutation[2] == 2 and irotation == 1:
            return 1
        elif permutation[2] == 2 and irotation == -1:
            return -1
        elif permutation[2] != 2 and irotation == 1:
            return -1
        elif permutation[2] != 2 and irotation == -1:
            return 1