# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/perseuspy/__init__.py
# Compiled at: 2019-11-19 08:16:09
# Size of source mod 2**32: 615 bytes
"""
perseuspy module for Python-Perseus interop.
"""
from perseuspy.version import version_string as __version__
import perseuspy.dependent_peptides, perseuspy.io.perseus.matrix, pandas as pd
pd.DataFrame.to_perseus = perseuspy.io.perseus.matrix.to_perseus
pd.read_perseus = perseuspy.io.perseus.matrix.read_perseus
import perseuspy.io.perseus.network
from perseuspy.io.perseus.network import read_networks, write_networks
import networkx as nx
nx.from_perseus = perseuspy.io.perseus.network.from_perseus
nx.to_perseus = perseuspy.io.perseus.network.to_perseus