# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/__init__.py
# Compiled at: 2020-04-15 14:09:48
# Size of source mod 2**32: 689 bytes
"""This is Dallinger, a platform for simulating evolution with people."""
from . import bots, command_line, config, models, information, nodes, networks, processes, transformations, experiment, experiments, heroku, registration
from .patches import patch
import logging
from logging import NullHandler
logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
patch()
__all__ = ('bots', 'command_line', 'config', 'models', 'information', 'nodes', 'networks',
           'processes', 'transformations', 'heroku', 'experiment', 'experiments',
           'registration', 'logger')