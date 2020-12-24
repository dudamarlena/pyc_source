# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Bioscripts/bioscripts.convert/bioscripts/convert/defs.py
# Compiled at: 2011-08-09 08:24:49
"""
Module-wide definitions and constants.

"""
__docformat__ = 'restructuredtext en'
from Bio import Alphabet
from Bio.Alphabet import IUPAC
from Bio.Data import IUPACData
__all__ = [
 'FORMATS',
 'EXT_TO_FORMAT',
 'FORMAT_TO_EXT',
 'KNOWN_FMTS',
 'VERSION',
 'EPILOG',
 'BIOSEQ_ALPHABET_DNA',
 'BIOSEQ_ALPHABET_PROTEIN']
FORMATS = {'clustal': [
             'aln'], 
   'fasta': [
           'fasta', 'fas'], 
   'genbank': [
             'gb', 'gbk', 'gbank'], 
   'nexus': [
           'nexus', 'nex', 'nxs', 'paup'], 
   'phd': [
         'phd'], 
   'phylip': [
            'phy'], 
   'stockholm': [
               'sth'], 
   'qual': [
          'qual'], 
   'tab': [
         'tab']}
EXT_TO_FORMAT = {}
for (k, v) in FORMATS.iteritems():
    EXT_TO_FORMAT[k] = k
    for ext in v:
        EXT_TO_FORMAT[ext] = k

FORMAT_TO_EXT = {}
for (k, v) in FORMATS.iteritems():
    FORMAT_TO_EXT[k] = v[0]

KNOWN_FMTS = FORMATS.keys()
EPILOG = 'FORMAT must be one of %s.\n' % (', ').join(sorted(KNOWN_FMTS))
BIOSEQ_GAP = '-'
BIOSEQ_ALPHABET_GAPPEDAMBIGDNA = Alphabet.Gapped(IUPAC.ambiguous_dna, BIOSEQ_GAP)
BIOSEQ_ALPHABET_DNA = BIOSEQ_ALPHABET_GAPPEDAMBIGDNA
BIOSEQ_ALPHABET_GAPPEDAMBIGPROTEIN = Alphabet.Gapped(IUPAC.extended_protein, BIOSEQ_GAP)
BIOSEQ_ALPHABET_PROTEIN = BIOSEQ_ALPHABET_GAPPEDAMBIGPROTEIN
try:
    from bioscripts.convert import __version__ as VERSION
except:
    VERSION = 'unknown'

_DEV_MODE = True