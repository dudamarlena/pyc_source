# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/__init__.py
# Compiled at: 2018-09-27 06:12:47
# Size of source mod 2**32: 474 bytes
from .base_ampal import Polymer, Monomer, Atom
from .protein import Polypeptide, Residue, align, flat_list_to_polymer, flat_list_to_dummy_chain
from .nucleic_acid import Polynucleotide, Nucleotide
from .ligands import Ligand, LigandGroup
from .assembly import Assembly, AmpalContainer
from .pdb_parser import load_pdb
from .pseudo_atoms import PseudoGroup, PseudoMonomer, PseudoAtom, Primitive
from .dssp import tag_dssp_data
__version__ = '1.4.0'