# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/DataSources/PDB.py
# Compiled at: 2019-04-23 02:08:32
"""
PDB.py -- Simple classes for reading/manipulating Protein and DNA structural
files in the format of the Protein Data Bank.

Copyright (2005) Whitehead Institute for Biomedical Research (except as noted below)
All Rights Reserved

Author: David Benjamin Gordon

"""
import sys, os, string, re, os.path, operator

class simplePDBatom:
    """
    Trival atom type that knows how to parse an ATOM line
    from a pdb file, and how to print itself out again
    """

    def __init__(self, line=''):
        if line:
            self.atnum = int(line[6:11])
            self.atname = line[12:16].strip()
            self.alt = line[16:17].strip()
            self.resname = line[17:20].strip().replace('+', '')
            self.chain = line[21:22].strip()
            self.resnum = int(line[22:26])
            self.insert = line[26:27].strip()
            self.x = float(line[30:38])
            self.y = float(line[38:46])
            self.z = float(line[46:54])
            self.occ = float(line[54:60])
            self.temp = float(line[60:66])
            self.segid = line[72:76].strip()
            self.elem = line[76:78].strip()
            self.charge = line[78:80].strip()

    def __repr__(self):
        s = 'ATOM  %5d %-4s%s%3s %s%4d%s   %8.3f%8.3f%8.3f%6.2f%6.2f      %4s%-2s%2s' % (
         self.atnum, self.atname, self.alt, self.resname,
         self.chain, self.resnum, self.insert,
         self.x, self.y, self.z,
         self.occ, self.temp, self.segid,
         self.elem, self.charge)
        return s

    def res3to1(self, resname_3letters):
        map = {'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F', 'GLY': 'G', 
           'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L', 'MET': 'M', 
           'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', 'SER': 'S', 
           'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'}
        if map.has_key(resname_3letters):
            return map[resname_3letters]
        else:
            return
            return


class simplePDB:
    """
    Trival PDB reader, with a few handy utilities.
    Relies on simplePDBatom
    """

    def __init__(self, filename):
        self.atoms = []
        self.filename = filename
        PdbFID = open(self.filename, 'r')
        for line in PdbFID.readlines():
            if line[0:4] == 'ATOM':
                a = simplePDBatom(line.strip())
                self.atoms.append(a)

    def get_chain_range(self, chain_id):
        lownum, highnum = (100000, -10000)
        for atom in self.atoms:
            if atom.chain == chain_id:
                if atom.atname == 'CA' or atom.atname == 'C1*':
                    if atom.resnum < lownum:
                        lownum = atom.resnum
                    if atom.resnum > highnum:
                        highnum = atom.resnum

        resnums = range(lownum, highnum + 1)
        return resnums

    def get_chain_sequence(self, chain_id):
        sequence = []
        resnums = self.get_chain_range(chain_id)
        for resnum in resnums:
            res1lett = '-'
            for atom in self.atoms:
                if atom.resnum == resnum and atom.chain == chain_id:
                    if atom.atname == 'CA' or atom.atname == 'C1*':
                        if len(atom.resname) == 3:
                            res1lett = atom.res3to1(atom.resname)
                        else:
                            res1lett = atom.resname

            sequence.append(res1lett)

        return (
         sequence, resnums)