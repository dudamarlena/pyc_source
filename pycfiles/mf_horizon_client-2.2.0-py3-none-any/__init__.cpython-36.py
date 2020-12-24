# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/__init__.py
# Compiled at: 2020-05-09 07:13:20
# Size of source mod 2**32: 317 bytes
import mf_horizon_client.client, mf_horizon_client.data_structures, mf_horizon_client.schemas
from ._version import get_versions
_versions_dict = get_versions()
__version__ = _versions_dict['version']
__gitsha__ = _versions_dict['full-revisionid']
del get_versions
del _versions_dict