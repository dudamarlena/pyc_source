# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioUtil/__init__.py
# Compiled at: 2018-11-26 23:33:43
# Size of source mod 2**32: 808 bytes
from pkg_resources import get_distribution
__version__ = get_distribution('BioUtil').version
__all__ = ['xzFile', 'xzopen',
 'tsv', 'tsvFile', 'tsvRecord',
 'vcf', 'vcfFile', 'vcfReader', 'vcfWriter',
 'samFile',
 'fastaFile', 'fastqFile', 'fastaRecord', 'fastqRecord',
 'cachedFasta', 'faidx',
 'log']
from .xz import xzFile, xzopen
from .tsv import tsvFile, tsvRecord
from .vcf import vcfFile, vcfReader, vcfWriter, _vcf
from pysam import AlignmentFile as samFile
import pysam as sam
from .cached_fasta import cachedFasta
fastaReader = cachedFasta
from .fastq import fastqFile, fastqRecord, fastaFile, fastaRecord
import pyfaidx as faidx
from . import log