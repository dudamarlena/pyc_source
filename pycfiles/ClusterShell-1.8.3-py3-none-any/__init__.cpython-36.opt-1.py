# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/__init__.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 1780 bytes
"""ClusterShell Python Library

ClusterShell is an event-driven open source Python library, designed to run
local or distant commands in parallel on server farms or on large clusters.
You can use ClusterShell as a building block to create cluster aware
administration scripts and system applications in Python. It will take care of
common issues encountered on HPC clusters, such as operating on groups of
nodes, running distributed commands using optimized execution algorithms, as
well as gathering results and merging identical outputs, or retrieving return
codes. ClusterShell takes advantage of existing remote shell facilities already
installed on your systems, like SSH.

Please see first:
  - ClusterShell.NodeSet
  - ClusterShell.Task
"""
__version__ = '1.8.3'
__version_info__ = tuple([int(_n) for _n in __version__.split('.')])
__date__ = '2019/12/01'
__author__ = 'Stephane Thiell <sthiell@stanford.edu>'
__url__ = 'http://clustershell.readthedocs.org/'