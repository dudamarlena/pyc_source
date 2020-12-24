# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/__init__.py
# Compiled at: 2019-02-08 08:28:12
# Size of source mod 2**32: 335 bytes
__version__ = '0.3.1'
from .setup import generateSetup
from .dist import getDependencies
from .dist import generateDists
from .help import printHelp
from .utils import *