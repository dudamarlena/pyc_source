# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/barnesc/work/code/nblast-rs/nblast-py/pynblast/__init__.py
# Compiled at: 2020-04-20 07:50:20
# Size of source mod 2**32: 471 bytes
"""Top-level package for nblast-rs."""
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