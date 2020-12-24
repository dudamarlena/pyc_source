# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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