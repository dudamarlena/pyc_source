# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/__init__.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 1780 bytes
__doc__ = 'ClusterShell Python Library\n\nClusterShell is an event-driven open source Python library, designed to run\nlocal or distant commands in parallel on server farms or on large clusters.\nYou can use ClusterShell as a building block to create cluster aware\nadministration scripts and system applications in Python. It will take care of\ncommon issues encountered on HPC clusters, such as operating on groups of\nnodes, running distributed commands using optimized execution algorithms, as\nwell as gathering results and merging identical outputs, or retrieving return\ncodes. ClusterShell takes advantage of existing remote shell facilities already\ninstalled on your systems, like SSH.\n\nPlease see first:\n  - ClusterShell.NodeSet\n  - ClusterShell.Task\n'
__version__ = '1.8.3'
__version_info__ = tuple([int(_n) for _n in __version__.split('.')])
__date__ = '2019/12/01'
__author__ = 'Stephane Thiell <sthiell@stanford.edu>'
__url__ = 'http://clustershell.readthedocs.org/'