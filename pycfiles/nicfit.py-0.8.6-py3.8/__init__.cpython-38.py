# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/__init__.py
# Compiled at: 2020-04-04 14:09:08
# Size of source mod 2**32: 469 bytes
from . import command
from . import logger
from .app import Application
from .logger import getLogger
from ._argparse import ArgumentParser
from .config import Config, ConfigOpts
from .command import Command, CommandError
from .__about__ import __version__ as version
log = getLogger(__package__)
__all__ = [
 'log', 'getLogger', 'version', 'logger',
 'Application', 'ArgumentParser', 'Config', 'ConfigOpts',
 'command', 'Command', 'CommandError']