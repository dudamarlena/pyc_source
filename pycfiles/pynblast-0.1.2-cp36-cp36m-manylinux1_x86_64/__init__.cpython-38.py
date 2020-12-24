# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/barnesc/work/code/nblast-rs/nblast-py/pynblast/__init__.py
# Compiled at: 2020-04-20 07:50:20
# Size of source mod 2**32: 471 bytes
__doc__ = 'Top-level package for nblast-rs.'
__author__ = 'Chris L. Barnes'
__email__ = 'chrislloydbarnes@gmail.com'
from .pynblast import get_version
__version__ = get_version()
__version_info__ = tuple((int(n) for n in __version__.split('.')))
from .util import rectify_tangents, Idx, Symmetry
from .arena import NblastArena
from .score_matrix import ScoreMatrix
__all__ = [
 'NblastArena', 'ScoreMatrix', 'Symmetry', 'rectify_tangents', 'Idx']