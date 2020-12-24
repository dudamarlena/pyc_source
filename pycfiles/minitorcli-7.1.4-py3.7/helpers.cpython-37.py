# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorcli/minitorcli/lib/helpers.py
# Compiled at: 2020-01-23 11:19:04
# Size of source mod 2**32: 3790 bytes
"""
Import all parts from helpers here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging.config
from ..minitorcliexceptions import SetupFailed
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-04-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
LOGGER_BASENAME = 'helpers'
LOGGER = logging.getLogger(LOGGER_BASENAME)

def setup_link(state, transfer_agent, tunnel, bootstrap_agent, machine):
    """Starts instantiated TransferAgents, opens instantiated Tunnel(s) and starts instantiated Machine(s).

    This function also passes the instantiated objects to the StateManager, which
    will stop Machines and close Tunnels after a KeyboardInterrupt (by the user
    or by the program (in COMMAND and FILE mode).

    Args:
        state (StateManager): An instantiated StateManager object.
        transfer_agent (TransferAgent): An instantiated TransferAgent object.
        bootstrap_agent (BootstrapAgent): <>
        tunnel (Tunnel): An instantiated Tunnel object.
        machine (Machine): An instantiated Machine object.

    """
    if not transfer_agent.start():
        raise SetupFailed(transfer_agent)
    if transfer_agent.__class__.__name__ == 'FirstTransferAgent':
        LOGGER.info('Agent transferred to %s ', machine.hostname)
    else:
        if transfer_agent.__class__.__name__ == 'ConsecutiveTransferAgent':
            LOGGER.info('Agent transferred through Tunnel to %s ', machine.hostname)
        else:
            state.add_object(tunnel)
            if not tunnel.open():
                raise SetupFailed(tunnel)
            LOGGER.info('Tunnel opened (%s)', tunnel.ip_address_i)
            state.add_object(bootstrap_agent)
            if not bootstrap_agent.start():
                raise SetupFailed(bootstrap_agent)
            LOGGER.info('Agent is executed')
            state.add_object(machine)
            assert machine.start(), machine
        LOGGER.info('Machine started (%s)', machine.hostname)