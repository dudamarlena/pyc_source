# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phenry/.config/i3/fluidspaces/src/fluidspaces/__init__.py
# Compiled at: 2017-10-25 04:10:39
# Size of source mod 2**32: 323 bytes
import pkg_resources
from .i3_commands import i3Commands
from .menu_commands import MenuCommands
from .workspace import Workspace
from .workspaces import Workspaces
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    pass