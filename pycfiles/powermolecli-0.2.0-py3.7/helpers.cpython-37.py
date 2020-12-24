# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorcli/minitorcli/lib/helpers.py
# Compiled at: 2020-05-10 10:56:22
# Size of source mod 2**32: 3488 bytes
"""
Import all parts from helpers here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging.config
from ..minitorcliexceptions import SetupFailed
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '10-05-2019'
__copyright__ = 'Copyright 2020, Vincent Schouten'
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
LOGGER_BASENAME = 'helpers'
LOGGER = logging.getLogger(LOGGER_BASENAME)

def setup_link(state, transferagent, tunnel, bootstrapagent, assistant):
    """Starts instantiated TransferAgents, opens instantiated Tunnel(s) and starts instantiated Machine(s).

    This function also passes the instantiated objects to the StateManager, which
    will stop Machines and close Tunnels after a KeyboardInterrupt (by the user
    or by the program (in COMMAND and FILE mode).

    Args:
        state (StateManager): An instantiated StateManager object.
        transfer_agent (TransferAgent): An instantiated TransferAgent object.
        bootstrap_agent (BootstrapAgent): <>
        tunnel (Tunnel): An instantiated Tunnel object.
        assistant (Assistant): An instantiated Assistant object.

    """
    if not transferagent.start():
        raise SetupFailed(transferagent)
    else:
        LOGGER.info('agent has been transferred to last host')
        state.add_object(tunnel)
        if not tunnel.start():
            raise SetupFailed(tunnel)
        LOGGER.info('tunneling has been set up')
        if not bootstrapagent.start():
            raise SetupFailed(bootstrapagent)
        LOGGER.info('agent has been executed')
        state.add_object(assistant)
        assert assistant.start(), assistant
    LOGGER.info('agent assistant has been executed')