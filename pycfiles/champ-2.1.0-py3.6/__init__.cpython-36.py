# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/champ/__init__.py
# Compiled at: 2019-05-22 08:28:32
# Size of source mod 2**32: 1229 bytes
"""
CHAMP (Convex Hull of Admissible Modularity Partitions) implementation
"""
from __future__ import absolute_import
import os
from .plot_domains import plot_2d_domains
from .plot_domains import plot_single_layer_modularity_domains
from .plot_domains import plot_line_halfspaces
from .plot_domains import plot_line_coefficients
from .plot_domains import plot_similarity_heatmap_single_layer
from .plot_domains import plot_multiplex_community
from .champ_functions import create_coefarray_from_partitions
from .champ_functions import create_halfspaces_from_array
from .champ_functions import get_intersection
from .champ_functions import get_random_halfspaces
from .louvain_ext import create_multilayer_igraph_from_edgelist
from .louvain_ext import create_multilayer_igraph_from_adjacency
from .louvain_ext import parallel_multilayer_louvain
from .louvain_ext import parallel_multilayer_louvain_from_adj
from .louvain_ext import parallel_louvain
from .louvain_ext import run_louvain
from .louvain_ext import adjacency_to_edges
from .leiden_ext import run_leiden
from .leiden_ext import parallel_leiden
from .PartitionEnsemble import PartitionEnsemble
__version__ = 'unknown'
from ._version import __version__