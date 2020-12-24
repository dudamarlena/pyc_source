# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/constants.py
# Compiled at: 2017-03-17 13:53:52
# Size of source mod 2**32: 3170 bytes
"""
List of all pointers and constants used in the Amber topology file.

Can be used like:
   from parmed.constants import *
"""
from __future__ import division
from math import pi as _pi, sqrt as _sqrt, log10 as _log10, acos as _acos
__all__ = [
 'AMBER_ELECTROSTATIC', 'AMBER_POINTERS', 'NATOM', 'NTYPES', 'NBONH', 'MBONA', 'NTHETH',
 'MTHETA', 'NPHIH', 'MPHIA', 'NHPARM', 'NPARM', 'NEXT', 'NRES', 'NBONA', 'NTHETA',
 'NPHIA', 'NUMBND', 'NUMANG', 'NPTRA', 'NATYP', 'NPHB', 'IFPERT', 'NBPER', 'NGPER',
 'NDPER', 'MBPER', 'MGPER', 'MDPER', 'IFBOX', 'NMXRS', 'IFCAP', 'NUMEXTRA', 'NCOPY',
 'NNB', 'RAD_TO_DEG', 'DEG_TO_RAD', 'TRUNCATED_OCTAHEDRON_ANGLE']
AMBER_ELECTROSTATIC = 18.2223
CHARMM_ELECTROSTATIC = _sqrt(332.0716)
AMBER_POINTERS = '\nNATOM  : total number of atoms\nNTYPES : total number of distinct atom types\nNBONH  : number of bonds containing hydrogen\nMBONA  : number of bonds not containing hydrogen\nNTHETH : number of angles containing hydrogen\nMTHETA : number of angles not containing hydrogen\nNPHIH  : number of dihedrals containing hydrogen\nMPHIA  : number of dihedrals not containing hydrogen\nNHPARM : currently not used\nNPARM  : currently not used\nNEXT   : number of excluded atoms\nNRES   : number of residues\nNBONA  : MBONA + number of constraint bonds\nNTHETA : MTHETA + number of constraint angles\nNPHIA  : MPHIA + number of constraint dihedrals\nNUMBND : number of unique bond types\nNUMANG : number of unique angle types\nNPTRA  : number of unique dihedral types\nNATYP  : number of atom types in parameter file, see SOLTY below\nNPHB   : number of distinct 10-12 hydrogen bond pair types\nIFPERT : set to 1 if perturbation info is to be read in\nNBPER  : number of bonds to be perturbed\nNGPER  : number of angles to be perturbed\nNDPER  : number of dihedrals to be perturbed\nMBPER  : number of bonds with atoms completely in perturbed group\nMGPER  : number of angles with atoms completely in perturbed group\nMDPER  : number of dihedrals with atoms completely in perturbed groups\nIFBOX  : set to 1 if standard periodic box, 2 when truncated octahedral\nNMXRS  : number of atoms in the largest residue\nIFCAP  : set to 1 if the CAP option from edit was specified\nNUMEXTRA: number of extra points\nNCOPY  : Number of copies for advanded simulations\n'
NATOM = 0
NTYPES = 1
NBONH = 2
MBONA = 3
NTHETH = 4
MTHETA = 5
NPHIH = 6
MPHIA = 7
NHPARM = 8
NPARM = 9
NEXT = 10
NRES = 11
NBONA = 12
NTHETA = 13
NPHIA = 14
NUMBND = 15
NUMANG = 16
NPTRA = 17
NATYP = 18
NPHB = 19
IFPERT = 20
NBPER = 21
NGPER = 22
NDPER = 23
MBPER = 24
MGPER = 25
MDPER = 26
IFBOX = 27
NMXRS = 28
IFCAP = 29
NUMEXTRA = 30
NCOPY = 31
NNB = NEXT
RAD_TO_DEG = 180.0 / _pi
DEG_TO_RAD = _pi / 180.0
TRUNCATED_OCTAHEDRON_ANGLE = _acos(-0.3333333333333333) * 180 / _pi
TINY = 1e-08
SMALL = 0.0001
TINY_DIGITS = int(_log10(TINY) + 0.5)
SMALL_DIGITS = int(_log10(SMALL) + 0.5)
DEFAULT_ENCODING = 'UTF-8'